output "alb_url" {
  description = "Public URL of the service."
  value       = "${var.certificate_arn == null ? "http" : "https"}://${aws_lb.main.dns_name}"
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.user_table.name
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.app.name
}
