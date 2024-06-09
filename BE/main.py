from flask import Flask, jsonify, request
from utils import get_article_content
from settings import RSS_FEEDS
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

@app.route('/api/category', methods=['GET'])
def get_all_category():
    return jsonify(RSS_FEEDS)

@app.route('/api/get_article', methods=['GET'])
def get_article_url():
    url = request.args.get('url')
    data = get_article_content(url)
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=1111,debug=True)
