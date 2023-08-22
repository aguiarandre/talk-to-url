import multiprocessing
from tqdm import tqdm
from numpy import dot, linalg
from llama_cpp import Llama
from flask import Blueprint, request, jsonify
from .index_url import llm, db


ask_question_bp = Blueprint("ask", __name__)

def cosine_similarity(vec_a, vec_b):
    """
    Measures the cosine angle between vector A and vector B.
    """
    cos = dot(vec_a, vec_b) / (linalg.norm(vec_a) * linalg.norm(vec_b))
    return cos



@ask_question_bp.route("/ask", methods=["POST"])
def ask_question():
    """
    This endpoint expects an input body in the form {"url":"https://www.example.com/", "question":"what is your name?"}


    :type question: string
    Args:
        url (str): The website URL for which you want to interact with.
        question (str): The question you want the LLM to answer based on the URL.

    Example:
        One can send a POST request to where this is hosted as::

            $ curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com", "question":"What is the purpose of this domain?"}' http://localhost:4000/v1/ask

    Todo:
        * ...

    .. http:post:: /v1/(string:url)

        **Example request**:

        .. sourcecode:: http

            POST /v1/index_url
            Content-Type: application/json

            {
                "url": "https://www.example.com",
                "question":"what is the purpose of this domain?"
            }

    """
    # collect input
    data = request.json
    website_url = data.get("url")
    question = data.get("question")

    # retrieve indexed url
    content = db.get_url(website_url)

    if website_url not in db.list_urls():
        return jsonify({"error": f"URL {website_url} has not been indexed."})

    prompt_embedding = llm.create_embedding(question)['data'][0]['embedding']

    # calculate embeddings and cosine similarity for each chunk
    chunked_content = content
    max_similarity = -float('inf')
    for text, embedding in tqdm(db.embedding_map.values()):
        cos = cosine_similarity(prompt_embedding, embedding)
        if cos > max_similarity:
            max_similarity = cos
            chunked_content = text

    prompt = f"Given the following content: '{chunked_content}', {question}"
    output = llm(prompt)

    return jsonify({"response": output})
