import boto3
import json
import csv
import io
import logging
from datetime import datetime

# Initialize AWS services
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Expenses')

# Define S3 bucket name
BUCKET_NAME = "expenses-tracker-reports"

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Lambda function triggered for expense report generation.")

    try:
        # Get the month (defaults to current month)
        month = event.get('month', datetime.now().strftime("%Y-%m"))
        logger.info(f"Generating report for month: {month}")

        # Scan DynamoDB for all expenses
        response = table.scan()
        expenses = response.get('Items', [])
        logger.info(f"Retrieved {len(expenses)} expenses from DynamoDB.")

        if not expenses:
            logger.warning("No expenses found for the report.")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No expenses found for the month.", "file": None})
            }

        # Create a CSV buffer
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)

        # Write CSV headers
        writer.writerow(["Expense ID", "Amount", "Date", "Description"])

        # Write expense data
        for expense in expenses:
            writer.writerow([
                expense.get("expenseId", "N/A"), 
                expense.get("amount", 0), 
                expense.get("date", "N/A"), 
                expense.get("description", "No Description")
            ])

        # Generate filename
        filename = f"{month}-expense-report.csv"

        # Upload the CSV file to S3 with Glacier Instant Retrieval
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=csv_buffer.getvalue(),
            StorageClass="GLACIER_IR"  # Set to Glacier Instant Retrieval
        )
        logger.info(f"Report successfully uploaded to S3: {filename}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Report generated and stored in Glacier Instant Retrieval", "file": filename})
        }

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

