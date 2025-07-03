import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Create SQLite DB and connect
db_name = "sales_data.db"
if os.path.exists(db_name):
    os.remove(db_name)

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Step 2: Create a simple 'sales' table
cursor.execute("""
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    );
""")

# Step 3: Insert some sample sales data
sample_sales = [
    ('Laptop', 5, 800.0),
    ('Mouse', 20, 25.0),
    ('Keyboard', 10, 45.0),
    ('Laptop', 2, 800.0),
    ('Mouse', 15, 25.0),
    ('Keyboard', 5, 45.0)
]

cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_sales)
conn.commit()

# Step 4: Run SQL query to get summary
query = """
    SELECT 
        product, 
        SUM(quantity) AS total_qty, 
        SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product;
"""

df = pd.read_sql_query(query, conn)

# Step 5: Print summary
print("📦 Basic Sales Summary:")
print(df)

# Step 6: Plot revenue bar chart
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='product', y='revenue', color='skyblue', legend=False)
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Step 7: Close connection
conn.close()
