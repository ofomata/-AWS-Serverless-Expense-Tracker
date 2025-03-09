import json
import boto3
import uuid
import os
import logging
from decimal import Decimal
from datetime import datetime

# AWS Clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Get table name from environment variable (for flexibility)
TABLE_NAME = os.getenv("DYNAMODB_TABLE", "Expenses")
table = dynamodb.Table(TABLE_NAME)

# Get SNS Topic ARN from environment variable
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_short_id(length=4):
    """Generate a short, unique ID of the specified length."""
    return uuid.uuid4().hex[:length]  # Get the first `length` characters of the UUID

def send_alert(amount):
    """Send an SNS alert if expense exceeds the threshold."""
    if SNS_TOPIC_ARN and amount > 500:
        logger.info(f"Sending SNS alert for high expense: ${amount}")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"🚨 High Expense Alert! You just recorded an expense of ${amount}.",
            Subject="Expense Alert"
        )
    else:
        logger.info("Expense below threshold. No SNS alert sent.")

def lambda_handler(event, context):
    logger.info("Lambda function triggered for expense logging.")

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        if "amount" not in body or "description" not in body:
            logger.error("Missing required fields: 'amount' or 'description'")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields: 'amount' and 'description'"})
            }

        # Convert amount to Decimal (Fixes DynamoDB float issue)
        amount = Decimal(str(body["amount"]))
        description = body["description"]

        # Generate unique expense ID
        expense_id = generate_short_id(4)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"Logging expense - ID: {expense_id}, Amount: ${amount}, Description: {description}")

        # Store data in DynamoDB
        table.put_item(
            Item={
                "expenseId": expense_id,
                "amount": amount,
                "description": description,
                "date": timestamp
            }
        )

        # Send SNS alert if needed
        send_alert(amount)

        logger.info(f"Expense logged successfully with ID: {expense_id}")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "Expense logged successfully", "expenseId": expense_id})
        }

    except Exception as e:
        logger.error(f"Error logging expense: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }
