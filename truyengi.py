from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from bs4 import BeautifulSoup

app = Flask(_name_)

@app.route("/home", methods=["GET"])
def ManHome():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/index.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName2, itemName3, itemName4 in zip(soupManga_base.find_all('span', class_='title'), soupManga_base.find_all('a', class_='cw-list-item'), soupManga_base.find_all('span', class_='chapter-link')):
        if count >= 8:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = {}
        JsonManga['name_manga'] = itemName2.text.strip()
        JsonManga['url_manga'] = itemName3.get('href')
        JsonManga['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga['chapter_manga'] = itemName4.a.get('href')
        listJsonManga.append(JsonManga)
        count += 1
    count = 0
    son = {"ngontinh":listJsonManga}
    return jsonify(son)

@app.route("/ngontinhmoi", methods=["GET"])
def get_NgonTinhMoi():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/index.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main-hd'):
        if count >= 1:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = dict()
        JsonManga = itemName1.find('h3').text
        listJsonManga.append(JsonManga)
        count += 1
    count = 0  # đếm số lượng truyện đã tìm được
    for itemName2, itemName3, itemName4 in zip(soupManga_base.find_all('span', class_='title'), soupManga_base.find_all('a', class_='cw-list-item'), soupManga_base.find_all('span', class_='chapter-link')):
        if count >= 8:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = {}
        JsonManga['name_manga'] = itemName2.text.strip()
        JsonManga['url_manga'] = itemName3.get('href')
        JsonManga['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga['chapter_manga'] = itemName4.a.get('href')
        listJsonManga.append(JsonManga)
        count += 1
    count = 0
    return jsonify(listJsonManga)

@app.route("/truyen18moi", methods=["GET"])
def get_Truyen18Moi():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/index.html') 
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main-hd')[1:]:
        if count >= 1:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = dict()
        JsonManga['name'] = itemName1.find('h3').text
        listJsonManga.append(JsonManga)
        count += 1
    count = 0  # đếm số lượng truyện đã tìm được
    for itemName2, itemName3, itemName4 in zip(soupManga_base.find_all('span', class_='title')[8:], soupManga_base.find_all('a', class_='cw-list-item')[8:], soupManga_base.find_all('span', class_='chapter-link')[8:]):
        if count >= 8:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = {}
        JsonManga['name_manga'] = itemName2.text.strip()
        JsonManga['url_manga'] = itemName3.get('href')
        JsonManga['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga['chapter_manga'] = itemName4.a.get('href')
        listJsonManga.append(JsonManga)
        count += 1
    count = 0
    return jsonify(listJsonManga)

@app.route("/tieuthuyetmoi", methods=["GET"])
def get_TieuThuyetMoi():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/index.html') 
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main-hd')[2:]:
        if count >= 1:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = dict()
        JsonManga['name'] = itemName1.find('h3').text
        listJsonManga.append(JsonManga)
        count += 1
    count = 0  # đếm số lượng truyện đã tìm được
    for itemName2, itemName3, itemName4 in zip(soupManga_base.find_all('span', class_='title')[16:], soupManga_base.find_all('a', class_='cw-list-item')[16:], soupManga_base.find_all('span', class_='chapter-link')[16:]):
        if count >= 8:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = {}
        JsonManga['name_manga'] = itemName2.text.strip()
        JsonManga['url_manga'] = itemName3.get('href')
        JsonManga['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga['chapter_manga'] = itemName4.a.get('href')
        listJsonManga.append(JsonManga)
        count += 1
    count = 0
    return jsonify(listJsonManga)

@app.route("/truyenmoi", methods=["GET"])
def get_TruyenMoi():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/index.html') 
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main-hd')[3:]:
        if count >= 1:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = dict()
        JsonManga['name'] = itemName1.find('h3').text
        listJsonManga.append(JsonManga)
        count += 1
    count = 0  # đếm số lượng truyện đã tìm được
    for itemName2, itemName3, itemName4 in zip(soupManga_base.find_all('span', class_='title')[24:], soupManga_base.find_all('a', class_='cw-list-item')[24:], soupManga_base.find_all('span', class_='chapter-link')[24:]):
        if count >= 16:  # nếu đã tìm đủ 8 truyện thì thoát vòng lặp
            break
        JsonManga = {}
        JsonManga['name_manga'] = itemName2.text.strip()
        JsonManga['url_manga'] = itemName3.get('href')
        JsonManga['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga['chapter_manga'] = itemName4.a.get('href')
        listJsonManga.append(JsonManga)
        count += 1
    count = 0
    return jsonify(listJsonManga)


if _name_ == "_main_":
   app.run(host='0.0.0.0', port=2342)