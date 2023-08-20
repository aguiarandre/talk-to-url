from flask import Blueprint, request, jsonify
from app.utils.content_extraction import WebsiteCrawler
from app.database.factory import DatabaseFactory, DatabaseType

index_url_bp = Blueprint("index_url", __name__)

db = DatabaseFactory.create_database(DatabaseType.IN_MEMORY)


@index_url_bp.route("/index_url", methods=["POST"])
def index_url():
    data = request.json
    website_url = data.get("url")
    crawler = WebsiteCrawler(website_url)
    # Extract and process content
    content = crawler.extract_content()

    # Store contents of the indexed URLs to database
    db.add_url(website_url, content)

    return jsonify(
        {
            "message": f"URL {website_url} has been indexed with {len(content)} letters.",
            "urls": ",".join(db.list_urls()),
        }
    )
