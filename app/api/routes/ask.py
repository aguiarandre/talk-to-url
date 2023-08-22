import multiprocessing
from tqdm import tqdm
from numpy import dot, linalg
import json
import heapq
from config import Config, logger
import logging
from flask import Blueprint, request, jsonify, Response, stream_with_context
from .index_url import llm, db, model

ask_question_bp = Blueprint("ask", __name__)
# logger = logging.getLogger(__name__)

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
        * Add response streaming feature

    """
    # collect input
    data = request.json
    website_url = data.get("url")
    question = data.get("question")

    # retrieve indexed url
    content = db.get_url(website_url)
    logger.info(f'Preparing to compare prompt against {len(db.embedding_map.values())} chunks...')

    if website_url not in db.list_urls():
        return jsonify({"error": f"URL {website_url} has not been indexed."})

    instruction = "Represent the webpage question:"
    prompt_embedding = model.encode([[instruction,question]])

    logger.info(f'Embedding prompt for comparison against chunks')
    # use priority queue to grab top Config.CHUNKS_STACKED ordered by cosine similarity

    top_k_chunks = []

    for text in tqdm(db.embedding_map.keys()):
        embed_chunk = db.get_embeddings(text)
        cos = cosine_similarity(prompt_embedding[0], embed_chunk[0])
        heapq.heappush(top_k_chunks, (-cos, text))

    top_similarities = list(map(lambda x : x[0], top_k_chunks[:Config.CHUNKS_STACKED]))
    logger.info(f'Best cosine similarities are: {top_similarities}')

    n = 0
    chunked_content = ''
    while n < Config.CHUNKS_STACKED and len(top_k_chunks):
        (_, text) = heapq.heappop(top_k_chunks)
        chunked_content += '\n' + str(text)
        n += 1
    logger.info(f'Stacked {n} chunks together')
    logger.info(f'Total number of letters stacked: {len(chunked_content)}')
    logger.info(f'Total number of tokens stacked: {len(llm.tokenize(chunked_content.encode("utf-8")))}')

    prompt = f"""Using only information from the following piece text, answer the question.
     Don't make up any information. If you can't find the answer, simply state "Could not find the answer".
     Only use information from the piece of text.
     Context:'{chunked_content}'
     Question: {question}
     Only return the helpful answer below and nothing else.
     Answer:"""

    logger.info(f'Entire prompt used: {prompt}')
    output = llm(prompt, stop=["Q:", "\n"], echo=True)
    # stream = llm(
    #     prompt,
    #     max_tokens=48,
    #     stop=["Q:", "\n"],
    #     stream=True,
    # )
    answer = output['choices'][0]['text']
    logger.info(f'Answer: {answer}')
    # return Response(stream_with_context(generate_text_response(stream)), content_type='text/plain')
    # return jsonify({"response": stream})
    return jsonify({"response": answer})

def generate_text_response(stream):
    for output in stream:
        yield output['choices'][0]['text']
