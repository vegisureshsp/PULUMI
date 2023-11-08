import pulumi
import pulumi_eks as eks

# Get some values from the Pulumi configuration (or use defaults)
config = pulumi.Config()
min_cluster_size = config.get_float("minClusterSize", 1)
max_cluster_size = config.get_float("maxClusterSize", 3)
desired_cluster_size = config.get_float("desiredClusterSize", 1)
eks_node_instance_type = config.get("eksNodeInstanceType", "t2.micro")
existing_vpc_id = "vpc-01bab204d8528eedb"  # Replace with your existing VPC ID
existing_public_subnet_ids = ["subnet-03cea030789b37116", "subnet-0285a9715566d8961"]  # Replace with your public subnet IDs
existing_private_subnet_ids = ["subnet-049bde5a5f60f8920", "subnet-026a7bd2e301fac3b"]  # Replace with your private subnet IDs

# Create the EKS cluster using the existing VPC and subnets
eks_cluster = eks.Cluster("eks-cluster",
    vpc_id=existing_vpc_id,
    public_subnet_ids=existing_public_subnet_ids,
    private_subnet_ids=existing_private_subnet_ids,
    instance_type=eks_node_instance_type,
    desired_capacity=desired_cluster_size,
    min_size=min_cluster_size,
    max_size=max_cluster_size,
    node_associate_public_ip_address=False,
)

# Export values at the stack level
pulumi.export("kubeconfig", eks_cluster.kubeconfig)
pulumi.export("vpcId", existing_vpc_id)