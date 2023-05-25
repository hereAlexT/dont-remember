resource "aws_lb" "dont-remember" {
  name               = "dont-remember"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.main.id]
  subnets            = data.aws_subnets.private.ids
}


resource "aws_lb_target_group" "users" {
  name        = "users"
  port        = 8888
  protocol    = "HTTP"
  vpc_id      = aws_security_group.main.vpc_id
  target_type = "ip"

  health_check {
    path     = "/api/v1/users/health"
    port     = "8888"
    protocol = "HTTP"

    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 30
    interval            = 60
  }
  depends_on = [aws_lb.dont-remember]
}
resource "aws_lb_target_group" "words" {
  name        = "words"
  port        = "8889"
  protocol    = "HTTP"
  vpc_id      = aws_security_group.main.vpc_id
  target_type = "ip"

  health_check {
    path     = "/api/v1/words/health"
    port     = "8889"
    protocol = "HTTP"

    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 30
    interval            = 60
  }
  depends_on = [aws_lb.dont-remember]
}


resource "aws_lb_listener" "dont-remember" {
  load_balancer_arn = aws_lb.dont-remember.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "Loadbalancer: Not Found"
      status_code  = "404"
    }
  }

  depends_on = [
    aws_lb_target_group.users,
    aws_lb_target_group.words,
  ]
}

resource "aws_lb_listener_rule" "users" {
  listener_arn = aws_lb_listener.dont-remember.arn
  priority     = 100

  condition {
    path_pattern {
      values = [
        "/api/v1/users/*",
        "/api/v1/users"
      ]
    }
  }
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.users.arn
  }
}

resource "aws_lb_listener_rule" "words" {
  listener_arn = aws_lb_listener.dont-remember.arn
  priority     = 200

  condition {
    path_pattern {
      values = [
        "/api/v1/words/*",
        "/api/v1/words"
      ]
    }
  }
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.words.arn
  }
}
