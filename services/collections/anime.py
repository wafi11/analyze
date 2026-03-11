import requests
import chromadb
import ollama

client = chromadb.Client()
animeCollection = client.get_or_create_collection("anime-functions")
def get_anime():
    base_url = "https://api.jikan.moe/v4"
    response = requests.get(f"{base_url}/random/anime")

    if response.status_code == 200:
        res = response.json()
        titles = res.get("data", {}).get("titles", [])
        
        data = [t["title"] for t in titles]
        print("title : ",data)
        return data
    else:
        return []
    

def store_anime_to_collection(anime_id: str, titles: list):
    if titles:
        animeCollection.upsert(
            ids=[anime_id],
            documents=[", ".join(titles)],
            metadatas=[{"titles": ", ".join(titles)}]
        )

def find_relevant_function(user_message: str, n_results: int = 2):
    results = animeCollection.query(
        query_texts=[user_message],
        n_results=n_results
    )
    return [meta["name"] for meta in results["metadatas"][0]]


available_functions = {
    "get_anime": get_anime,
}

def ask_anime(user_message: str):
    relevant_fns = find_relevant_function(user_message, n_results=2)
    
    context_data = {}
    for fn_name in relevant_fns:
        fn = available_functions.get(fn_name)
        if fn:
            context_data[fn_name] = fn()

    messages = [
        {"role": "system", "content": f"You are an anime expert. Use this data: {str(context_data)}"},
        {"role": "user", "content": user_message}
    ]

    stream = ollama.chat(model='llama3.2:latest', messages=messages, stream=True)
    for chunk in stream:
        yield chunk['message']['content']


