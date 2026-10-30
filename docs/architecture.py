"""Render docs/architecture.png.

Requires Graphviz and `pip install diagrams`; run from the repository root:
    python docs/architecture.py
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, Fargate
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import Users
from diagrams.aws.management import AutoScaling, CloudwatchLogs
from diagrams.aws.network import ElbApplicationLoadBalancer, Endpoint, InternetGateway, NATGateway
from diagrams.aws.security import IdentityAndAccessManagementIamRole
from diagrams.aws.storage import S3
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Github

GRAPH = {
    "fontsize": "26",
    "labelloc": "t",
    "dpi": "96",
    "fontname": "Helvetica",
    "pad": "0.6",
    "nodesep": "0.7",
    "ranksep": "1.0",
    "splines": "spline",
}
NODE = {"fontsize": "14", "fontname": "Helvetica"}
PUBLIC = {"bgcolor": "#E9F3E6", "pencolor": "#7AA116", "fontname": "Helvetica"}
PRIVATE = {"bgcolor": "#E6F2F8", "pencolor": "#147EBA", "fontname": "Helvetica"}
TRAFFIC = {"color": "#232F3E", "penwidth": "1.6"}
AWS_CALL = {"color": "#527FFF", "style": "dashed"}
PIPELINE = {"color": "#D45B07", "penwidth": "1.6"}

with Diagram(
    "Flask Hello Birthday API on ECS Fargate",
    filename="docs/architecture",
    show=False,
    direction="LR",
    graph_attr=GRAPH,
    node_attr=NODE,
):
    users = Users("Users")

    with Cluster("CI/CD: GitHub Actions"):
        github = Github("Push / PR\nto develop")
        checks = GithubActions("Lint + pytest\nimage smoke test\nterraform test")
        deploy = GithubActions("Deploy job\n(env: production)")
        terraform = Terraform("terraform plan\n-out + apply")

    with Cluster("AWS Region us-east-1"):
        role = IdentityAndAccessManagementIamRole("OIDC deploy role\n(no stored keys)")
        ecr = ECR("ECR\nimmutable SHA tags\nscan on push")
        state = S3("Terraform state\n(S3 + lockfile)")
        dynamodb = Dynamodb("DynamoDB\nusers table\nPITR")
        logs = CloudwatchLogs("CloudWatch Logs")
        scaling = AutoScaling("Target tracking\nCPU 60%, 2-5 tasks")

        with Cluster("VPC 10.0.0.0/16"):
            igw = InternetGateway("Internet\ngateway")
            ddb_endpoint = Endpoint("DynamoDB\ngateway endpoint")

            with Cluster("Public subnets (us-east-1a, us-east-1c)", graph_attr=PUBLIC):
                alb = ElbApplicationLoadBalancer(
                    "Application\nLoad Balancer\n(HTTP / optional HTTPS)"
                )
                nat = NATGateway("NAT gateway\n(single, 1a)")

            with Cluster("Private subnets: no public IPs", graph_attr=PRIVATE):
                task_a = Fargate("Fargate task (1a)\ngunicorn :8000")
                task_c = Fargate("Fargate task (1c)\ngunicorn :8000")

    tasks = [task_a, task_c]

    users >> Edge(label="HTTP / HTTPS", **TRAFFIC) >> igw >> Edge(**TRAFFIC) >> alb
    alb >> Edge(label="ALB SG only", **TRAFFIC) >> tasks
    tasks >> Edge(label="Get/PutItem", **AWS_CALL) >> ddb_endpoint >> Edge(**AWS_CALL) >> dynamodb
    tasks >> Edge(label="image pull, logs", **AWS_CALL) >> nat
    nat >> Edge(**AWS_CALL) >> [ecr, logs]
    scaling >> Edge(style="dotted", color="#888888") >> tasks

    github >> Edge(**PIPELINE) >> checks >> Edge(label="default branch", **PIPELINE) >> deploy
    deploy >> Edge(label="AssumeRoleWithWebIdentity", **PIPELINE) >> role
    deploy >> Edge(label="docker push :sha", **PIPELINE) >> ecr
    deploy >> Edge(**PIPELINE) >> terraform
    terraform >> Edge(style="dashed", color="#7B42BC") >> [state, alb]
