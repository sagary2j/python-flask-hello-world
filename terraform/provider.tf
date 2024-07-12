terraform {
  backend "s3" {
    bucket  = "terrforms3-remote-backend"
    key     = "global/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}