from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from utils.utils import beetoon_api
import requests
import json
mydb = beetoon_api(host='localhost',user='root',password="S@1989", db='crawl_beetoon')
app = Flask(__name__)


# Danh sach tat ca category
@app.route("/manga/categories", methods=["GET"])
def get_categories():
    order_by = request.args.get('order_by', 'id')
    sort_direction = request.args.get('sort_direction', 'asc')
    search_text = request.args.get('search_text', '')
    data = mydb.get_categories()
    return jsonify(data)

# Danh sach manga theo category id
@app.route("/manga/categories/<int:category_id>")
def get_category_by_id(category_id):
    data = mydb.get_category_by_id(category_id)

    return jsonify(data)
# Danh sach tat ca manga
@app.route("/manga", methods=["GET"])
def get_manga():
    data = mydb.get_from_manga()
    comics = data["data"]
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_comics = comics[start_index:end_index]
    data['data'] = sliced_comics
    
    return jsonify(data)

# Chi tiet manga theo ID
@app.route("/manga/<int:manga_id>", methods = ['GET'])
def get_manga_by_id(manga_id):
    data = mydb.get_manga_by_id(manga_id)
    return jsonify(data)

# Danh sach chapter theo manga id
@app.route("/manga/<int:manga_id>/chapter", methods = ['GET'])
def get_chapter_list_by_manga(manga_id):
    data = mydb.get_chapter_list_by_manga(manga_id)
    return jsonify(data)

# Chi tiet chapter theo id
@app.route("/manga/<int:manga_id>/chapter/chapter-<int:chapter_id>", methods = ['GET'])
def get_chapter_by_id(manga_id, chapter_id):
    data = mydb.get_chapter_by_id(manga_id, chapter_id)
    return jsonify(data)

@app.route("/hello", methods=["GET"])
def get_new():
    return jsonify({"data":"hi"})


# api.add_resource({"data": "Hello World"}, "/hello")

if __name__ == "__main__":
   app.run(host='0.0.0.0')