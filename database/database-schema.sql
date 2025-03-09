-- Connect to the RDS instance
~ $ mysql --host=expense-tracker-db.cxa6gecsas3w.us-east-1.rds.amazonaws.com --user=admin --password test
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 64
Server version: 8.0.40 Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.


Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

-- After entering the password, create the table
CREATE TABLE expenses (
    expense_id VARCHAR(10) PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    date DATETIME NOT NULL
);


-- After Backup is done use this cocde to view table
MySQL [test]> SELECT * FROM expenses;

-- Backedup Table Data
+------------+------------+-----------------------------------+---------------------+
| expense_id | amount     | description                       | date                |
+------------+------------+-----------------------------------+---------------------+
| 7203       |    5000.00 | Promotion For New Product         | 2025-03-09 20:21:11 |
| 805f       | 1000000.00 | Capital Expense For Child Company | 2025-03-09 20:20:14 |
| 983f       |  500000.00 | Marketting for new product        | 2025-03-09 18:18:57 |
| abfb       |     500.00 | Miscellaneous                     | 2025-03-09 20:22:01 |
| b363       |    1000.00 | Staff Training and Recruitment    | 2025-03-09 20:20:50 |
| cdc9       |    5000.00 | Sales                             | 2025-03-09 20:52:59 |
| d711       |  200000.00 | New Product From China Supplier   | 2025-03-09 21:05:05 |
+------------+------------+-----------------------------------+---------------------+
7 rows in set (0.001 sec)