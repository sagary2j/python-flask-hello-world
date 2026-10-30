variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix for resource names. Must match the bootstrap stack so the deploy role can manage IAM roles."
  type        = string
  default     = "flask-hello-world"
}

variable "image_tag" {
  description = "Tag of the container image in ECR to deploy (CI passes the git commit SHA)."
  type        = string
}

variable "ecr_repository_name" {
  description = "ECR repository created by the bootstrap stack."
  type        = string
  default     = "flask-docker-app"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table holding usernames and dates of birth."
  type        = string
  default     = "users"
}

variable "dynamodb_deletion_protection" {
  description = "Protect the users table from accidental deletion (disable before terraform destroy)."
  type        = bool
  default     = true
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones for the subnets; one public and one private subnet per zone."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1c"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets (ALB and NAT gateway), one per availability zone."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets (Fargate tasks), one per availability zone."
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "single_nat_gateway" {
  description = "Use one NAT gateway for all private subnets. Cheaper, but egress depends on a single AZ."
  type        = bool
  default     = true
}

variable "allowed_ingress_cidrs" {
  description = "CIDR blocks allowed to reach the load balancer."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "certificate_arn" {
  description = "Optional ACM certificate ARN. When set, the ALB serves HTTPS and redirects HTTP to HTTPS."
  type        = string
  default     = null
}

variable "container_port" {
  description = "Port gunicorn listens on inside the container."
  type        = number
  default     = 8000
}

variable "task_cpu" {
  description = "Fargate task CPU units."
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Fargate task memory (MiB)."
  type        = number
  default     = 512
}

variable "min_tasks" {
  description = "Minimum number of running tasks."
  type        = number
  default     = 2
}

variable "max_tasks" {
  description = "Maximum number of running tasks."
  type        = number
  default     = 5
}

variable "cpu_target_percent" {
  description = "Average service CPU utilisation that autoscaling aims for."
  type        = number
  default     = 60
}

variable "container_insights" {
  description = "Enable CloudWatch Container Insights on the cluster (extra cost)."
  type        = bool
  default     = false
}

variable "log_retention_days" {
  description = "Retention for the application log group."
  type        = number
  default     = 14
}
