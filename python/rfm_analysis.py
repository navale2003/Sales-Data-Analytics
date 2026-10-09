import pandas as pd


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

customers = pd.read_csv(
    "data/cleaned/customers_cleaned.csv"
)

orders = pd.read_csv(
    "data/cleaned/orders_cleaned.csv"
)

print("Customers and orders loaded successfully!")


# ============================================================
# 2. CONVERT DATE
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)


# ============================================================
# 3. KEEP COMPLETED ORDERS
# ============================================================

completed_orders = orders[
    orders["order_status"] == "Completed"
].copy()

print("\nTotal Orders:", len(orders))
print("Completed Orders:", len(completed_orders))


# ============================================================
# 4. CALCULATE REVENUE
# ============================================================

completed_orders["revenue"] = (
    completed_orders["quantity"] *
    completed_orders["unit_price"]
)


# ============================================================
# 5. SET ANALYSIS DATE
# ============================================================

analysis_date = (
    completed_orders["order_date"].max()
    + pd.Timedelta(days=1)
)

print("\nAnalysis Date:", analysis_date.date())


# ============================================================
# 6. CALCULATE RFM METRICS
# ============================================================

rfm = (
    completed_orders
    .groupby("customer_id")
    .agg(
        Recency=(
            "order_date",
            lambda x: (
                analysis_date - x.max()
            ).days
        ),

        Frequency=(
            "order_id",
            "nunique"
        ),

        Monetary=(
            "revenue",
            "sum"
        )
    )
    .reset_index()
)


# ============================================================
# 7. ROUND MONETARY VALUE
# ============================================================

rfm["Monetary"] = rfm["Monetary"].round(2)


print("\n")
print("=" * 70)
print("RFM METRICS")
print("=" * 70)

print(
    rfm.head(10).to_string(index=False)
)


# ============================================================
# 8. CREATE RFM SCORES
# ============================================================

# Recency:
# Lower is better
# Recent customers receive higher scores

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    5,
    labels=[5, 4, 3, 2, 1],
    duplicates="drop"
)


# Frequency:
# Higher is better

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)


# Monetary:
# Higher spending is better

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop"
)


# Convert scores to integers

rfm["R_Score"] = rfm["R_Score"].astype(int)

rfm["F_Score"] = rfm["F_Score"].astype(int)

rfm["M_Score"] = rfm["M_Score"].astype(int)


# ============================================================
# 9. CREATE TOTAL RFM SCORE
# ============================================================

rfm["RFM_Score"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)


print("\n")
print("=" * 70)
print("RFM SCORES")
print("=" * 70)

print(
    rfm.head(10).to_string(index=False)
)


# ============================================================
# 10. CREATE CUSTOMER SEGMENTS
# ============================================================

def segment_customer(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4 and m >= 3:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "New Customers"

    elif r >= 3 and f >= 2 and m >= 2:
        return "Potential Loyalists"

    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2 and m >= 3:
        return "Cannot Lose Them"

    elif r <= 2 and f <= 2:
        return "Lost Customers"

    else:
        return "Others"


rfm["Segment"] = rfm.apply(
    segment_customer,
    axis=1
)


# ============================================================
# 11. SEGMENT SUMMARY
# ============================================================

segment_summary = (
    rfm
    .groupby("Segment")
    .agg(
        customers=("customer_id", "count"),
        average_recency=("Recency", "mean"),
        average_frequency=("Frequency", "mean"),
        total_revenue=("Monetary", "sum"),
        average_revenue=("Monetary", "mean")
    )
    .reset_index()
)


segment_summary["average_recency"] = (
    segment_summary["average_recency"].round(2)
)

segment_summary["average_frequency"] = (
    segment_summary["average_frequency"].round(2)
)

segment_summary["total_revenue"] = (
    segment_summary["total_revenue"].round(2)
)

segment_summary["average_revenue"] = (
    segment_summary["average_revenue"].round(2)
)


segment_summary = segment_summary.sort_values(
    "total_revenue",
    ascending=False
)


# ============================================================
# 12. DISPLAY SEGMENT SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("CUSTOMER SEGMENT SUMMARY")
print("=" * 70)

print(
    segment_summary.to_string(index=False)
)


# ============================================================
# 13. TOP CUSTOMERS
# ============================================================

top_customers = (
    rfm
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(20)
)


print("\n")
print("=" * 70)
print("TOP 20 CUSTOMERS BY MONETARY VALUE")
print("=" * 70)

print(
    top_customers[
        [
            "customer_id",
            "Recency",
            "Frequency",
            "Monetary",
            "RFM_Score",
            "Segment"
        ]
    ].to_string(index=False)
)


# ============================================================
# 14. MERGE CUSTOMER INFORMATION
# ============================================================

rfm_customer = rfm.merge(
    customers[
        [
            "customer_id",
            "name",
            "email",
            "city",
            "state",
            "age",
            "gender"
        ]
    ],
    on="customer_id",
    how="left"
)


# ============================================================
# 15. SAVE RFM RESULTS
# ============================================================

rfm.to_csv(
    "data/cleaned/rfm_customer_analysis.csv",
    index=False
)

segment_summary.to_csv(
    "data/cleaned/customer_segments.csv",
    index=False
)

rfm_customer.to_csv(
    "data/cleaned/rfm_customer_details.csv",
    index=False
)


# ============================================================
# 16. COMPLETION MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("RFM ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created:")

print("- rfm_customer_analysis.csv")

print("- customer_segments.csv")

print("- rfm_customer_details.csv")