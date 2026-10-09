import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

customers = pd.read_csv(
    "data/cleaned/customers_cleaned.csv"
)

products = pd.read_csv(
    "data/cleaned/products_cleaned.csv"
)

orders = pd.read_csv(
    "data/cleaned/orders_cleaned.csv"
)

payments = pd.read_csv(
    "data/cleaned/payments_cleaned.csv"
)

returns = pd.read_csv(
    "data/cleaned/returns_cleaned.csv"
)

print("All cleaned datasets loaded successfully!")


# ============================================================
# 2. CONVERT DATE COLUMNS
# ============================================================

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

payments["payment_date"] = pd.to_datetime(
    payments["payment_date"]
)

returns["return_date"] = pd.to_datetime(
    returns["return_date"]
)


# ============================================================
# 3. CREATE REVENUE COLUMN
# ============================================================

orders["revenue"] = (
    orders["quantity"] *
    orders["unit_price"]
)


# ============================================================
# 4. CREATE DISCOUNT AMOUNT
# ============================================================

orders["discount_amount"] = (
    orders["revenue"] *
    orders["discount"] / 100
)


# ============================================================
# 5. CREATE NET REVENUE
# ============================================================

orders["net_revenue"] = (
    orders["revenue"] -
    orders["discount_amount"]
)


# ============================================================
# 6. BASIC BUSINESS KPIs
# ============================================================

print("\n")
print("============================================================")
print("                 BASIC BUSINESS KPIs")
print("============================================================")

total_customers = len(customers)

total_products = len(products)

total_orders = len(orders)

completed_orders = (
    orders["order_status"] == "Completed"
).sum()

cancelled_orders = (
    orders["order_status"] == "Cancelled"
).sum()

print("\nTotal Customers:", total_customers)
print("Total Products:", total_products)
print("Total Orders:", total_orders)
print("Completed Orders:", completed_orders)
print("Cancelled Orders:", cancelled_orders)


# ============================================================
# 7. REVENUE ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                    REVENUE ANALYSIS")
print("============================================================")

total_revenue = orders["revenue"].sum()

completed_revenue = orders[
    orders["order_status"] == "Completed"
]["revenue"].sum()

cancelled_revenue = orders[
    orders["order_status"] == "Cancelled"
]["revenue"].sum()

total_discount = orders["discount_amount"].sum()

total_net_revenue = orders["net_revenue"].sum()

print("\nTotal Revenue:", round(total_revenue, 2))

print(
    "Completed Order Revenue:",
    round(completed_revenue, 2)
)

print(
    "Cancelled Order Revenue:",
    round(cancelled_revenue, 2)
)

print(
    "Total Discount Amount:",
    round(total_discount, 2)
)

print(
    "Total Net Revenue:",
    round(total_net_revenue, 2)
)


# ============================================================
# 8. AVERAGE ORDER VALUE
# ============================================================

print("\n")
print("============================================================")
print("                 AVERAGE ORDER VALUE")
print("============================================================")

aov = (
    orders["revenue"].sum()
    / len(orders)
)

completed_orders_data = orders[
    orders["order_status"] == "Completed"
]

completed_aov = (
    completed_orders_data["revenue"].sum()
    / len(completed_orders_data)
)

print("\nOverall AOV:", round(aov, 2))

print(
    "Completed Order AOV:",
    round(completed_aov, 2)
)


# ============================================================
# 9. MONTHLY REVENUE
# ============================================================

print("\n")
print("============================================================")
print("                  MONTHLY REVENUE")
print("============================================================")

orders["month"] = orders["order_date"].dt.to_period("M")

monthly_revenue = (
    orders.groupby("month")["net_revenue"]
    .sum()
    .reset_index()
)

monthly_revenue["month"] = (
    monthly_revenue["month"].astype(str)
)

print("\nMonthly Revenue:")
print(monthly_revenue)


# ============================================================
# 10. CATEGORY PERFORMANCE
# ============================================================

print("\n")
print("============================================================")
print("                 CATEGORY PERFORMANCE")
print("============================================================")

