locals {
  cluster_name = aws_ecs_cluster.dont-remember.name

  microservices = {
    "user" : {
      name : "user",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.users.name}",
      resource_label : "${aws_lb.dont-remember.arn_suffix}/${aws_lb_target_group.users.arn_suffix}",
    },
    "concert" : {
      name : "concert",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.words.name}",
      resource_label : "${aws_lb.dont-remember.arn_suffix}/${aws_lb_target_group.words.arn_suffix}",
    },
  }
  target_connection_per_task = 300
}


resource "aws_appautoscaling_target" "main" {
  for_each = local.microservices

  max_capacity       = 500
  min_capacity       = 2
  resource_id        = each.value.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "dont-remember" {
  for_each = local.microservices

  name               = "${each.value.name}-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace
  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 24
    scale_in_cooldown  = 120
    scale_out_cooldown = 120
  }
}
