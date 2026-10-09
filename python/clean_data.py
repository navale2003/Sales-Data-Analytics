import pandas as pd


# =============================
# LOAD RAW DATA
# =============================

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")
payments = pd.read_csv("data/raw/payments.csv")
returns = pd.read_csv("data/raw/returns.csv")


# =============================
# INSPECT CUSTOMERS
# =============================

print("\n========== CUSTOMERS ==========")

print("Shape:", customers.shape)

print("\nFirst 5 rows:")
print(customers.head())

print("\nData types:")
print(customers.dtypes)


# =============================
# INSPECT PRODUCTS
# =============================

print("\n========== PRODUCTS ==========")

print("Shape:", products.shape)

print("\nFirst 5 rows:")
print(products.head())

print("\nData types:")
print(products.dtypes)


# =============================
# INSPECT ORDERS
# =============================

print("\n========== ORDERS ==========")

print("Shape:", orders.shape)

print("\nFirst 5 rows:")
print(orders.head())

print("\nData types:")
print(orders.dtypes)


# =============================
# INSPECT PAYMENTS
# =============================

print("\n========== PAYMENTS ==========")

print("Shape:", payments.shape)

print("\nFirst 5 rows:")
print(payments.head())

print("\nData types:")
print(payments.dtypes)


# =============================
# INSPECT RETURNS
# =============================

print("\n========== RETURNS ==========")

print("Shape:", returns.shape)

print("\nFirst 5 rows:")
print(returns.head())

print("\nData types:")
print(returns.dtypes)

# =============================
# CHECK MISSING VALUES
# =============================

print("\n\n========== MISSING VALUES ==========")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nPayments:")
print(payments.isnull().sum())

print("\nReturns:")
print(returns.isnull().sum())

# =============================
# CHECK DUPLICATE ROWS
# =============================

print("\n\n========== DUPLICATE ROWS ==========")

print("\nCustomers duplicates:")
print(customers.duplicated().sum())

print("\nProducts duplicates:")
print(products.duplicated().sum())

print("\nOrders duplicates:")
print(orders.duplicated().sum())

print("\nPayments duplicates:")
print(payments.duplicated().sum())

print("\nReturns duplicates:")
print(returns.duplicated().sum())
# =============================
# CONVERT DATE COLUMNS
# =============================

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


print("\n\n========== DATE TYPES AFTER CONVERSION ==========")

print("\nCustomers signup_date:")
print(customers["signup_date"].dtype)

print("\nOrders order_date:")
print(orders["order_date"].dtype)

print("\nPayments payment_date:")
print(payments["payment_date"].dtype)

print("\nReturns return_date:")
print(returns["return_date"].dtype)

# =============================
# CHECK INVALID NUMERICAL VALUES
# =============================

print("\n\n========== INVALID NUMERICAL VALUES ==========")

# -----------------------------
# CUSTOMER AGE
# -----------------------------

print("\nCustomers with invalid age:")

invalid_age = customers[
    (customers["age"] < 18) |
    (customers["age"] > 100)
]

print(invalid_age)
print("Count:", len(invalid_age))


# -----------------------------
# ORDER QUANTITY
# -----------------------------

print("\nOrders with invalid quantity:")

invalid_quantity = orders[
    orders["quantity"] <= 0
]

print(invalid_quantity)
print("Count:", len(invalid_quantity))


# -----------------------------
# ORDER UNIT PRICE
# -----------------------------

print("\nOrders with invalid unit price:")

invalid_unit_price = orders[
    orders["unit_price"] < 0
]

print(invalid_unit_price)
print("Count:", len(invalid_unit_price))


# -----------------------------
# ORDER DISCOUNT
# -----------------------------

print("\nOrders with invalid discount:")

invalid_discount = orders[
    (orders["discount"] < 0) |
    (orders["discount"] > 100)
]

print(invalid_discount)
print("Count:", len(invalid_discount))


# -----------------------------
# PRODUCT PRICE
# -----------------------------

print("\nProducts with invalid price:")

