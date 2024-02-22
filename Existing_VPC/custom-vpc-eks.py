import pulumi
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s

# Retrieve the ID of the existing VPC
existing_vpc_id = "your-existing-vpc-id"

# Define your custom subnet CIDR blocks
subnet1_cidr_block = "10.1.1.0/24"
subnet2_cidr_block = "10.1.2.0/24"

# Create subnets with the custom CIDR blocks in the existing VPC
subnet1 = aws.ec2.Subnet("subnet1",
    vpc_id=existing_vpc_id,
    cidr_block=subnet1_cidr_block)

subnet2 = aws.ec2.Subnet("subnet2",
    vpc_id=existing_vpc_id,
    cidr_block=subnet2_cidr_block)

# Retrieve the ID of the existing security group or define your custom security group
existing_security_group_id = "your-existing-security-group-id"

# Create EKS cluster with custom configurations using the existing VPC and security group
eks_cluster = eks.Cluster("blog-demo-python",
    vpc_id=existing_vpc_id,
    subnet_ids=[subnet1.id, subnet2.id],
    security_group_ids=[existing_security_group_id],  # Use existing security group ID
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
