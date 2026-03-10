import os
import duckdb

path = os.path.join(os.path.dirname(__file__), "./../data/orders.csv")

def analyze_get_user_most_discount():
    
    query = f"""
        SELECT 
            customer_name, 
            ROUND(SUM(CAST(discount AS DOUBLE))) as total_discount
        FROM '{path}'
        GROUP BY customer_name
        ORDER BY total_discount DESC
        LIMIT 10
    """
    
    result = duckdb.sql(query).fetchall()
    
    for row in result:
        print(f"name: {row[0]}, total: {row[1]}")

def get_top_spender():
    
    query = f"""
        SELECT 
            customer_name, 
            SUM(CAST(REPLACE(sales, ',', '') AS DOUBLE)) as total_spender
        FROM '{path}'
        GROUP BY customer_name
        ORDER BY total_spender DESC
        LIMIT 10
    """
    
    result = duckdb.sql(query).fetchall()
    
    for row in result:
        print(f"name: {row[0]}, total: {row[1]}")

def top_location_far():
    query = f"""
        SELECT 
            country, 
            state,
            SUM(CAST(shipping_cost AS DOUBLE)) as total_shipping_cost,
            COUNT(order_id) as count_orders,
        FROM '{path}'
        GROUP BY country, state
        ORDER BY count_orders DESC
        LIMIT 10
    """
    
    result = duckdb.sql(query).fetchall()
    
    # Header yang disesuaikan
    print(f"{'Country':<20} | {'State':<20} | {'Orders':<10} | {'Shipping Cost':<15}")
    print("-" * 75) 

    for row in result:
        print(f"{str(row[0]):<20} | {str(row[1])[:17]+'...':<20} | {row[3]:<10} | {row[2]:<15.2f}")

def how_to_get_discount_value():
    query = f"""
        SELECT 
            order_id, 
            SUM(CAST(REPLACE(sales, ',', '') AS DOUBLE) * CAST(discount AS DOUBLE)) AS total_discount_nominal   
        FROM '{path}'
        GROUP BY order_id
        ORDER BY total_discount_nominal DESC
        LIMIT 10
    """
    
    result = duckdb.sql(query).fetchall()
    
    for row in result:
        print(f"order: {row[0]}, total: {row[1]}")

def how_to_get_price_product():
    query = f"""
        SELECT 
            order_id, 
            product_name,
            SUM((CAST(REPLACE(sales, ',', '') AS DOUBLE) / (1 - CAST(discount AS DOUBLE))) / CAST(quantity AS INT)) AS harga_satuan_asli_total
        FROM '{path}'
        GROUP BY order_id,product_name
        ORDER BY harga_satuan_asli_total DESC
        LIMIT 10
    """
    
    result = duckdb.sql(query).fetchall()
    print(f"{'Order ID':<15} | {'Product Name':<30} | {'Harga Product':<15}")
    print("-" * 65) 

    for row in result:
        print(f"{str(row[0]):<15} | {str(row[1])[:27]+'...':<30} | {row[2]:<15.2f}")