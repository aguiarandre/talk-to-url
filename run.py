from flask import Flask
from app.api.routes.index_url import index_url_bp
from app.api.routes.ask import ask_question_bp

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(index_url_bp, url_prefix="/v1")
    app.register_blueprint(ask_question_bp, url_prefix="/v1")
    app.run(host="0.0.0.0", port=4000)

# docker run -p 4000:80 --mount type=bind,source="$(pwd)"/app,target=/llm findly-api
# curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:4000/index_url
# docker exec -it findly //bin//sh
