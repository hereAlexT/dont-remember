output "default_vpc_id" {
    value = data.aws_vpc.default.id
}


output "rds_endpoint" {
  value = aws_db_instance.dont-remember.endpoint
}

output "rds_username" {
  sensitive = true
  value = var.db_username
}

output "rds_password" {
  sensitive = true
  value = var.db_password
}

output "rds_uri" {
  sensitive = true
  value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.dont-remember.endpoint}/${aws_db_instance.dont-remember.db_name}"
}

output "users_url" {
  value = "http://${aws_lb.dont-remember.dns_name}/api/v1/users"
}

output "words_url" {
  value = "http://${aws_lb.dont-remember.dns_name}/api/v1/words"
}

output "api_url" {
  value = "http://${aws_lb.dont-remember.dns_name}/api/v1"
}