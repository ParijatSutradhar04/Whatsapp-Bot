import google.generativeai as genai
import os
import time
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "empty message"}), 400

    # Quick reply echo while we call Gemini — this makes the UI feel snappy.
    # Replace generate_reply() with your working Gemini API function.
    try:
        bot_reply = generate_reply(user_message)
    except Exception as e:
        # Fallback reply for debugging
        bot_reply = f"Sorry, an error occurred: {str(e)}"

    return jsonify({"reply": bot_reply})

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def generate_reply(prompt: str) -> str:
    """Generate a reply using Gemini API"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

if __name__ == "__main__":
    # run in debug for development, use proper server for production
    app.run(host="0.0.0.0", port=8501, debug=True)
