import pandas as pd


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

orders = pd.read_csv(
    "data/cleaned/orders_cleaned.csv"
)

products = pd.read_csv(
    "data/cleaned/products_cleaned.csv"
)

print("Orders and products loaded successfully!")


# ============================================================
# 2. KEEP COMPLETED ORDERS
# ============================================================

completed_orders = orders[
    orders["order_status"] == "Completed"
].copy()

print("\nTotal Orders:", len(orders))
print("Completed Orders:", len(completed_orders))


# ============================================================
# 3. CALCULATE REVENUE
# ============================================================

completed_orders["revenue"] = (
    completed_orders["quantity"]
    * completed_orders["unit_price"]
)


# ============================================================
# 4. CALCULATE DISCOUNT
# ============================================================

completed_orders["discount_amount"] = (
    completed_orders["revenue"]
    * completed_orders["discount"]
    / 100
)


# ============================================================
# 5. CALCULATE NET REVENUE
# ============================================================

completed_orders["net_revenue"] = (
    completed_orders["revenue"]
    - completed_orders["discount_amount"]
)


# ============================================================
# 6. JOIN PRODUCT COST
# ============================================================

profit_data = completed_orders.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "cost"
        ]
    ],
    on="product_id",
    how="left"
)


# ============================================================
# 7. CALCULATE PRODUCT COST
# ============================================================

profit_data["total_cost"] = (
    profit_data["quantity"]
    * profit_data["cost"]
)


# ============================================================
# 8. CALCULATE PROFIT
# ============================================================

profit_data["profit"] = (
    profit_data["net_revenue"]
    - profit_data["total_cost"]
)


# ============================================================
# 9. CALCULATE PROFIT MARGIN
# ============================================================

profit_data["profit_margin"] = (
    profit_data["profit"]
    / profit_data["net_revenue"]
    * 100
)


# ============================================================
# 10. OVERALL PROFITABILITY
# ============================================================

total_revenue = profit_data["revenue"].sum()

total_discount = profit_data["discount_amount"].sum()

total_net_revenue = profit_data["net_revenue"].sum()

total_cost = profit_data["total_cost"].sum()

total_profit = profit_data["profit"].sum()

overall_margin = (
    total_profit
    / total_net_revenue
    * 100
)


print("\n")
print("=" * 70)
print("OVERALL PROFITABILITY")
print("=" * 70)

print("\nTotal Revenue:", round(total_revenue, 2))

print("Total Discount:", round(total_discount, 2))

print("Net Revenue:", round(total_net_revenue, 2))

print("Total Product Cost:", round(total_cost, 2))

print("Total Profit:", round(total_profit, 2))

print(
    "Overall Profit Margin:",
    round(overall_margin, 2),
    "%"
)


# ============================================================
# 11. CATEGORY PROFITABILITY
# ============================================================

category_profit = (
    profit_data
    .groupby("category")
    .agg(
        orders=("order_id", "count"),
        quantity_sold=("quantity", "sum"),
        revenue=("net_revenue", "sum"),
        cost=("total_cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)


category_profit["profit_margin"] = (
    category_profit["profit"]
    / category_profit["revenue"]
    * 100
)


category_profit = category_profit.sort_values(
    "profit",
    ascending=False
)


print("\n")
print("=" * 70)
print("CATEGORY PROFITABILITY")
print("=" * 70)

print(
    category_profit.to_string(index=False)
)


# ============================================================
# 12. TOP 10 PROFITABLE PRODUCTS
# ============================================================

product_profit = (
    profit_data
    .groupby(
        [
            "product_id",
            "product_name",
            "category"
        ]
    )
    .agg(
        quantity_sold=("quantity", "sum"),
        revenue=("net_revenue", "sum"),
        cost=("total_cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)


product_profit["profit_margin"] = (
    product_profit["profit"]
    / product_profit["revenue"]
    * 100
)


product_profit = product_profit.sort_values(
    "profit",
    ascending=False
)


print("\n")
print("=" * 70)
print("TOP 10 MOST PROFITABLE PRODUCTS")
print("=" * 70)

print(
    product_profit.head(10).to_string(index=False)
)


# ============================================================
# 13. LOWEST PROFITABLE PRODUCTS
# ============================================================

lowest_profit_products = product_profit.sort_values(
    "profit"
)


print("\n")
print("=" * 70)
print("10 LOWEST PROFIT PRODUCTS")
print("=" * 70)

print(
    lowest_profit_products
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 14. HIGHEST MARGIN PRODUCTS
# ============================================================

highest_margin_products = product_profit.sort_values(
    "profit_margin",
    ascending=False
)


print("\n")
print("=" * 70)
print("10 HIGHEST MARGIN PRODUCTS")
print("=" * 70)

print(
    highest_margin_products
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 15. LOWEST MARGIN PRODUCTS
# ============================================================

lowest_margin_products = product_profit.sort_values(
    "profit_margin"
)


print("\n")
print("=" * 70)
print("10 LOWEST MARGIN PRODUCTS")
print("=" * 70)

print(
    lowest_margin_products
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 16. SAVE RESULTS
# ============================================================

profit_data.to_csv(
    "data/cleaned/profitability_details.csv",
    index=False
)

category_profit.to_csv(
    "data/cleaned/category_profitability.csv",
    index=False
)

product_profit.to_csv(
    "data/cleaned/product_profitability.csv",
    index=False
)


# ============================================================
# 17. COMPLETION MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("PROFITABILITY ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created:")

print("- profitability_details.csv")
print("- category_profitability.csv")
print("- product_profitability.csv")