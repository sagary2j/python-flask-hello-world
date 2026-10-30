resource "aws_dynamodb_table" "user_table" {
  name                        = var.dynamodb_table_name
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "username"
  deletion_protection_enabled = var.dynamodb_deletion_protection

  attribute {
    name = "username"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
