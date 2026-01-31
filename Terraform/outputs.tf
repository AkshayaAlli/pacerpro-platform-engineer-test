output "ec2_instance_id" {
  value = aws_instance.demo.id
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.restart_ec2.function_name
}

