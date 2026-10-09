import pandas as pd
import os

# ============================================================
# 1. LOAD DATA
# ============================================================

customers_path = "data/cleaned/customers_cleaned.csv"
orders_path = "data/cleaned/orders_cleaned.csv"

customers = pd.read_csv(customers_path)
orders = pd.read_csv(orders_path)

# Convert date column
orders["order_date"] = pd.to_datetime(orders["order_date"])

print("=" * 70)
print("CHURN ANALYSIS")
print("=" * 70)


# ============================================================
# 2. USE COMPLETED ORDERS ONLY
# ============================================================

completed_orders = orders[
    orders["order_status"] == "Completed"
].copy()

print("\nTotal completed orders:", len(completed_orders))


# ============================================================
# 3. CALCULATE ORDER REVENUE
# ============================================================

completed_orders["revenue"] = (
    completed_orders["quantity"]
    * completed_orders["unit_price"]
)

completed_orders["discount_amount"] = (
    completed_orders["revenue"]
    * completed_orders["discount"]
    / 100
)

completed_orders["net_revenue"] = (
    completed_orders["revenue"]
    - completed_orders["discount_amount"]
)


# ============================================================
# 4. FIND LAST PURCHASE FOR EACH CUSTOMER
# ============================================================

customer_activity = completed_orders.groupby(
    "customer_id"
).agg(
    last_purchase_date=("order_date", "max"),
    frequency=("order_id", "nunique"),
    monetary=("net_revenue", "sum")
).reset_index()


# ============================================================
# 5. INCLUDE ALL CUSTOMERS
# ============================================================

customer_churn = customers[
    ["customer_id", "name", "city", "state", "age", "gender"]
].merge(
    customer_activity,
    on="customer_id",
    how="left"
)


# ============================================================
# 6. ANALYSIS DATE
# ============================================================

analysis_date = completed_orders["order_date"].max() + pd.Timedelta(days=1)

print("\nAnalysis date:", analysis_date.date())


# ============================================================
# 7. CALCULATE DAYS SINCE LAST PURCHASE
# ============================================================

customer_churn["days_since_last_purchase"] = (
    analysis_date - customer_churn["last_purchase_date"]
).dt.days


# ============================================================
# 8. HANDLE CUSTOMERS WHO NEVER PURCHASED
# ============================================================

customer_churn["frequency"] = (
    customer_churn["frequency"]
    .fillna(0)
    .astype(int)
)

customer_churn["monetary"] = (
    customer_churn["monetary"]
    .fillna(0)
)


# ============================================================
# 9. DEFINE CHURN STATUS
# ============================================================

# Assumption:
# A customer is considered churned if they have not purchased
# for more than 90 days.

def classify_customer(row):

    if row["frequency"] == 0:
        return "Never Purchased"

    elif row["days_since_last_purchase"] > 90:
        return "Churned"

    else:
        return "Active"


customer_churn["churn_status"] = customer_churn.apply(
    classify_customer,
    axis=1
)


# ============================================================
# 10. CHURN SUMMARY
# ============================================================

total_customers = len(customer_churn)

purchased_customers = customer_churn[
    customer_churn["frequency"] > 0
]

customers_with_purchase = len(purchased_customers)

churned_customers = len(
    customer_churn[
        customer_churn["churn_status"] == "Churned"
    ]
)

active_customers = len(
    customer_churn[
        customer_churn["churn_status"] == "Active"
    ]
)

never_purchased = len(
    customer_churn[
        customer_churn["churn_status"] == "Never Purchased"
    ]
)


# ============================================================
# 11. CHURN RATE
# ============================================================

if customers_with_purchase > 0:

    churn_rate = (
        churned_customers
        / customers_with_purchase
        * 100
    )

else:
    churn_rate = 0


# ============================================================
# 12. PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER CHURN SUMMARY")
print("=" * 70)

print("Total Customers       :", total_customers)
print("Customers Purchased   :", customers_with_purchase)
print("Active Customers      :", active_customers)
print("Churned Customers     :", churned_customers)
print("Never Purchased       :", never_purchased)

print(
    "Churn Rate            :",
    round(churn_rate, 2),
    "%"
)


# ============================================================
# 13. CHURN STATUS DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("CHURN STATUS DISTRIBUTION")
print("=" * 70)

status_summary = (
    customer_churn["churn_status"]
    .value_counts()
    .reset_index()
)

status_summary.columns = [
    "churn_status",
    "customer_count"
]

status_summary["percentage"] = (
    status_summary["customer_count"]
    / total_customers
    * 100
)

print(status_summary.to_string(index=False))


# ============================================================
# 14. CHURN BY STATE
# ============================================================

print("\n" + "=" * 70)
print("CHURN BY STATE")
print("=" * 70)

state_churn = (
    customer_churn[
        customer_churn["frequency"] > 0
    ]
    .groupby("state")
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn_status",
                           lambda x: (x == "Churned").sum())
    )
    .reset_index()
)

state_churn["churn_rate"] = (
    state_churn["churned_customers"]
    / state_churn["total_customers"]
    * 100
)

state_churn = state_churn.sort_values(
    "churn_rate",
    ascending=False
)

print(
    state_churn.head(10).to_string(index=False)
)


# ============================================================
# 15. HIGH-VALUE CHURNED CUSTOMERS
# ============================================================

print("\n" + "=" * 70)
print("HIGH-VALUE CHURNED CUSTOMERS")
print("=" * 70)

high_value_churned = customer_churn[
    customer_churn["churn_status"] == "Churned"
].sort_values(
    "monetary",
    ascending=False
)

print(
    high_value_churned[
        [
            "customer_id",
            "name",
            "state",
            "last_purchase_date",
            "days_since_last_purchase",
            "frequency",
            "monetary",
            "churn_status"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 16. SAVE RESULTS
# ============================================================

output_folder = "data/cleaned"

os.makedirs(output_folder, exist_ok=True)

customer_churn.to_csv(
    f"{output_folder}/customer_churn_analysis.csv",
    index=False
)

status_summary.to_csv(
    f"{output_folder}/churn_summary.csv",
    index=False
)

state_churn.to_csv(
    f"{output_folder}/state_churn_analysis.csv",
    index=False
)

print("\n" + "=" * 70)
print("CHURN ANALYSIS COMPLETED")
print("=" * 70)

print("\nFiles saved:")
print("1. customer_churn_analysis.csv")
print("2. churn_summary.csv")
print("3. state_churn_analysis.csv")