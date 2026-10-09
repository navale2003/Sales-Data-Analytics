import sqlite3
import pandas as pd

# ============================================================
# CONNECT TO DATABASE
# ============================================================

db_path = "ecommerce.db"

conn = sqlite3.connect(db_path)

print("Connected to SQLite database successfully!")


# ============================================================
# FUNCTION TO RUN SQL QUERY
# ============================================================

def run_query(query, title):

    print("\n")
    print("=" * 70)
    print(title)
    print("=" * 70)

    result = pd.read_sql_query(query, conn)

    print(result.to_string(index=False))

    return result


# ============================================================
# 1. BASIC BUSINESS KPIs
# ============================================================

query = """
SELECT
    COUNT(*) AS total_orders,
    SUM(quantity * unit_price) AS total_revenue,
    AVG(quantity * unit_price) AS average_order_value
FROM orders;
"""

run_query(query, "1. BASIC BUSINESS KPIs")


# ============================================================
# 2. ORDER STATUS ANALYSIS
# ============================================================

query = """
SELECT
    order_status,
    COUNT(*) AS total_orders,
    SUM(quantity * unit_price) AS revenue
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""

run_query(query, "2. ORDER STATUS ANALYSIS")


# ============================================================
# 3. MONTHLY REVENUE
# ============================================================

query = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS orders,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY month
ORDER BY month;
"""

run_query(query, "3. MONTHLY REVENUE")


# ============================================================
# 4. CATEGORY PERFORMANCE
# ============================================================

query = """
SELECT
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS quantity_sold,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
"""

run_query(query, "4. CATEGORY PERFORMANCE")


# ============================================================
# 5. TOP 10 PRODUCTS
# ============================================================

query = """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS quantity_sold,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;
"""

run_query(query, "5. TOP 10 PRODUCTS BY REVENUE")


# ============================================================
# 6. TOP 10 CUSTOMERS
# ============================================================

query = """
SELECT
    c.customer_id,
    c.name,
    c.state,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.state
ORDER BY revenue DESC
LIMIT 10;
"""

run_query(query, "6. TOP 10 CUSTOMERS BY REVENUE")


# ============================================================
# 7. STATE PERFORMANCE
# ============================================================

query = """
SELECT
    c.state,
    COUNT(o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.state
ORDER BY revenue DESC;
"""

run_query(query, "7. STATE-WISE PERFORMANCE")


# ============================================================
# 8. PAYMENT METHOD
# ============================================================

query = """
SELECT
    payment_method,
    COUNT(*) AS total_payments,
    COUNT(DISTINCT order_id) AS unique_orders
FROM payments
GROUP BY payment_method
ORDER BY total_payments DESC;
"""

run_query(query, "8. PAYMENT METHOD ANALYSIS")


# ============================================================
# 9. PAYMENT STATUS
# ============================================================

query = """
SELECT
    payment_status,
    COUNT(*) AS total_payments,
    COUNT(DISTINCT order_id) AS unique_orders
FROM payments
GROUP BY payment_status
ORDER BY total_payments DESC;
"""

run_query(query, "9. PAYMENT STATUS ANALYSIS")


# ============================================================
# 10. RETURN ANALYSIS
# ============================================================

query = """
SELECT
    return_reason,
    COUNT(*) AS total_returns
FROM returns
GROUP BY return_reason
ORDER BY total_returns DESC;
"""

run_query(query, "10. RETURN ANALYSIS")


# ============================================================
# 11. RETURN RATE
# ============================================================

query = """
SELECT
    COUNT(DISTINCT r.order_id) AS returned_orders,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(
        COUNT(DISTINCT r.order_id) * 100.0
        / COUNT(DISTINCT o.order_id),
        2
    ) AS return_rate_percentage
FROM orders o
LEFT JOIN returns r
    ON o.order_id = r.order_id;
"""

run_query(query, "11. OVERALL RETURN RATE")


# ============================================================
# 12. PROFIT BY CATEGORY
# ============================================================

query = """
SELECT
    p.category,

    ROUND(
        SUM(
            (o.quantity * o.unit_price)
            - (o.quantity * p.cost)
        ),
        2
    ) AS profit

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

GROUP BY p.category

ORDER BY profit DESC;
"""

run_query(query, "12. PROFIT BY CATEGORY")


# ============================================================
# 13. TOP PROFITABLE PRODUCTS
# ============================================================

query = """
SELECT
    p.product_id,
    p.product_name,
    p.category,

    ROUND(
        SUM(
            (o.quantity * o.unit_price)
            - (o.quantity * p.cost)
        ),
        2
    ) AS profit

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category

ORDER BY profit DESC

LIMIT 10;
"""

run_query(query, "13. TOP 10 PROFITABLE PRODUCTS")


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("\n")
print("=" * 70)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 70)