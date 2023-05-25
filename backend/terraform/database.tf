resource "aws_db_instance" "dont-remember" {
  allocated_storage      = 20
  max_allocated_storage  = 1000
  engine                 = "postgres"
  engine_version         = "14"
  instance_class         = "db.t4g.medium"
  db_name                = "dontremember"
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = aws_db_parameter_group.dont-remember.name
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.database.id]
  publicly_accessible    = true

  tags = {
    Name = "dont-remember"
  }
}

resource "null_resource" "init_db" {
  depends_on = [aws_db_instance.dont-remember]

  provisioner "local-exec" {
    command = "python3 ./database/init-db.py  ${aws_db_instance.dont-remember.endpoint} ${aws_db_instance.dont-remember.db_name} ${aws_db_instance.dont-remember.username} ${aws_db_instance.dont-remember.password}"
  }
}

resource "aws_db_parameter_group" "dont-remember" {
  name   = "dont-remember"
  family = "postgres14"

  parameter {
    name  = "idle_in_transaction_session_timeout"
    value = 60000
  }
  parameter {
    name  = "max_connections"
    value = 15000
    apply_method = "pending-reboot"
  }
}