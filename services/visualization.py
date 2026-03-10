import os
import duckdb
import matplotlib.pyplot as plt

path = os.path.join(os.path.dirname(__file__), "./../data/orders.csv")

def visualization():
    fig, axes = plt.subplots(3, 2, figsize=(15, 18))
    fig.subplots_adjust(hspace=0.5, wspace=0.3)
    axes = axes.flatten() # Biar gampang diakses pake index 0,1,2...

    # --- GRAFIK 1: Top Discount Users ---
    df1 = duckdb.sql(f"""
        SELECT customer_name, SUM(CAST(discount AS DOUBLE)) as total 
        FROM '{path}' GROUP BY 1 ORDER BY total DESC LIMIT 10
    """).df()
    axes[0].barh(df1['customer_name'], df1['total'], color='skyblue')
    axes[0].set_title('Top 10 Customers by Discount (Total)')
    axes[0].invert_yaxis()

    # --- GRAFIK 2: Top Spenders ---
    df2 = duckdb.sql(f"""
        SELECT customer_name, SUM(CAST(REPLACE(sales, ',', '') AS DOUBLE)) as total 
        FROM '{path}' GROUP BY 1 ORDER BY total DESC LIMIT 10
    """).df()
    axes[1].barh(df2['customer_name'], df2['total'], color='salmon')
    axes[1].set_title('Top 10 Spenders (Sales)')
    axes[1].invert_yaxis()

    # --- GRAFIK 3: Top Shipping Cost by Country ---
    df3 = duckdb.sql(f"""
        SELECT country, SUM(CAST(shipping_cost AS DOUBLE)) as total 
        FROM '{path}' GROUP BY 1 ORDER BY total DESC LIMIT 10
    """).df()
    axes[2].bar(df3['country'], df3['total'], color='gold')
    axes[2].set_title('Top 10 Shipping Cost by Country')
    plt.setp(axes[2].get_xticklabels(), rotation=45)

    # --- GRAFIK 4: Top Discount Nominal ---
    df4 = duckdb.sql(f"""
        SELECT order_id, SUM(CAST(REPLACE(sales, ',', '') AS DOUBLE) * CAST(discount AS DOUBLE)) AS total 
        FROM '{path}' GROUP BY 1 ORDER BY total DESC LIMIT 10
    """).df()
    axes[3].bar(df4['order_id'], df4['total'], color='lightgreen')
    axes[3].set_title('Top 10 Orders by Discount Nominal')
    plt.setp(axes[3].get_xticklabels(), rotation=45)

    # --- GRAFIK 5: Most Expensive Product Price ---
    df5 = duckdb.sql(f"""
        SELECT product_name, 
        AVG((CAST(REPLACE(sales, ',', '') AS DOUBLE) / (1 - NULLIF(CAST(discount AS DOUBLE), 1))) / CAST(quantity AS INT)) AS harga 
        FROM '{path}' GROUP BY 1 ORDER BY harga DESC LIMIT 10
    """).df()
    df5['product_name'] = df5['product_name'].str[:20] + '...'
    axes[4].barh(df5['product_name'], df5['harga'], color='orchid')
    axes[4].set_title('Top 10 Most Expensive Unit Price')
    axes[4].invert_yaxis()

    # Hapus subplots yang kosong (index 5)
    fig.delaxes(axes[5])

    print("Visualisasi selesai dibuat!")
    plt.savefig('dashboard_report.png') # Simpan jadi gambar
    plt.show()