# Sumo Logic Alert → AWS Lambda → EC2 Restart + SNS Notification

## Overview
This repo contains:
- A Sumo Logic query to detect `/api/data` responses > 3 seconds.
- A Sumo Logic alert that triggers when > 5 such entries occur within 10 minutes.
- An AWS Lambda (Python) that restarts a specific EC2 instance and publishes an SNS notification.
- Terraform to deploy EC2 + SNS + Lambda + IAM.

## Repo Structure
- `sumo_logic_query.txt` – Sumo query
- `lambda_function/` – Python Lambda handler
- `terraform/` – Terraform IaC

## Part 1: Sumo Logic Query + Alert
1. Paste query from `sumo_logic_query.txt`
2. Create a Scheduled Search alert:
   - Time range: last 10 minutes
   - Frequency: 1–5 minutes
   - Trigger: when result count > 0

## Part 2: Lambda
Lambda reads:
- `INSTANCE_ID` (env var)
- `SNS_TOPIC_ARN` (env var)

Behavior:
- Calls `ec2.reboot_instances([INSTANCE_ID])`
- Logs to CloudWatch
- Publishes a message to SNS topic

## Part 3: Terraform Deploy
1. Go to `terraform/`
2. Run:
   ```bash
   terraform init
   terraform apply -var="alert_email=YOUR_EMAIL" -var="ami_id=YOUR_AMI_ID"
