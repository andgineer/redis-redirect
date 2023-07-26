variable "namespace" {
  type    = string
  default = "redis-redirect"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "aws_account_code" {
  type    = string
  default = "???"
}

variable "vpc_id" {
  type    = string
  default = "vpc-???"
}
