"""int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""


from flask import Blueprint, request, jsonify
from app.database.factory import DatabaseFactory, DatabaseType
from app.crawler.factory import CrawlerFactory, CrawlerType
import multiprocessing
from llama_cpp import Llama
from config import Config

index_url_bp = Blueprint("index_url", __name__)

db = DatabaseFactory.create_database(DatabaseType.IN_MEMORY)


llm = Llama(
    model_path=Config.MODEL_PATH,
        n_ctx=Config.MODEL_CTX_SIZE,
        embedding=True,
)

@index_url_bp.route("/index_url", methods=["POST"])
def index_url():
    """
    This endpoint expects a URL in the format
    {"url": "https://www.example.com"}
    and is responsible for:
    1. instantiating the web-crawler that will extract the webpage's content
    2. store the output into a generic database.

    Args:
        url (str): The website URL for which you want to interact with.

    Example:
        One can send a POST request to where this is hosted as::

            $ curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:4000/v1/index_url

    Todo:
        * make async pool

    """
    data = request.json

    website_url = data.get("url")

    # Extract and process content
    crawler = CrawlerFactory.create_crawler(CrawlerType.STATIC, website_url)
    content = crawler.extract_content()

    # Store contents of the indexed URLs to database

    db.add_url(website_url, content)

    # break content into chunks of N tokens tops
    tokens = llm.tokenize(content.encode('utf-8'))
    chunks = split_into_max_tokens(tokens, max_chunk_size=Config.MAX_TOKENS, intersection=Config.CHUNK_INTERSECTION)

    chunked_content = content

    with multiprocessing.Pool(processes=Config.N_PROCESSES) as pool:
        response = pool.map(get_embeddings, chunks)

    return jsonify(
        {
            "message": f"URL {website_url} has been indexed with {len(content)} letters."
        }
    )

def get_embeddings(chunk):
    text = llm.detokenize(chunk)
    embedding = llm.create_embedding(str(text))['data'][0]['embedding']
    db.add_embeddings(text, embedding)

    return

def split_into_max_tokens(tokens, max_chunk_size=1024, intersection=0):
    chunks = []
    start_index = 0
    while start_index < len(tokens):
        end_index = start_index + max_chunk_size
        chunk = tokens[start_index:end_index]
        chunks.append(chunk)
        start_index += max_chunk_size - intersection
    return chunks
