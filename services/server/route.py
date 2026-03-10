from flask import Flask, request, Response, stream_with_context, render_template
from config.ai import exp_ask_ai

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    def generate():
        for chunk in exp_ask_ai(user_message):
            yield f"data: {chunk}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")