category_performance = (
    orders
    .merge(
        products[["product_id", "category"]],
        on="product_id",
        how="left"
    )
    .groupby("category")
    .agg(
        orders=("order_id", "count"),
        quantity_sold=("quantity", "sum"),
        revenue=("net_revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\nCategory Performance:")
print(category_performance)


# ============================================================
# 11. PRODUCT PERFORMANCE
# ============================================================

print("\n")
print("============================================================")
print("                  PRODUCT PERFORMANCE")
print("============================================================")

product_performance = (
    orders
    .merge(
        products[
            ["product_id", "product_name", "category"]
        ],
        on="product_id",
        how="left"
    )
    .groupby(
        [
            "product_id",
            "product_name",
            "category"
        ]
    )
    .agg(
        orders=("order_id", "count"),
        quantity_sold=("quantity", "sum"),
        revenue=("net_revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\nTop 10 Products by Revenue:")
print(
    product_performance.head(10)
)


# ============================================================
# 12. STATE PERFORMANCE
# ============================================================

print("\n")
print("============================================================")
print("                   STATE PERFORMANCE")
print("============================================================")

state_performance = (
    orders
    .merge(
        customers[
            ["customer_id", "state"]
        ],
        on="customer_id",
        how="left"
    )
    .groupby("state")
    .agg(
        orders=("order_id", "count"),
        customers=("customer_id", "nunique"),
        revenue=("net_revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\nTop 10 States by Revenue:")
print(
    state_performance.head(10)
)


# ============================================================
# ============================================================
# 13. PAYMENT METHOD ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                PAYMENT METHOD ANALYSIS")
print("============================================================")


payment_analysis = (
    payments
    .groupby("payment_method")
    .agg(
        payments=("payment_id", "count"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)


# Add revenue by joining payment information with orders

payment_revenue = (
    payments[
        [
            "order_id",
            "payment_method"
        ]
    ]
    .merge(
        orders[
            [
                "order_id",
                "net_revenue"
            ]
        ],
        on="order_id",
        how="left"
    )
    .groupby("payment_method")
    .agg(
        revenue=("net_revenue", "sum")
    )
    .reset_index()
)


# Combine payment count and revenue

payment_analysis = payment_analysis.merge(
    payment_revenue,
    on="payment_method",
    how="left"
)


payment_analysis = payment_analysis.sort_values(
    "revenue",
    ascending=False
)


print("\nPayment Method Performance:")
print(payment_analysis)

# ============================================================
# 14. PAYMENT STATUS ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                 PAYMENT STATUS")
print("============================================================")

payment_status_analysis = (
    payments
    .groupby("payment_status")
    .agg(
        payments=("payment_id", "count"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)

print("\nPayment Status:")
print(payment_status_analysis)


# ============================================================
# 15. ORDER STATUS ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                  ORDER STATUS")
print("============================================================")

order_status_analysis = (
    orders
    .groupby("order_status")
    .agg(
        orders=("order_id", "count"),
        revenue=("revenue", "sum"),
        net_revenue=("net_revenue", "sum")
    )
    .reset_index()
)

print("\nOrder Status Analysis:")
print(order_status_analysis)


# ============================================================
# 16. CUSTOMER ORDER ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                 CUSTOMER ANALYSIS")
print("============================================================")

customer_analysis = (
    orders
    .groupby("customer_id")
    .agg(
        orders=("order_id", "count"),
        quantity=("quantity", "sum"),
        revenue=("net_revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\nTop 10 Customers by Revenue:")
print(
    customer_analysis.head(10)
)


# ============================================================
# 17. RETURN ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                   RETURN ANALYSIS")
print("============================================================")

total_returns = len(returns)

return_rate = (
    total_returns / total_orders
) * 100

print("\nTotal Returns:", total_returns)

print(
    "Return Rate:",
    round(return_rate, 2),
    "%"
)


# Return reasons

return_reasons = (
    returns["return_reason"]
    .value_counts()
    .reset_index()
)

return_reasons.columns = [
    "return_reason",
    "return_count"
]

print("\nReturn Reasons:")
print(return_reasons)


# ============================================================
# 18. DISCOUNT ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                  DISCOUNT ANALYSIS")
print("============================================================")

discount_analysis = (
    orders
    .groupby("discount")
    .agg(
        orders=("order_id", "count"),
        revenue=("revenue", "sum"),
        net_revenue=("net_revenue", "sum")
    )
    .reset_index()
    .sort_values("discount")
)

print("\nDiscount Analysis:")
print(discount_analysis)


# ============================================================
# 19. PROFIT ANALYSIS
# ============================================================

print("\n")
print("============================================================")
print("                   PROFIT ANALYSIS")
print("============================================================")

orders_with_products = orders.merge(
    products[
        [
            "product_id",
            "price",
            "cost"
        ]
    ],
    on="product_id",
    how="left"
)

orders_with_products["cost_amount"] = (
    orders_with_products["quantity"] *
    orders_with_products["cost"]
)

orders_with_products["profit"] = (
    orders_with_products["net_revenue"] -
    orders_with_products["cost_amount"]
)

orders_with_products["profit_margin"] = (
    orders_with_products["profit"] /
    orders_with_products["net_revenue"]
) * 100


total_profit = (
    orders_with_products["profit"].sum()
)

average_profit_margin = (
    orders_with_products["profit_margin"].mean()
)

print(
    "\nTotal Profit:",
    round(total_profit, 2)
)

print(
    "Average Profit Margin:",
    round(average_profit_margin, 2),
    "%"
)


# ============================================================
# 20. TOP PROFITABLE CATEGORIES
# ============================================================

category_profit = (
    orders_with_products
    .merge(
        products[
            ["product_id", "category"]
        ],
        on="product_id",
        how="left"
    )
    .groupby("category")
    .agg(
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
    .sort_values(
        "profit",
        ascending=False
    )
)

print("\nCategory Profitability:")
print(category_profit)


# ============================================================
# 21. BASIC VISUALIZATION - MONTHLY REVENUE
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["month"],
    monthly_revenue["net_revenue"],
    marker="o"
)

plt.title("Monthly Net Revenue")

plt.xlabel("Month")

plt.ylabel("Net Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 22. BASIC VISUALIZATION - CATEGORY REVENUE
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_performance["category"],
    category_performance["revenue"]
)

plt.title("Revenue by Product Category")

plt.xlabel("Category")

plt.ylabel("Net Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 23. BASIC VISUALIZATION - ORDER STATUS
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    order_status_analysis["order_status"],
    order_status_analysis["orders"]
)

plt.title("Orders by Status")

plt.xlabel("Order Status")

plt.ylabel("Number of Orders")

plt.tight_layout()

plt.show()


# ============================================================
# 24. SAVE EDA RESULTS
# ============================================================

monthly_revenue.to_csv(
    "data/cleaned/monthly_revenue.csv",
    index=False
)

category_performance.to_csv(
    "data/cleaned/category_performance.csv",
    index=False
)

product_performance.to_csv(
    "data/cleaned/product_performance.csv",
    index=False
)

state_performance.to_csv(
    "data/cleaned/state_performance.csv",
    index=False
)

payment_analysis.to_csv(
    "data/cleaned/payment_analysis.csv",
    index=False
)

customer_analysis.to_csv(
    "data/cleaned/customer_analysis.csv",
    index=False
)

return_reasons.to_csv(
    "data/cleaned/return_analysis.csv",
    index=False
)

category_profit.to_csv(
    "data/cleaned/category_profit.csv",
    index=False
)


print("\n")
print("============================================================")
print("                 EDA COMPLETED")
print("============================================================")

print("\nEDA result files saved successfully!")

print("\nCreated files:")
print("- monthly_revenue.csv")
print("- category_performance.csv")
print("- product_performance.csv")
print("- state_performance.csv")
print("- payment_analysis.csv")
print("- customer_analysis.csv")
print("- return_analysis.csv")
print("- category_profit.csv")