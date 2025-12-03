import os
import time
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS 
from langchain_agent import get_agent_response

load_dotenv()
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Allow CORS for all origins during development and GitHub Pages testing
# Later you can restrict origins if needed.
CORS(app, resources={r"/api/*": {"origins": "*"}})   # <-- ADD THIS

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "empty message"}), 400

    try:
        bot_reply = generate_reply(user_message)
    except Exception as e:
        bot_reply = f"Sorry, an error occurred: {str(e)}"

    return jsonify({"reply": bot_reply})

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def generate_reply(prompt: str) -> str:
    """Generate a reply using LangChain agent with memory"""
    try:
        response = get_agent_response(prompt)
        return response
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


if __name__ == "__main__":
    # Render expects the PORT env var
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
