from flask import Blueprint, request, jsonify
from app.utils.content_extraction import indexed_urls
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

ask_question_bp = Blueprint("ask", __name__)


@ask_question_bp.route("/ask", methods=["POST"])
def ask_question():
    """
    Docstring goes here
    """
    data = request.json
    website_url = data.get("url")
    prompt = data.get("prompt")

    if website_url not in indexed_urls:
        return jsonify({"error": f"URL {website_url} has not been indexed."})

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt} within {website_url}."},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation
    )

    reply = response.choices[0].message["content"]

    return jsonify({"response": reply})
