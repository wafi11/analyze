import ollama
from config.chromaDB import find_relevant_function
from services.query import (
    analyze_get_user_most_discount,
    get_top_spender,
    top_location_far,
    how_to_get_discount_value,
    how_to_get_price_product,
    recommendations_packet_bundling
)

available_functions = {
    "analyze_get_user_most_discount": analyze_get_user_most_discount,
    "get_top_spender": get_top_spender,
    "top_location_far": top_location_far,
    "how_to_get_discount_value": how_to_get_discount_value,
    "how_to_get_price_product": how_to_get_price_product,
    "recommendations_packet_bundling": recommendations_packet_bundling,
}

def exp_ask_ai(user_message: str, history: list = []):
    # Step 1: Cari function yang relevan via vector search
    relevant_fns = find_relevant_function(user_message, n_results=2)
    print(f"[Vector Search] Relevant functions: {relevant_fns}")

    # Step 2: Jalankan function yang relevan
    context_data = {}
    for fn_name in relevant_fns:
        fn = available_functions.get(fn_name)
        if fn:
            context_data[fn_name] = fn()

    # Step 3: Kirim data + pertanyaan ke AI
    messages = [
        {
            "role": "system",
            "content": f"You are a senior data analyst. Use this data to answer: {str(context_data)}"
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Step 4: Stream jawaban
    stream = ollama.chat(
        model='llama3.2:latest',
        messages=messages,
        stream=True
    )
    for chunk in stream:
        yield chunk['message']['content']
