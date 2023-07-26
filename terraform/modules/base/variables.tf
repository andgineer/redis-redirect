# Main
variable "environment" {}
variable "region" {}
variable "subnets" { type = list(string) }
variable "vpc_id" {}
variable "account_id" {}

variable "target_bucket" {}
