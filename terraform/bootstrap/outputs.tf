output "deploy_role_arn" {
  description = "Set this as the AWS_DEPLOY_ROLE_ARN GitHub Actions variable."
  value       = aws_iam_role.github_deploy.arn
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}
