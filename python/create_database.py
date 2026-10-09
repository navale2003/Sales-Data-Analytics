import sqlite3
import pandas as pd
import os


# -----------------------------
# Database connection
# -----------------------------

db_path = "ecommerce.db"

conn = sqlite3.connect(db_path)


# -----------------------------
# CSV files
# -----------------------------

files = {
    "customers": "data/raw/customers.csv",
    "products": "data/raw/products.csv",
    "orders": "data/raw/orders.csv",
    "payments": "data/raw/payments.csv",
    "returns": "data/raw/returns.csv"
}


# -----------------------------
# Load CSV files into SQLite
# -----------------------------

for table_name, file_path in files.items():

    print(f"\nLoading {table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} loaded successfully!")
    print("Rows:", len(df))


# -----------------------------
# Check tables
# -----------------------------

cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
""")

tables = cursor.fetchall()

print("\nTables in database:")

for table in tables:
    print("-", table[0])


# -----------------------------
# Close database
# -----------------------------

conn.close()

print("\nDatabase creation completed!")