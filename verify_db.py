import sqlite3

conn = sqlite3.connect('shipment_database.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM product")
print("Total products:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM shipment")
print("Total shipment rows:", cursor.fetchone()[0])

print("\nSample shipment rows:")
cursor.execute("""
    SELECT shipment.id, product.name, shipment.quantity, shipment.origin, shipment.destination
    FROM shipment
    JOIN product ON shipment.product_id = product.id
    LIMIT 10
""")
for row in cursor.fetchall():
    print(row)

print("\nChecking grouped shipment (should be 2 rows: pants qty=3, keyboards qty=2):")
cursor.execute("""
    SELECT product.name, shipment.quantity, shipment.origin, shipment.destination
    FROM shipment
    JOIN product ON shipment.product_id = product.id
    WHERE shipment.origin = 'bb75bf7d-c008-4267-bf92-6089cff5fe56'
    AND shipment.destination = '5e9405de-a078-4b00-99c6-96564568b63c'
""")
for row in cursor.fetchall():
    print(row)

conn.close()