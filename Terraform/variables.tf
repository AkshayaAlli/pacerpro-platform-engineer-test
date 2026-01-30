variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "alert_email" {
  type        = string
  description = "Email to subscribe to SNS topic (confirm subscription from inbox)."
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

# Use Amazon Linux 2023 x86_64 in many regions; you can override if needed.
variable "ami_id" {
  type        = string
  description = "AMI ID for EC2 instance."
}

variable "instance_name" {
  type    = string
  default = "sumo-alert-demo-ec2"
}

