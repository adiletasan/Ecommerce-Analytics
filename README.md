# Ecommerce-Analytics 
Astana E-Commerce Analytics

Astana E-Commerce is a growing online marketplace that connects customers with a wide range of products, including electronics, fashion, home appliances, and more. With thousands of daily transactions, the company generates valuable data about customer behavior, product performance, and sales trends.

This project aims to analyze and visualize e-commerce sales data to support better decision-making in areas such as marketing, logistics, and product management.

The Astana E-Commerce Analytics Project demonstrates how structured transaction data can be used to answer key business questions.

Key analytics include:

Total sales revenue by region and category.

Top 10 best-selling products.

Customer lifetime value (CLV).

Monthly/seasonal sales trends.

Average order value (AOV) per customer.

Seller performance (orders, ratings, revenue).

Payment methods distribution.

Refunds and cancellation rates.

New vs returning customers.

Logistics performance (delivery time & delays).

The project will evolve step by step throughout the trimester. Each assignment will add new functionality — from database setup → SQL queries → Python integration → visualization dashboards.

🖼️ Screenshot

(Temporary placeholder — will be updated with ER diagram or analytics dashboard later)



⚙️ Step-by-Step Instructions

1️⃣ Setup Database

Install MySQL or PostgreSQL.

Create a new database:

CREATE DATABASE ecommerce_db;

Import the dataset (CSV/SQL dump provided in /data folder):

mysql -u root -p ecommerce_db < data_import.sql

2️⃣ Run Python Script

Clone this repository:

git clone https://github.com/your-username/ecommerce-analytics.git
cd ecommerce-analytics


Install dependencies:

pip install -r requirements.txt


Run the script:

python main.py


(The script will connect to the database, run SQL queries, and display results in the terminal.)

3️⃣ Launch Apache Superset (Later in Project)

Start Superset server:

superset run -p 8088 --with-threads --reload --debugger


Open browser → http://localhost:8088

Connect database → Build dashboards.


🛠️ Tools & Resources

Database: MySQL / PostgreSQL

Programming Language: Python 3.11+

Libraries: Pandas, SQLAlchemy, mysql-connector-python / psycopg2

Visualization: Apache Superset

Version Control: GitHub

Diagram Tool: dbdiagram.io / Draw.io for ER diagrams

Dataset Source: Kaggle Open E-Commerce Dataset (Orders, Customers, Products, Sellers, Payments)
