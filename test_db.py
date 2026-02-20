import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('data/banking.db')

# Run a test query
query = "SELECT * FROM customers LIMIT 5"
df = pd.read_sql_query(query, conn)

print("First 5 customers:")
print(df)

# Close connection
conn.close()