from flask import Flask, jsonify, request
from utils import get_article_content
from settings import RSS_FEEDS
from flask_cors import CORS
import random
import json
import os
from recommend_article import RecommendArticles

app = Flask(__name__)
CORS(app)

file_name = "train_data.csv"
Repo = RecommendArticles(file_name=file_name)

# check file train_data is exists
if not os.path.exists(file_name):
    Repo.get_train_data()

print("Train model")
Repo.train_model()


@app.route("/api/category", methods=["GET"])
def get_all_category():
    return jsonify(RSS_FEEDS)


@app.route("/api/get_article", methods=["GET"])
def get_article_url():
    url = request.args.get("url")
    data = get_article_content(url)
    return jsonify({"data": data})


@app.route("/api/get_recommend", methods=["POST"])
def get_random_article():
    body = request.get_json()
    links = body.get("links")
    current_link = body.get("current_link")
    if not links:
        return jsonify({"error": "Invalid request"}), 400
    recommended_articles = Repo.recommend(links, 20)
    if current_link:
        recommended_articles = recommended_articles.loc[
            recommended_articles["link"] != current_link
        ]
    len_recommend = len(recommended_articles.index)
    if len_recommend == 0:
        return jsonify({"data": {}})
    # random 1 recommended article
    rand_index = random.randint(0, len_recommend - 1)
    result = recommended_articles.iloc[rand_index]
    result = json.loads(result.to_json())
    return jsonify({"data": result})


if __name__ == "__main__":
    app.run(port=5001, debug=True)
