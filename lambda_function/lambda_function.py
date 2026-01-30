import os
import json
import boto3
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")
sns = boto3.client("sns")

INSTANCE_ID = os.environ.get("INSTANCE_ID", "")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")

def _publish(message: str, subject: str = "EC2 Restart Triggered"):
    if not SNS_TOPIC_ARN:
        logger.warning("SNS_TOPIC_ARN not set; skipping SNS publish.")
        return
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject[:100],
        Message=message
    )

def lambda_handler(event, context):
    """
    Expected trigger: Sumo alert via webhook / API Gateway (any JSON payload).
    Action: reboot the configured EC2 instance, log, and notify SNS.
    """
    if not INSTANCE_ID:
        raise ValueError("Missing env var INSTANCE_ID")

    now = datetime.now(timezone.utc).isoformat()
    logger.info("Received event: %s", json.dumps(event))

    try:
        # Reboot is a "restart" without changing instance ID (fast). Alternative: stop/start.
        ec2.reboot_instances(InstanceIds=[INSTANCE_ID])

        msg = (
            f"[{now}] Reboot requested for EC2 instance {INSTANCE_ID}.\n\n"
            f"Trigger payload (truncated): {json.dumps(event)[:2000]}"
        )
        logger.info(msg)
        _publish(msg, subject="EC2 reboot requested")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Reboot requested",
                "instance_id": INSTANCE_ID,
                "timestamp": now
            })
        }

    except Exception as e:
        err = f"[{now}] Failed to reboot {INSTANCE_ID}: {repr(e)}"
        logger.exception(err)
        _publish(err, subject="EC2 reboot FAILED")
        raise
