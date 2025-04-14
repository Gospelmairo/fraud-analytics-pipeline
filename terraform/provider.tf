terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "0.67.0"  # Pinned version known to work well
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


provider "aws" {
  region = var.aws_region
}

provider "snowflake" {
  username = var.snowflake_username
  password = var.snowflake_password
  account  = var.snowflake_account
  role     = "ACCOUNTADMIN"
  warehouse = "COMPUTE_WH"
}
