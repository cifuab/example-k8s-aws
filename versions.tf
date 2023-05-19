terraform {
  required_version = ">= 1.0.0"
  backend "s3" {
    encrypt        = true
    bucket         = "docplan"
    key            = "test/eu-north-1.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "terraform-state-lock-dynamo"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.72"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.10"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.4.1"
    }
  }

  # ##  Used for end-to-end testing on project; update to suit your needs
  # backend "s3" {
  # }
}
