## Main:
variable "namespace" {}
variable "environment" {}
variable "region" {}
variable "subnets" { type = list(string) }
variable "account_id" {}

## REDIS:
variable "num_node_groups" {}
variable "redis_id" {}
variable "security_groups" {}
