from flask import Blueprint, request, jsonify
import openai
from dotenv import load_dotenv
import os
from .index_url import db
from llama_cpp import Llama

LLM = Llama(
    model_path="D:/Users/andreaguiar/llm/llama-2-7b-chat.ggmlv3.q2_K.bin", n_ctx=4096
)

load_dotenv()

# openai.api_key = os.environ.get("OPENAI_API_KEY")

ask_question_bp = Blueprint("ask", __name__)


@ask_question_bp.route("/ask", methods=["POST"])
def ask_question():
    """
    Docstring goes here
    """
    data = request.json
    website_url = data.get("url")
    question = data.get("question")

    content = db.get_url(website_url)

    if website_url not in db.list_urls():
        return jsonify({"error": f"URL {website_url} has not been indexed."})

    prompt = f"Given the following content: '{content}', {question}"

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"},
    ]
    output = LLM(prompt)

    # display the response
    print(output["choices"][0]["text"])
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo", messages=conversation
    # )

    # reply = response.choices[0].message["content"]

    return jsonify({"response": output["choices"][0]["text"]})
