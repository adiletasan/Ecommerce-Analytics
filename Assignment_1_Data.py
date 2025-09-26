#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-commerce Analytics Script
Connects to adilet_ds database and executes analytical queries
Author: Student
Date: 2025
"""
import os
import warnings
import mysql.connector as mysql
from datetime import datetime

# Suppress getpass warnings
warnings.filterwarnings("ignore", category=UserWarning, module="getpass")

def get_database_connection():
    """Get database connection to adilet_ds"""
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'database': 'adilet_ds'
    }
    
    # Get password
    password = os.getenv('MYSQL_PASSWORD')
    if not password:
        import getpass
        password = getpass.getpass("MySQL password: ")
    
    config['password'] = password
    
    try:
        connection = mysql.connect(**config)
        print(f"✅ Connected to database '{config['database']}'")
        return connection
    except mysql.Error as e:
        print(f"❌ Connection failed: {e}")
        return None

def execute_query(connection, query_name, sql_query, limit_rows=None):
    """Execute query and display results in a formatted way"""
    print(f"\n{'='*80}")
    print(f"📊 {query_name}")
    print('='*80)
    print(f"Query: {sql_query.strip()[:100]}{'...' if len(sql_query.strip()) > 100 else ''}")
    print("-" * 80)
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        if not results:
            print("❌ No results found.")
            return
        
        # Limit results if specified
        display_results = results[:limit_rows] if limit_rows else results
        
        # Calculate column widths for better formatting
        col_widths = {}
        for col in columns:
            col_widths[col] = max(len(str(col)), 10)
        
        for row in display_results[:5]:  # Check first 5 rows for width calculation
            for i, val in enumerate(row):
                col = columns[i]
                val_len = len(str(val)) if val is not None else 4
                col_widths[col] = max(col_widths[col], min(val_len, 20))
        
        # Print headers
        header = " | ".join(f"{col:>{col_widths[col]}}" for col in columns)
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in display_results:
            row_str = " | ".join(
                f"{str(val) if val is not None else 'NULL':>{col_widths[columns[i]]}}"
                for i, val in enumerate(row)
            )
            print(row_str)
        
        # Summary
        if limit_rows and len(results) > limit_rows:
            print(f"\n📋 Showing {len(display_results)} of {len(results)} rows")
        else:
            print(f"\n📋 Total rows: {len(results)}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Query failed: {e}")

def main():
    """Main function - executes analytical queries"""
    print("🚀 E-COMMERCE ANALYTICS DASHBOARD")
    print("=" * 60)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🗄️  Database: adilet_ds (Brazilian E-commerce Dataset)")
    print("=" * 60)
    
    conn = get_database_connection()
    if not conn:
        return
    
    # Define analytical queries to execute
    analytical_queries = [
        {
            "name": "1. Payment Method Performance Analysis",
            "sql": """
            SELECT 
                payment_type,
                COUNT(*) as total_transactions,
                ROUND(AVG(payment_value), 2) as avg_transaction_value,
                ROUND(SUM(payment_value), 2) as total_revenue,
                ROUND(SUM(payment_value) * 100.0 / (SELECT SUM(payment_value) FROM olist_order_payments_dataset), 2) as revenue_percentage
            FROM olist_order_payments_dataset 
            GROUP BY payment_type 
            ORDER BY total_revenue DESC;
            """,
            "limit": 10
        },
        
        {
            "name": "2. Customer Geographic Distribution", 
            "sql": """
            SELECT 
                customer_state,
                COUNT(*) as customer_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM olist_customers_dataset), 2) as percentage
            FROM olist_customers_dataset 
            GROUP BY customer_state 
            ORDER BY customer_count DESC;
            """,
            "limit": 15
        },
        
        {
            "name": "3. Top Product Categories",
            "sql": """
            SELECT 
                product_category_name,
                COUNT(*) as product_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM olist_products_dataset WHERE product_category_name IS NOT NULL), 2) as category_percentage
            FROM olist_products_dataset 
            WHERE product_category_name IS NOT NULL
            GROUP BY product_category_name 
            ORDER BY product_count DESC 
            LIMIT 10;
            """,
            "limit": 10
        },
        
        {
            "name": "4. Payment Installment Analysis",
            "sql": """
            SELECT 
                payment_installments,
                COUNT(*) as transaction_count,
                ROUND(AVG(payment_value), 2) as avg_value_per_installment_plan,
                ROUND(SUM(payment_value), 2) as total_value
            FROM olist_order_payments_dataset 
            WHERE payment_installments IS NOT NULL AND payment_installments <= 24
            GROUP BY payment_installments 
            ORDER BY payment_installments;
            """,
            "limit": 15
        },
        
        {
            "name": "5. Payment Value Distribution Analysis",
            "sql": """
            SELECT 
                CASE 
                    WHEN payment_value < 50 THEN 'Low (< R$50)'
                    WHEN payment_value < 200 THEN 'Medium (R$50-200)'
                    WHEN payment_value < 500 THEN 'High (R$200-500)'
                    ELSE 'Very High (> R$500)'
                END as payment_range,
                COUNT(*) as transaction_count,
                ROUND(AVG(payment_value), 2) as avg_value_in_range,
                ROUND(SUM(payment_value), 2) as total_value_in_range
            FROM olist_order_payments_dataset 
            GROUP BY 
                CASE 
                    WHEN payment_value < 50 THEN 'Low (< R$50)'
                    WHEN payment_value < 200 THEN 'Medium (R$50-200)'
                    WHEN payment_value < 500 THEN 'High (R$200-500)'
                    ELSE 'Very High (> R$500)'
                END
            ORDER BY avg_value_in_range;
            """,
            "limit": None
        },
        
        {
            "name": "6. Top Customer Cities",
            "sql": """
            SELECT 
                customer_city,
                customer_state,
                COUNT(*) as customer_count
            FROM olist_customers_dataset 
            GROUP BY customer_city, customer_state 
            ORDER BY customer_count DESC 
            LIMIT 15;
            """,
            "limit": 15
        },
        
        {
            "name": "7. Geographic Coverage by State",
            "sql": """
            SELECT 
                geolocation_state,
                COUNT(DISTINCT geolocation_zip_code_prefix) as unique_zip_codes,
                COUNT(*) as total_geolocation_records
            FROM olist_geolocation_dataset 
            GROUP BY geolocation_state 
            ORDER BY unique_zip_codes DESC
            LIMIT 15;
            """,
            "limit": 15
        },

        {
            "name": "8. Product Content Analysis",
            "sql": """
            SELECT 
                product_category_name,
                COUNT(*) as product_count,
                ROUND(AVG(product_name_length), 1) as avg_name_length,
                ROUND(AVG(product_description_length), 1) as avg_description_length,
                ROUND(AVG(product_photos_qty), 1) as avg_photos_qty
            FROM olist_products_dataset 
            WHERE product_category_name IS NOT NULL
            GROUP BY product_category_name 
            HAVING COUNT(*) >= 10
            ORDER BY avg_description_length DESC 
            LIMIT 10;
            """,
            "limit": 10
        },

        {
            "name": "9. Seller Geographic Distribution",
            "sql": """
            SELECT 
                seller_state,
                COUNT(DISTINCT seller_id) as unique_sellers
            FROM olist_sellers_dataset 
            GROUP BY seller_state 
            ORDER BY unique_sellers DESC
            LIMIT 15;
            """,
            "limit": 15
        }
    ]
    
    # Execute basic verification queries first
    print("\n🔍 BASIC DATA VERIFICATION")
    print("=" * 40)
    
    basic_queries = [
        {
            "name": "Database Tables Overview",
            "sql": """
            SELECT 
                table_name,
                table_rows,
                ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb
            FROM information_schema.tables 
            WHERE table_schema = 'adilet_ds' 
            ORDER BY table_rows DESC;
            """,
            "limit": None
        },
        
        {
            "name": "Sample Payment Data",
            "sql": "SELECT * FROM olist_order_payments_dataset LIMIT 5;",
            "limit": None
        }
    ]
    
    # Execute basic queries
    for query in basic_queries:
        execute_query(conn, query["name"], query["sql"], query.get("limit"))
    
    # Execute analytical queries
    print(f"\n🎯 ANALYTICAL INSIGHTS")
    print("=" * 40)
    
    for query in analytical_queries:
        execute_query(conn, query["name"], query["sql"], query.get("limit"))
    
    # Data quality checks
    print(f"\n🔍 DATA QUALITY CHECKS")
    print("=" * 40)
    
    quality_checks = [
        {
            "name": "NULL Values Check",
            "sql": """
            SELECT 
                'customers' as table_name,
                COUNT(*) as total_rows,
                SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_customer_ids,
                SUM(CASE WHEN customer_state IS NULL THEN 1 ELSE 0 END) as null_states
            FROM olist_customers_dataset
            
            UNION ALL
            
            SELECT 
                'payments' as table_name,
                COUNT(*) as total_rows,
                SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_order_ids,
                SUM(CASE WHEN payment_value IS NULL THEN 1 ELSE 0 END) as null_payment_values
            FROM olist_order_payments_dataset;
            """,
            "limit": None
        }
    ]
    
    for check in quality_checks:
        execute_query(conn, check["name"], check["sql"], check.get("limit"))
    
    conn.close()
    
    print(f"\n{'='*80}")
    print("✅ ANALYSIS COMPLETE!")
    print("📊 Summary:")
    print(f"   • Executed {len(basic_queries) + len(analytical_queries) + len(quality_checks)} queries")
    print("   • Analyzed payment methods, customer distribution, and product categories")
    print("   • Performed data quality checks")
    print("   • Results displayed in formatted tables")
    print("=" * 80)

if __name__ == "__main__":
    main()
