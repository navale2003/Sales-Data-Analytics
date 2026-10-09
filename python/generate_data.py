
import pandas as pd
import numpy as np
from faker import Faker

# -----------------------------
# Setup
# -----------------------------

fake = Faker("en_IN")

np.random.seed(42)

# Number of records
NUM_CUSTOMERS = 20_000
NUM_PRODUCTS = 500



# -----------------------------
# Generate Customers
# -----------------------------

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "state": fake.state(),
        "age": np.random.randint(18, 65),
        "gender": np.random.choice(
            ["Male", "Female", "Other"],
            p=[0.48, 0.48, 0.04]
        ),
        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        )
    })


customers_df = pd.DataFrame(customers)


# -----------------------------
# Generate Products
# -----------------------------

categories = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books",
    "Accessories"
]

products = []

for product_id in range(1, NUM_PRODUCTS + 1):

    category = np.random.choice(categories)

    products.append({
        "product_id": product_id,
        "product_name": f"{category} Product {product_id}",
        "category": category,
        "price": round(np.random.uniform(200, 50000), 2),
        "cost": round(np.random.uniform(100, 30000), 2)
    })


products_df = pd.DataFrame(products)


# -----------------------------
# Save CSV files
# -----------------------------

customers_df.to_csv(
    "data/raw/customers.csv",
    index=False
)

products_df.to_csv(
    "data/raw/products.csv",
    index=False
)


# -----------------------------
# Display results
# -----------------------------

print("Customers created:", len(customers_df))
print("Products created:", len(products_df))

print("\nCustomer sample:")
print(customers_df.head())

print("\nProduct sample:")
print(products_df.head())

print("\nData generation completed!")

# -----------------------------
# Generate Orders
# -----------------------------

NUM_ORDERS = 100_000

orders = []

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

order_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Cancelled"
]

for order_id in range(1, NUM_ORDERS + 1):

    customer_id = np.random.randint(1, NUM_CUSTOMERS + 1)
    product_id = np.random.randint(1, NUM_PRODUCTS + 1)

    product_price = products_df.loc[
        products_df["product_id"] == product_id,
        "price"
    ].values[0]

    quantity = np.random.randint(1, 5)

    discount = np.random.choice(
        [0, 5, 10, 15, 20, 25],
        p=[0.20, 0.20, 0.25, 0.15, 0.15, 0.05]
    )

    payment_method = np.random.choice(payment_methods)

    order_status = np.random.choice(order_statuses)

    order_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "order_date": order_date,
        "quantity": quantity,
        "unit_price": round(product_price, 2),
        "discount": discount,
        "payment_method": payment_method,
        "order_status": order_status
    })


orders_df = pd.DataFrame(orders)


# -----------------------------
# Save Orders
# -----------------------------

orders_df.to_csv(
    "data/raw/orders.csv",
    index=False
)


print("\nOrders created:", len(orders_df))

print("\nOrder sample:")
print(orders_df.head())

print("\nAll data generation completed!")
# -----------------------------
# Generate Payments
# -----------------------------

payments = []

payment_statuses = [
    "Paid",
    "Paid",
    "Paid",
    "Failed",
    "Refunded"
]

for order_id in orders_df["order_id"]:

    payment_status = np.random.choice(payment_statuses)

    payment_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    payments.append({
        "payment_id": order_id,
        "order_id": order_id,
        "payment_method": orders_df.loc[
            orders_df["order_id"] == order_id,
            "payment_method"
        ].values[0],
        "payment_status": payment_status,
        "payment_date": payment_date
    })


payments_df = pd.DataFrame(payments)


# -----------------------------
# Save Payments
# -----------------------------

payments_df.to_csv(
    "data/raw/payments.csv",
    index=False
)

print("\nPayments created:", len(payments_df))

print("\nPayment sample:")
print(payments_df.head())


# -----------------------------
# Generate Returns
# -----------------------------

NUM_RETURNS = 10000

return_order_ids = np.random.choice(
    orders_df["order_id"],
    size=NUM_RETURNS,
    replace=False
)

returns = []

return_reasons = [
    "Damaged Product",
    "Wrong Product",
    "Product Not as Expected",
    "Late Delivery",
    "Quality Issue",
    "Changed Mind"
]

for i, order_id in enumerate(return_order_ids, start=1):

    return_date = fake.date_between(
        start_date="-1y",
        end_date="today"
    )

    return_reason = np.random.choice(return_reasons)

    returns.append({
        "return_id": i,
        "order_id": order_id,
        "return_date": return_date,
        "return_reason": return_reason
    })


returns_df = pd.DataFrame(returns)


# -----------------------------
# Save Returns
# -----------------------------

returns_df.to_csv(
    "data/raw/returns.csv",
    index=False
)

print("\nReturns created:", len(returns_df))

print("\nReturn sample:")
print(returns_df.head())

print("\nALL DATA GENERATION COMPLETED!")