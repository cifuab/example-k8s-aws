# tflint-ignore: terraform_unused_declarations
variable "cluster_name" {
  description = "Name of cluster - used by Terratest for e2e test automation"
  type        = string
  default     = ""
}
# variable "region " {
#   description = "Aws region for deploy"
#   # type        = string
#   default     = "eu-north-1"
# }
variable "env" {
  description = "enviroment"
  type        = string
  default     = "test"
}
variable "vpc_cidr" {
  description = "CDIR space"
  type        = string
  default     = "10.0.0.0/16"
}
variable "tags" {
  description = "general tags"
  type        = map(any)
  default = {
    name       = "docpp"
    env        = "test"
    GithubRepo = "github.com/cifuab/example"
  }
}
  