from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Dictionary to store indexed URLs and their content
indexed_urls = {}


@app.route("/index_url", methods=["POST"])
def index_url():
    print("You entered index_url")
    data = request.json
    website_url = data.get("url")
    print(website_url)
    # Fetch and process website content here
    # You can use libraries like 'requests' or 'BeautifulSoup'

    # Store the indexed content in the dictionary
    indexed_urls[website_url] = {"content": "Processed content goes here"}

    return jsonify({"message": f"URL {website_url} has been indexed."})


@app.route("/ask", methods=["POST"])
def ask_question():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)

# docker run -p 4000:80 --mount type=bind,source="$(pwd)"/app,target=/llm findly-api
