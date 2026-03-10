import psycopg2
import csv
import os
from datetime import datetime
from config.db import connect,close


def parse_date(date_str):
    for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%-d/%-m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"format tanggal tidak dikenali: {date_str}")


def clean_number(value):
    return value.replace(",", "")  


def insert_customers(cursor, data):
    query = """
        INSERT INTO customers (customer_name, segment)
        VALUES (%s, %s)
        ON CONFLICT (customer_name) DO NOTHING
    """
    seen = set()
    for row in data:
        key = row["customer_name"]
        if key not in seen:
            seen.add(key)
            cursor.execute(query, [row["customer_name"], row["segment"]])
    print(f"customers inserted: {len(seen)}")


def insert_regions(cursor, data):
    query = """
        INSERT INTO regions (state, country, market, region)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (state, country) DO NOTHING
    """
    seen = set()
    for row in data:
        key = (row["state"], row["country"])
        if key not in seen:
            seen.add(key)
            cursor.execute(query, [row["state"], row["country"], row["market"], row["region"]])
    print(f"regions inserted: {len(seen)}")


def insert_products(cursor, data):
    query = """
        INSERT INTO products (product_id, product_name, category, sub_category)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
    """
    seen = set()
    for row in data:
        key = row["product_id"]
        if key not in seen:
            seen.add(key)
            cursor.execute(query, [row["product_id"], row["product_name"], row["category"], row["sub_category"]])
    print(f"products inserted: {len(seen)}")


def insert_orders(cursor, data):
    query_order = """
        INSERT INTO orders (order_id, order_date, ship_date, ship_mode, order_priority, year, customer_id, region_id)
        VALUES (%s, %s, %s, %s, %s, %s,
            (SELECT id FROM customers WHERE customer_name = %s LIMIT 1),
            (SELECT id FROM regions WHERE state = %s AND country = %s LIMIT 1)
        )
        ON CONFLICT (order_id) DO NOTHING
    """
    seen = set()
    for row in data:
        key = row["order_id"]
        if key not in seen:
            seen.add(key)
            cursor.execute(query_order, [
                row["order_id"],
                parse_date(row["order_date"]),  
                parse_date(row["ship_date"]),
                row["ship_mode"],
                row["order_priority"],
                int(row["year"]),
                row["customer_name"],
                row["state"],
                row["country"],
            ])
    print(f"orders inserted: {len(seen)}")

def insert_order_items(cursor, data):
    query = """
        INSERT INTO order_items (order_id, product_id, sales, quantity, discount, profit, shipping_cost)
        VALUES (
            (SELECT id FROM orders WHERE order_id = %s LIMIT 1),
            (SELECT id FROM products WHERE product_id = %s LIMIT 1),
            %s, %s, %s, %s, %s
        )
    """
    for row in data:
        cursor.execute(query, [
            row["order_id"],
            row["product_id"],
            float(clean_number(row["sales"])),
            int(clean_number(row["quantity"])),
            float(clean_number(row["discount"])),
            float(clean_number(row["profit"])),
            float(clean_number(row["shipping_cost"])),
        ])
    print(f"order_items inserted: {len(data)}")


def read_csv():
    path = os.path.join(os.path.dirname(__file__), "./../data/orders.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")

    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader]

def insert_to_flat_table(cursor, data):
    query = """
        INSERT INTO orders (
            order_id, order_date, ship_date, ship_mode, customer_name, 
            segment, state, country, market, region, product_id, 
            category, sub_category, product_name, sales, quantity, 
            discount, profit, shipping_cost, order_priority, year
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    for row in data:
        cursor.execute(query, [
            row["order_id"],
            parse_date(row["order_date"]),
            parse_date(row["ship_date"]),
            row["ship_mode"],
            row["customer_name"],
            row["segment"],
            row["state"],
            row["country"],
            row["market"],
            row["region"],
            row["product_id"],
            row["category"],
            row["sub_category"],
            row["product_name"],
            float(clean_number(row["sales"])),
            int(clean_number(row["quantity"])),
            float(clean_number(row["discount"])),
            float(clean_number(row["profit"])),
            float(clean_number(row["shipping_cost"])),
            row["order_priority"],
            int(row["year"])
        ])
    print(f"Total rows inserted into flat table: {len(data)}")