invalid_product_price = products[
    products["price"] <= 0
]

print(invalid_product_price)
print("Count:", len(invalid_product_price))


# -----------------------------
# PRODUCT COST
# -----------------------------

print("\nProducts with invalid cost:")

invalid_product_cost = products[
    products["cost"] <= 0
]

print(invalid_product_cost)
print("Count:", len(invalid_product_cost))


# -----------------------------
# PRODUCT COST GREATER THAN PRICE
# -----------------------------

print("\nProducts where cost is greater than price:")

invalid_cost_price = products[
    products["cost"] > products["price"]
]

print(invalid_cost_price)
print("Count:", len(invalid_cost_price))

# =============================
# CHECK CATEGORICAL VALUES
# =============================

print("\n\n========== CATEGORICAL VALUES ==========")


# -----------------------------
# CUSTOMER GENDER
# -----------------------------

print("\nCustomer Gender:")
print(customers["gender"].value_counts())


# -----------------------------
# CUSTOMER CITY
# -----------------------------

print("\nCustomer City:")
print(customers["city"].value_counts())


# -----------------------------
# CUSTOMER STATE
# -----------------------------

print("\nCustomer State:")
print(customers["state"].value_counts())


# -----------------------------
# PRODUCT CATEGORY
# -----------------------------

print("\nProduct Category:")
print(products["category"].value_counts())


# -----------------------------
# ORDER STATUS
# -----------------------------

print("\nOrder Status:")
print(orders["order_status"].value_counts())


# -----------------------------
# PAYMENT METHOD
# -----------------------------

print("\nPayment Method:")
print(payments["payment_method"].value_counts())


# -----------------------------
# PAYMENT STATUS
# -----------------------------

print("\nPayment Status:")
print(payments["payment_status"].value_counts())


# -----------------------------
# RETURN REASON
# -----------------------------

print("\nReturn Reason:")
print(returns["return_reason"].value_counts())
# =============================
# CHECK REFERENTIAL INTEGRITY
# =============================

print("\n\n========== REFERENTIAL INTEGRITY ==========")


# -----------------------------
# CUSTOMER IDs
# -----------------------------

invalid_customer_ids = orders[
    ~orders["customer_id"].isin(customers["customer_id"])
]

print("\nOrders with invalid customer_id:")
print("Count:", len(invalid_customer_ids))


# -----------------------------
# PRODUCT IDs
# -----------------------------

invalid_product_ids = orders[
    ~orders["product_id"].isin(products["product_id"])
]

print("\nOrders with invalid product_id:")
print("Count:", len(invalid_product_ids))


# -----------------------------
# PAYMENT ORDER IDs
# -----------------------------

invalid_payment_order_ids = payments[
    ~payments["order_id"].isin(orders["order_id"])
]

print("\nPayments with invalid order_id:")
print("Count:", len(invalid_payment_order_ids))


# -----------------------------
# RETURN ORDER IDs
# -----------------------------

invalid_return_order_ids = returns[
    ~returns["order_id"].isin(orders["order_id"])
]

print("\nReturns with invalid order_id:")
print("Count:", len(invalid_return_order_ids))
# =============================
# SAVE CLEANED DATA
# =============================

print("\n\n========== SAVING CLEANED DATA ==========")

customers.to_csv(
    "data/cleaned/customers_cleaned.csv",
    index=False
)

products.to_csv(
    "data/cleaned/products_cleaned.csv",
    index=False
)

orders.to_csv(
    "data/cleaned/orders_cleaned.csv",
    index=False
)

payments.to_csv(
    "data/cleaned/payments_cleaned.csv",
    index=False
)

returns.to_csv(
    "data/cleaned/returns_cleaned.csv",
    index=False
)

print("\nCleaned datasets saved successfully!")

print("\nFiles created:")
print("1. customers_cleaned.csv")
print("2. products_cleaned.csv")
print("3. orders_cleaned.csv")
print("4. payments_cleaned.csv")
print("5. returns_cleaned.csv")