import sqlite3

conn = sqlite3.connect('shipment_database.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")
    cursor.execute(f"PRAGMA table_info({table_name});")
    for col in cursor.fetchall():
        print(f"  {col[1]} ({col[2]})")

conn.close()