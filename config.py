import logging
from logging.handlers import RotatingFileHandler
import os

class Config:
    N_PROCESSES = 2

    # CONTEXT WINDOW LENGTH
    MAX_TOKENS = 512
    CHUNK_INTERSECTION = 20
    CHUNKS_STACKED = 6

    # LLAMA CONFIG
    APP_PATH = "/Users/andreaguiar/Desktop/usr/dev/llm/talk-to-url/"
    MODEL_PATH = "/Users/andreaguiar/Desktop/usr/dev/llm/talk-to-url/data/llama-2-7b-chat.ggmlv3.q2_K.bin"

    MODEL_CTX_SIZE = 4096

    # EMBEDDINGS
    INSTRUCTOR_MODEL = 'hkunlp/instructor-xl'

# logger config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler('/Users/andreaguiar/Desktop/usr/dev/llm/talk-to-url/log/app.log', maxBytes=1024 * 1024, backupCount=3)

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
