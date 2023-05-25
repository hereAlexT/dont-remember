resource "aws_ecs_service" "words" {
  name            = "words"
  cluster         = aws_ecs_cluster.dont-remember.id
  task_definition = aws_ecs_task_definition.words.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.words.arn
    container_name = "words"
    container_port = "8889"
  }
  depends_on = [aws_lb_listener.dont-remember]
}

resource "aws_ecs_service" "users" {
  name            = "users"
  cluster         = aws_ecs_cluster.dont-remember.id
  task_definition = aws_ecs_task_definition.users.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.users.arn
    container_name = "users"
    container_port = "8888"
  }
  depends_on = [aws_lb_listener.dont-remember]
}

