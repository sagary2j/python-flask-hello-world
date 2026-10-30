mock_provider "aws" {
  mock_data "aws_caller_identity" {
    defaults = { account_id = "123456789012" }
  }

  mock_data "aws_iam_policy_document" {
    defaults = { json = "{}" }
  }

  mock_data "aws_ecr_repository" {
    defaults = { repository_url = "123456789012.dkr.ecr.us-east-1.amazonaws.com/flask-docker-app" }
  }

  mock_resource "aws_lb" {
    override_during = plan
    defaults = {
      arn      = "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/flask-hello-world/0123456789abcdef"
      dns_name = "flask-hello-world.elb.example.com"
    }
  }

  mock_resource "aws_lb_target_group" {
    defaults = { arn = "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/flask-hello-world/0123456789abcdef" }
  }

  mock_resource "aws_iam_role" {
    defaults = { arn = "arn:aws:iam::123456789012:role/flask-hello-world-mock" }
  }

  mock_resource "aws_dynamodb_table" {
    defaults = { arn = "arn:aws:dynamodb:us-east-1:123456789012:table/users" }
  }

  mock_resource "aws_ecs_cluster" {
    defaults = { arn = "arn:aws:ecs:us-east-1:123456789012:cluster/flask-hello-world" }
  }

  mock_resource "aws_ecs_task_definition" {
    defaults = { arn = "arn:aws:ecs:us-east-1:123456789012:task-definition/flask-hello-world:1" }
  }
}

variables {
  image_tag = "0123abc"
}

run "defaults" {
  command = plan

  assert {
    condition     = length(aws_nat_gateway.this) == 1 && length(aws_route.private_nat) == 2
    error_message = "Default should share one NAT gateway across both private subnets."
  }

  assert {
    condition     = jsondecode(aws_ecs_task_definition.app.container_definitions)[0].image == "123456789012.dkr.ecr.us-east-1.amazonaws.com/flask-docker-app:0123abc"
    error_message = "Task definition must deploy the image_tag that CI passes in."
  }

  assert {
    condition     = aws_ecs_service.app.network_configuration[0].assign_public_ip == false
    error_message = "Tasks must run in private subnets without public IPs."
  }

  assert {
    condition     = aws_lb_listener.http.default_action[0].type == "forward" && length(aws_lb_listener.https) == 0
    error_message = "Without a certificate the ALB should serve plain HTTP."
  }

  assert {
    condition     = output.alb_url == "http://flask-hello-world.elb.example.com"
    error_message = "alb_url should use http without a certificate."
  }
}

run "https_enabled" {
  command = plan

  variables {
    certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/example"
  }

  assert {
    condition     = length(aws_lb_listener.https) == 1 && aws_lb_listener.http.default_action[0].type == "redirect"
    error_message = "With a certificate, HTTP must redirect to the HTTPS listener."
  }

  assert {
    condition     = length(aws_vpc_security_group_ingress_rule.alb_https) == 1
    error_message = "Port 443 must be opened when HTTPS is enabled."
  }

  assert {
    condition     = output.alb_url == "https://flask-hello-world.elb.example.com"
    error_message = "alb_url should use https when a certificate is set."
  }
}

run "nat_per_az" {
  command = plan

  variables {
    single_nat_gateway = false
  }

  assert {
    condition     = length(aws_nat_gateway.this) == 2 && length(aws_eip.nat) == 2
    error_message = "single_nat_gateway = false should create one NAT gateway per AZ."
  }
}
