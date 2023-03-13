from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

#LẤY PHÂN LOẠI TRANG MANGA
@app.route("/home", methods=["GET"])
def get_Home():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://www.mngdoom.com/')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    for itemMangaLastUpdate in soupManga_base.findAll('dl'):
        ItemJsonManga = dict()

        # LẤY TÊN
        ItemJsonManga['name_manga'] = itemMangaLastUpdate.a['title']

        # LẤY LINK
        ItemJsonManga['full_manga'] = itemMangaLastUpdate.a['href']

        # LẤY POSTER
        ItemJsonManga['poster_manga'] = itemMangaLastUpdate.img['src']

        # LÁY THỜI GIAN CẬP NHẬT
        ItemJsonManga['time_update'] = itemMangaLastUpdate.find('span', class_='time hidden-xs').text.strip()
        
        listJsonManga.append(ItemJsonManga)
        print(ItemJsonManga)
    return listJsonManga

#LẤY CHI TIẾT THÔNG TIN MANGA
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = requests.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    FullDetailManga = dict()
    index = 0

    for meta in soupManga_base.findAll('dl', class_='dl-horizontal'):
        
        #LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Alternative Name:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Alternative Name'] = alt.text.strip()
            index+=1
        
        #LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Status:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Status'] = alt.text.strip()
            index+=1

        #LẤY THỂ LOẠI
        FullDetailManga['Categories'] = meta.findAll('dd')[index].text.strip()
        index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Type'] = alt.text.strip()
            index+=1

        #LẤY TÁC GIẢ
        FullDetailManga['Author'] = meta.findAll('dd')[index].text.strip()
        index+=1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Artist:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Artist'] = alt.text.strip()
            index+=1

        # LẤY SỐ VIEW
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Total Views:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Total Views'] = alt.text.strip()
            index+=1

    # LẤY GIỚI THIỆU TRUYỆN
    FullDetailManga['info'] = soupManga_base.find('div', class_='note note-default margin-top-15').find('span').text.strip()

    return FullDetailManga

#LẤY ẢNH CHAPTER
@app.route('/chapter', methods=['GET'])
def get_chapter():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    num_img = []
    for num in soup.findAll('img', class_='img-responsive'):
        num_img.append(num.get('src').strip())
    img = {}
    img['image'] = num_img
    
    return img



if __name__ == "__main__":
   app.run(host='0.0.0.0',port=2003)