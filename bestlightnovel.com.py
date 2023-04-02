from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/home", methods=["GET"])
def get_home():
    session = requests.Session()
    rManga_base = session.get('https://bestlightnovel.com/')
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    manga_data_list = []
    for item in soup.findAll('div', class_='item'):
        manga_data = dict()
        manga_data['manga-title'] = item.find('div', class_='slide-caption').find('a').text.strip()
        manga_data['manga-link'] = item.find('div', class_='slide-caption').find('a').get('href')
        manga_data['manga-chapter-title'] = item.find('div', class_='slide-caption').find_all('a')[1].text.strip()
        manga_data['manga-chapter-link'] = item.find('div', class_='slide-caption').find_all('a')[1].get('href')
        manga_data['manga-poster'] = item.find('img').get('src')
        manga_data_list.append(manga_data)

    return jsonify(manga_data_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1986)
