locals {
  rds_uri        = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.dont-remember.endpoint}"
  rds_endpoint   = aws_db_instance.dont-remember.endpoint
  words_endpoint = "http://${aws_lb.dont-remember.dns_name}/api/v1/words"
  users_endpoint = "http://${aws_lb.dont-remember.dns_name}/api/v1/users"
}
