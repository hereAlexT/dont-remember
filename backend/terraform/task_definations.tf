locals {
  task_cpu    = 1024
  task_memory = 2048
}

resource "aws_ecs_task_definition" "words" {
  family                   = "words"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = local.task_cpu
  memory                   = local.task_memory
  execution_role_arn       = data.aws_iam_role.lab.arn
  task_role_arn            = data.aws_iam_role.lab.arn

  container_definitions = jsonencode([
    {
      name         = "words"
      image        = "${aws_ecr_repository.words.repository_url}:${var.image_version}"
      essential    = true
      cpu          = local.task_cpu
      memory       = local.task_memory
      portMappings = [
        {
          containerPort = 8889
          hostPort      = 8889
        }
      ]
      environment : [
        {
          name  = "SQLALCHEMY_DATABASE_URI"
          value = "${local.rds_uri}/dontremember"
        },
        {
          name  = "JWT_SECRET_KEY"
          value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDgzMDI5NywianRpI"
        },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options   = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "words"
        }
      }
    }
  ])

}


resource "aws_ecs_task_definition" "users" {
  family                   = "users"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = local.task_cpu
  memory                   = local.task_memory
  execution_role_arn       = data.aws_iam_role.lab.arn
  task_role_arn            = data.aws_iam_role.lab.arn

  container_definitions = jsonencode([
    {
      name         = "users"
      image        = "${aws_ecr_repository.users.repository_url}:${var.image_version}"
      essential    = true
      cpu          = local.task_cpu
      memory       = local.task_memory
      portMappings = [
        {
          containerPort = 8888
          hostPort      = 8888
        }
      ]
      environment : [
        {
          name  = "SQLALCHEMY_DATABASE_URI"
          value = "${local.rds_uri}/dontremember"
        },
        {
          name  = "JWT_SECRET_KEY"
          value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDgzMDI5NywianRpI"
        },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options   = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "users"
        }
      }
    }
  ])
}