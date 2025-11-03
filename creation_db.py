import sqlite3

# Connect to database
db = sqlite3.connect("store_inventory.db")

# Create Product table
db.execute("""
CREATE TABLE IF NOT EXISTS Product (
    id_product INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Create Customer table
db.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    id_customer INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT
)
""")

# Create Sale table
db.execute("""
CREATE TABLE IF NOT EXISTS Sale (
    id_sale INTEGER PRIMARY KEY AUTOINCREMENT,
    id_product INTEGER,
    id_customer INTEGER,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (id_product) REFERENCES Product(id_product),
    FOREIGN KEY (id_customer) REFERENCES Customer(id_customer)
)
""")

# Insert sample data
db.execute("INSERT INTO Product (name, price) VALUES (?, ?)", ("Laptop", 1200))
db.execute("INSERT INTO Product (name, price) VALUES (?, ?)", ("Mouse", 25))

db.execute("INSERT INTO Customer (name, phone) VALUES (?, ?)", ("Alice", "0612345678"))
db.execute("INSERT INTO Customer (name, phone) VALUES (?, ?)", ("Yassin", "0698765432"))

db.execute("INSERT INTO Sale (id_product, id_customer, quantity, total_price) VALUES (?, ?, ?, ?)", (1, 1, 1, 1200))
db.execute("INSERT INTO Sale (id_product, id_customer, quantity, total_price) VALUES (?, ?, ?, ?)", (2, 2, 2, 50))

# Commit and show results
db.commit()

db.row_factory = sqlite3.Row
cursor = db.execute("SELECT * FROM Sale")

for row in cursor:
    print("Sale ID:", row["id_sale"], " | Product ID:", row["id_product"], " | Customer ID:", row["id_customer"], " | Total:", row["total_price"])

db.close()
