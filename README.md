# AWS Serverless Expense Tracker

## **Project Overview**

This project is a **serverless expense tracking system** that leverages AWS services to store, process, and back up expense records. Users can log expenses, generate reports, and ensure data persistence with automated backups.

## **Architecture**

The system is divided into multiple components, each handling a specific function. Below is an overview of the architecture:

```
project-folder/
│── lambdas/             # AWS Lambda functions (Python)
│── api-gateway/         # API Gateway configurations (Swagger/OpenAPI)
│── database/            # SQL script for RDS database setup
│── screenshots/         # screenshot folder with images
│── frontend/            # Frontend files (HTML, CSS, JS, stored in S3)
│── README.md            # Project documentation
```

### **Key AWS Services Used**

- **Amazon S3** – Hosts the static frontend files and Stores monthly expense reports in CSV format.
- **API Gateway** – Exposes the backend APIs to handle user requests.
- **AWS Lambda** – Handles backend logic, API requests, automates backups and report and handles SNS.
- **DynamoDB** – Stores real-time expense data.
- **Amazon RDS(MySQL)** – Serves as a backup storage.
- **Amazon SNS** – Sends emails to user when expenses records above $500.
- **IAM** – Ensures security and access control.
- **CloudWatch** – Monitors and logs activities for debugging.
- **Amazon EventBridge** - Automates backup and report generation.

## **Features**

✅ **Expense Logging** → Users add expenses via the web interface and is processed by the api.
✅ **Monthly Reports** → AWS Lambda generates and stores CSV reports in S3.
✅ **Automated Backups** → DynamoDB data is periodically backed up to RDS.
✅ **EventBridge Automation** → Handles daily backups and monthly reports.
✅ **CloudWatch Monitoring** → Tracks API and Lambda performance.

---

## **Deployment Instructions**

### **1. Deploying the Frontend (Amazon S3)**

1. Upload the frontend/ files to an Amazon S3 bucket.
2. Enable static website hosting in the S3 bucket settings.
3. Set the bucket policy to allow public read access.
4. Note the website URL from the S3 console for frontend access.

**Bucket Policy**
{
"Version": "2012-10-17",
"Statement": [
{
"Sid": "PublicReadGetObject",
"Effect": "Allow",
"Principal": "*",
"Action": "s3:GetObject",
"Resource": "arn:aws:s3:::your-bucket-name/*"
}
]
}

### **2. Setting Up API Gateway**

1. Navigate to **API Gateway** in the AWS Console.
2. Create a new **REST API** and import the Swagger file from `api-gateway/`.
3. Deploy the API and note the generated URL.
4. Enable CORS for the API endpoint.

### **3. Deploying Lambda Functions**

1. Zip the `lambdas/` folder containing all Lambda function scripts.
2. Navigate to AWS Lambda and create three separate Lambda functions:
   - logExpense (handles expense logging and SNS notifications)
   - generateReport (generates monthly reports and uploads them to S3)
   - backupToRDS (backs up expenses from DynamoDB to RDS)
3. Upload the ZIP files for each function in **AWS Lambda**.
4. Attach necessary **IAM roles** with permissions for:
   DynamoDB (read/write access)
   S3 (upload reports)
   RDS (database connection)
   SNS (send alerts for high expenses)
5. Deploy Dependencies for Lambda (pymysql for RDS).

   - Create a ZIP file containing the pymysql package.
   - Run the following commands in your terminal on your local computer

     # 1. Create a directory for the package

     mkdir python

     # 2. Install pymysql into this directory

     pip install pymysql -t python/

     # 3. Zip the directory (this will create python.zip)

     zip -r pymysql-layer.zip python/

   - Upload pymysql-layer.zip as a Lambda Layer in AWS.
   - Attach this layer only to the backupToRDS Lambda function (since it's the only one using RDS).

### **4. Configuring DynamoDB & RDS**

1. Navigate to **AWS DynamoDB** and create a table named **Expenses** with:
   - **Primary Key**: expenseId(String)
2. Navigate to **Amazon RDS** and create a MySQL database instance.
3. Run the SQL script from `database/` to create the **expenses table**.
4. Note down the RDS endpoint for Lambda integration.

### **5. Setting Up Expense Reports (Amazon S3 & Glacier Storage)**

1. Create an **S3 bucket** named **expenses-tracker-reports**.
2. Enable Glacier Storage for cost efficiency:
   - Go to the **Management** tab in the S3 bucket settings.
   - Create a **Lifecycle Rule** to move reports to **Glacier Flexible Retrieval** after 90 days.
   - Configure the rule as follows:
     - Transition to Glacier Flexible Retrieval: After 90 days.
     - Expiration (optional): Delete objects after a specific period if needed.
3. Ensure the bucket policy allows Lambda to upload reports.
4. The **generateReport Lambda** will automatically upload reports to this bucket.

### **6. Configuring Notifications (SNS)**

1. Navigate to Amazon SNS and create a new topic for expense alerts.
2. Subscribe users to receive alerts when high expenses are logged.
3. Update the SNS topic ARN in the Lambda function environment variables.

### **7. Enabling Monitoring (CloudWatch)**

1. Enable **Amazon CloudWatch Logs** for all Lambda functions.
2. Create **CloudWatch Alarms** to monitor system health and trigger notifications if errors occur.

---

## **How Everything Connects**

- The frontend (S3) interacts with API Gateway, which triggers Lambda functions.
- Lambda functions process expenses, storing data in DynamoDB and backing it up in RDS.
- S3 stores expense reports with Glacier Instant Retrieval for long-term access.
- SNS sends alerts for high expenses, notifying subscribed users.
- CloudWatch provide real-time monitoring and logging.

---

## **Future Improvements**

🔹 **User Authentication & Security** – Implement AWS Cognito for secure login and role-based access.
🔹 **Expense Categorization & Budgeting** – Allow users to categorize expenses and set budget limits.
🔹 **AI-Powered Insights** – Use machine learning to analyze spending patterns and provide financial recommendations.
🔹 **Receipt Upload & Auto-Processing** – Enable users to upload receipts to S3 and extract data using Amazon Textract.

---

## **Conclusion**

The **Serverless Expense Tracker** is a fully automated, scalable, and cost-efficient solution for tracking expenses. Built with **AWS Lambda, DynamoDB, S3, API Gateway, and RDS,** it ensures seamless data storage, reporting, and backups. With **SNS alerts for high expenses, automated monthly reports stored in S3 Glacier,** and **daily backups to RDS,** the system enhances financial management while minimizing infrastructure costs.

Future improvements, such as **AI-driven insights and receipt scanning,** will further enhance its functionality. This project showcases the power of **serverless architecture** in building efficient, event-driven applications.

---

### **Need Help?**

If you encounter any issues, feel free to create a GitHub issue or contact me. 😊
