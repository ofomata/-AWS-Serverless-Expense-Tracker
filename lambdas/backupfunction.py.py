import json
import boto3
import pymysql  # Uses the layer
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Expenses")  # Change to your actual DynamoDB table name

# RDS Connection (From Environment Variables)
DB_HOST = os.getenv("RDS_HOST")  # RDS Endpoint
DB_USER = os.getenv("RDS_USER")  # DB Username
DB_PASS = os.getenv("RDS_PASS")  # DB Password
DB_NAME = os.getenv("RDS_NAME")  # Database Name

def lambda_handler(event, context):
    logger.info("Lambda function triggered for DynamoDB to RDS backup.")

    try:
        # Connect to RDS
        conn = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conn.cursor()
        logger.info("Connected to RDS successfully.")

        # Retrieve expenses from DynamoDB
        response = table.scan()
        expenses = response.get('Items', [])
        logger.info(f"Retrieved {len(expenses)} expenses from DynamoDB.")

        # Insert into RDS (with Upsert to prevent duplicate error)
        for expense in expenses:
            cursor.execute("""
                INSERT INTO expenses (expense_id, amount, description, date) 
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                amount = VALUES(amount), 
                description = VALUES(description), 
                date = VALUES(date);
            """, (expense['expenseId'], expense['amount'], expense['description'], expense['date']))
        
        conn.commit()
        conn.close()
        logger.info("Backup to RDS completed successfully.")

        return {"statusCode": 200, "body": json.dumps({"message": "Backup successful!"})}

    except Exception as e:
        logger.error(f"Error occurred during backup: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
