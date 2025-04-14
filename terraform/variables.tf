variable "aws_region" {
  default = "us-east-1"
}

variable "snowflake_username" {}
variable "snowflake_password" {}
variable "snowflake_account" {}
variable "snowflake_role" {
  default = "ACCOUNTADMIN"
}

variable "snowflake_warehouse" {
  description = "COMPUTE_WH"
  type        = string
}
