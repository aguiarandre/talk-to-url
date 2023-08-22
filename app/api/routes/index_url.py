"""int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""


from flask import Blueprint, request, jsonify
from app.database.factory import DatabaseFactory, DatabaseType
from app.crawler.factory import CrawlerFactory, CrawlerType
import multiprocessing
from llama_cpp import Llama
import logging
from config import Config
from InstructorEmbedding import INSTRUCTOR

logger = logging.getLogger(__name__)
index_url_bp = Blueprint("index_url", __name__)

logger.info(f'Initializing Database')
db = DatabaseFactory.create_database(DatabaseType.IN_MEMORY)

logger.info(f'Initializing Instructor model for embeddings')
model = INSTRUCTOR(Config.INSTRUCTOR_MODEL)

logger.info(f'Initializing LLM at {Config.MODEL_PATH} with {Config.MODEL_CTX_SIZE}')
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
    logger.info(f'Indexing {website_url}')

    # Extract and process content
    crawler = CrawlerFactory.create_crawler(CrawlerType.STATIC, website_url)
    content = crawler.extract_content()
    logger.info(f'{website_url} content extracted: {len(content)} words')

    # Store contents of the indexed URLs to database

    db.add_url(website_url, content)
    logger.info(f'{website_url} added to DB')

    # break content into chunks of N tokens tops
    tokens = llm.tokenize(content.encode('utf-8'))
    logger.info(f'{website_url} has {len(tokens)}')

    chunks = split_into_max_tokens(tokens, max_chunk_size=Config.MAX_TOKENS, intersection=Config.CHUNK_INTERSECTION)
    logger.info(f'{website_url} was separated into {len(chunks)}')

    chunked_content = content

    with multiprocessing.Pool(processes=Config.N_PROCESSES) as pool:
        responses = pool.map(get_embeddings, chunks)

    for t, embed in responses:
        db.add_embeddings(t, embed)
    logger.info(f'{website_url} has embeddings stored in DB with {len(db.embedding_map.keys())} keys')

    return jsonify(
        {
            "message": f"URL {website_url} has been indexed. {len(content)} letters was divided into {len(db.embedding_map.keys())} chunks."
        }
    )

def get_embeddings(chunk):
    text = llm.detokenize(chunk)
    instruction = "Represent the webpage text:"
    embedding = model.encode([[instruction,str(text)]])

    return (text, embedding)

def split_into_max_tokens(tokens, max_chunk_size=1024, intersection=0):
    chunks = []
    start_index = 0
    while start_index < len(tokens):
        end_index = start_index + max_chunk_size
        chunk = tokens[start_index:end_index]
        chunks.append(chunk)
        start_index += max_chunk_size - intersection
    return chunks
