import psycopg2


def connect():
    conn = psycopg2.connect("postgresql://postgres:password@localhost:5432/orders")
    print("database connected successfully")
    return conn

def close(conn):
    conn.close()
