from flask import Flask, request, Response, stream_with_context, render_template
from services.collections.analyst import ask_analyst
from services.collections.anime import ask_anime
import ollama

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    # Step 1: Router dulu, TIDAK di-stream
    domain = detect_domain(user_message)
    print(f"[Router] Domain: {domain}")

    # Step 2: Pilih handler yang tepat
    if domain == "analyst":
        handler = ask_analyst(user_message)
    elif domain == "anime":
        handler = ask_anime(user_message)
    else:
        def handler():
            yield "Maaf, saya tidak mengerti pertanyaan kamu."
        handler = handler()

    def generate():
        for chunk in handler:
            yield f"data: {chunk}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


def detect_domain(user_message: str) -> str:
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {
                "role": "system",
                "content": """Kamu adalah router. Tentukan domain dari pertanyaan user.
                Jawab HANYA dengan satu kata:
                - 'analyst' jika tentang data penjualan, diskon, customer, produk
                - 'anime' jika tentang anime, manga, karakter anime
                - 'unknown' jika tidak tahu"""
            },
            {"role": "user", "content": user_message}
        ]
    )
    return response['message']['content'].strip().lower()
