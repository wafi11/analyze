import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("functions")

functions_metadata = [
    {
        "name": "analyze_get_user_most_discount",
        "description": "customer yang paling banyak dapat diskon, top discount, siapa yang sering diskon"
    },
    {
        "name": "get_top_spender",
        "description": "customer paling banyak belanja, top spender, siapa yang paling boros, total pembelian terbesar"
    },
    {
        "name": "top_location_far",
        "description": "lokasi pengiriman terbanyak, shipping cost tertinggi, daerah mana yang paling banyak order"
    },
    {
        "name": "how_to_get_discount_value",
        "description": "nominal diskon terbesar per order, berapa nilai diskon yang diberikan"
    },
    {
        "name": "how_to_get_price_product",
        "description": "harga asli produk sebelum diskon, harga satuan produk, original price"
    },
    {
        "name": "recommendations_packet_bundling",
        "description": "rekomendasi bundling produk, produk yang sering dibeli bersamaan, paket produk"
    },
]

collection.upsert(
    ids=[f["name"] for f in functions_metadata],
    documents=[f["description"] for f in functions_metadata],
    metadatas=[{"name": f["name"]} for f in functions_metadata]
)

def find_relevant_function(user_message: str, n_results: int = 2):
    results = collection.query(
        query_texts=[user_message],
        n_results=n_results
    )
    return [meta["name"] for meta in results["metadatas"][0]]