import csv
import sqlite3
from collections import defaultdict

conn = sqlite3.connect('shipment_database.db')
cursor = conn.cursor()

product_cache = {}

def get_or_create_product_id(product_name):
    if product_name in product_cache:
        return product_cache[product_name]
    cursor.execute("SELECT id FROM product WHERE name = ?", (product_name,))
    row = cursor.fetchone()
    if row:
        product_cache[product_name] = row[0]
        return row[0]
    cursor.execute("INSERT INTO product (name) VALUES (?)", (product_name,))
    new_id = cursor.lastrowid
    product_cache[product_name] = new_id
    return new_id

# --- Spreadsheet 0: self-contained, one row per shipment ---
with open('data/shipping_data_0.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        product_id = get_or_create_product_id(row['product'])
        cursor.execute(
            "INSERT INTO shipment (product_id, quantity, origin, destination) VALUES (?, ?, ?, ?)",
            (product_id, int(row['product_quantity']), row['origin_warehouse'], row['destination_store'])
        )

# --- Spreadsheet 2: shipment-level origin/destination, keyed by shipment_identifier ---
shipment_info = {}
with open('data/shipping_data_2.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        shipment_info[row['shipment_identifier']] = {
            'origin': row['origin_warehouse'],
            'destination': row['destination_store']
        }

# --- Spreadsheet 1: one row per product, need to count occurrences per (shipment, product) ---
quantities = defaultdict(int)
with open('data/shipping_data_1.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['shipment_identifier'], row['product'])
        quantities[key] += 1

for (shipment_id, product_name), quantity in quantities.items():
    product_id = get_or_create_product_id(product_name)
    info = shipment_info[shipment_id]
    cursor.execute(
        "INSERT INTO shipment (product_id, quantity, origin, destination) VALUES (?, ?, ?, ?)",
        (product_id, quantity, info['origin'], info['destination'])
    )

conn.commit()
conn.close()

print("Done inserting all shipment data.")