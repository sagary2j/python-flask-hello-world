variable "aws_region" {
  description = "AWS region for the ECR repository."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Must match project_name in the main stack; the deploy role may only manage IAM roles with this prefix."
  type        = string
  default     = "flask-hello-world"
}

variable "github_repository" {
  description = "GitHub repository (owner/name) allowed to assume the deploy role."
  type        = string
  default     = "sagary2j/python-flask-hello-world"
}

variable "github_environment" {
  description = "GitHub Actions environment whose jobs may assume the deploy role."
  type        = string
  default     = "production"
}

variable "create_oidc_provider" {
  description = "Create the GitHub OIDC provider. Set false if the account already has one."
  type        = bool
  default     = true
}

variable "ecr_repository_name" {
  description = "ECR repository for the application image."
  type        = string
  default     = "flask-docker-app"
}

variable "images_to_keep" {
  description = "Number of most recent images kept in ECR."
  type        = number
  default     = 30
}
