provider "aws" {
  region = var.region
}

## Account info:
# Get aws account id
data "aws_caller_identity" "current" {}

# Get availability zones
data "aws_availability_zones" "available" {}

# Get VPC ID
data "aws_vpc" "available" {
  id = var.vpc_id
}

# Get VPC subnets
data "aws_subnet" "available" {
  count             = 2
  vpc_id            = data.aws_vpc.available.id
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

# Get CloudFormation stack to find provisioned resources in it
data "aws_cloudformation_stack" "account_cf" {
  name = var.aws_account_code
}

data "aws_security_group" "sg_default" {
  filter {
    name   = "group-name"
    values = ["default"]
  }

  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.available.id]
  }
}

data "aws_security_group" "sg_cache_inbound" {
  filter {
    name   = "group-name"
    values = ["*redis_inbound*"]
  }
}


data "aws_security_group" "sg_cache_outbound" {
  filter {
    name   = "group-name"
    values = ["*redis_outbound*"]
  }
}

module "redis-redirect-base" {
  source = "../../modules/base/"

  environment = var.environment
  region      = var.region

  account_id = data.aws_caller_identity.current.account_id
  vpc_id     = data.aws_vpc.available.id
  subnets    = data.aws_subnet.available.*.id

  target_bucket = data.aws_cloudformation_stack.account_cf.outputs["LogsBucket"]
}

module "redis-redirect-redis" {
  source = "../../modules/redis/"

  namespace   = var.namespace
  region      = var.region
  subnets     = data.aws_subnet.available.*.id
  account_id  = data.aws_caller_identity.current.account_id
  environment = var.environment

  num_node_groups = "1"
  redis_id = "${var.namespace}-redis"

  security_groups = [
    data.aws_security_group.sg_default.id,
    data.aws_security_group.sg_cache_inbound.id,
    data.aws_security_group.sg_cache_outbound.id
  ]
}
