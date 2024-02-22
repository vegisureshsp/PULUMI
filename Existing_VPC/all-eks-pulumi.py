import pulumi
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s 

# Create a new VPC
vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")

# Create subnets
subnet1 = aws.ec2.Subnet("subnet1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24")

subnet2 = aws.ec2.Subnet("subnet2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24")

# Create a security group
security_group = aws.ec2.SecurityGroup("my-security-group",
    vpc_id=vpc.id,
    description="Allow HTTP traffic",
    ingress=[{
        "protocol": "tcp",
        "from_port": 80,
        "to_port": 80,
        "cidr_blocks": ["0.0.0.0/0"],
    }])

# Create an internet gateway
internet_gateway = aws.ec2.InternetGateway("internet-gateway",
    vpc_id=vpc.id)

# Create a route table and route
route_table = aws.ec2.RouteTable("route-table",
    vpc_id=vpc.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": internet_gateway.id,
    }])

# Associate subnets with the route table
subnet1_association = aws.ec2.RouteTableAssociation("subnet1-association",
    subnet_id=subnet1.id,
    route_table_id=route_table.id)

subnet2_association = aws.ec2.RouteTableAssociation("subnet2-association",
    subnet_id=subnet2.id,
    route_table_id=route_table.id)

# Create EKS cluster
eks_cluster = eks.Cluster("blog-demo-python",
    vpc_id=vpc.id,
    subnet_ids=[subnet1.id, subnet2.id],
    security_group_ids=[security_group.id],
    instance_type="t3.medium",
    node_group_opts={
        "desiredCapacity": 2,
        "instanceType": "t3.medium",
        "region": aws.Region.EU_WEST_1,  # Set your desired region here
        "tags": {"Environment": "Production"}  # Add any additional tags if required
    })

# Define the Kubernetes Deployment
app_deployment = k8s.apps.v1.Deployment("app-deployment",
    metadata={
        "name": "nginx-deployment",
    },
    spec={
        "selector": {
            "matchLabels": {"app": "nginx"},
        },
        "replicas": 2,
        "template": {
            "metadata": {"labels": {"app": "nginx"}},
            "spec": {
                "containers": [{
                    "name": "nginx",
                    "image": "nginx",
                    "ports": [{"containerPort": 80}],
                }],
            },
        },
    })

# Define the Kubernetes Service
app_service = k8s.core.v1.Service("app-service",
    metadata={
        "name": "nginx-service",
    },
    spec={
        "ports": [{"port": 80}],
        "selector": {"app": "nginx"},
    })

# Export the Kubernetes resources
pulumi.export("app_deployment", app_deployment.metadata)
pulumi.export("app_service", app_service.metadata)
