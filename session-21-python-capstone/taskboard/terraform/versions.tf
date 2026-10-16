terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # Credentials come from the environment / `aws configure`, never from these files.
  default_tags {
    tags = {
      Project     = "taskboard"
      Environment = var.environment
      Session     = "21"
      ManagedBy   = "terraform"
    }
  }
}
