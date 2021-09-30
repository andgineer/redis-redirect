resource "aws_elasticache_subnet_group" "default" {
  name       = "${var.namespace}-cache-subnet"
  subnet_ids = var.subnets
}

resource "aws_elasticache_replication_group" "default" {
  replication_group_id          = "${var.redis_id}"
  replication_group_description = "Redis for redis-redirect"

  //  https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html
  node_type            = "cache.m4.large"

  port                 = 6379

  // for daily backup of the cluster state. 0 for no backup
  snapshot_retention_limit = 0
  snapshot_window          = "00:00-05:00"

  subnet_group_name = aws_elasticache_subnet_group.default.name

  automatic_failover_enabled = true

  security_group_ids = var.security_groups

  cluster_mode {
    replicas_per_node_group = 1
    num_node_groups         = "${var.num_node_groups}"
  }
}
