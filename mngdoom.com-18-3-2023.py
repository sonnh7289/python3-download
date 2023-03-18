from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = Flask(__name__)

#LẤY PHÂN LOẠI TRANG MANGA
@app.route("/home", methods=["GET"])
def get_Home():
    link_full = request.headers.get('Link-Full')
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get(link_full)
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

    return listJsonManga

#LẤY CHI TIẾT THÔNG TIN MANGA
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
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
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Categories:':
                FullDetailManga['Categories'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Type'] = alt.text.strip()
            index+=1

        #LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Author:':
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

#LẤY PHÂN LOẠI TRANG MANGA
@app.route("/directory", methods=["GET"])
def get_Directory():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listDirectory = []

    for itemMangaDirectory in soupManga_base.findAll('a', class_='manga-info-qtip'):
        ItemDirectory = dict()

        # LẤY TÊN
        ItemDirectory['name_manga'] = itemMangaDirectory.text.strip()

        # LẤY LINK
        ItemDirectory['full_manga'] = itemMangaDirectory['href']

        # LẤY POSTER
        ItemDirectory['data_manga'] = itemMangaDirectory['data-info']

        
        listDirectory.append(ItemDirectory)
        
    return listDirectory


#LẤY MANGA PHỔ BIẾN
@app.route("/popular", methods=["GET"])
def get_Popular():
    link_full = request.headers.get('Link-Full')
    listPopularManga = []
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    # index=0

    for meta in soupManga_base.findAll('div', class_='row manga-list-style'):
        ItemPopularManga = dict()

        ItemPopularManga['link'] = meta.a['href']

        ItemPopularManga['poster'] = meta.img['src']

        ItemPopularManga['Name'] = meta.a['title']
        index = 0
        index+=1

        #LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Alternative Name:':
                ItemPopularManga['Alternative Name'] = meta.findAll('dd')[index].text.strip()
            index+=1
        
        #LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Status:':
                ItemPopularManga['Status'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Categories:':
                ItemPopularManga['Categories'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                ItemPopularManga['Type'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Author:':
                ItemPopularManga['Author'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Artist:':
                ItemPopularManga['Artist'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY SỐ VIEW
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Total Views:':
                ItemPopularManga['Total Views'] = meta.findAll('dd')[index].text.strip()
            index+=1

        listPopularManga.append(ItemPopularManga)

    return listPopularManga


@app.route("/genres", methods=["GET"])
def get_Genres():
    link_full = request.headers.get('Link-Full')
    listGenresManga = []
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')


    for meta in soupManga_base.findAll('dl', class_='dl-horizontal'):
        
        index = 0
        index += 1
        ItemGenresManga = dict()

        ItemGenresManga['link'] = meta.a['href']

        ItemGenresManga['Name'] = meta.a['title']

        #LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Alternative Name:':
                ItemGenresManga['Alternative Name'] = meta.findAll('dd')[index].text.strip()
            index+=1
        
        #LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Status:':
                ItemGenresManga['Status'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Categories:':
                ItemGenresManga['Categories'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                ItemGenresManga['Type'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Author:':
                ItemGenresManga['Author'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Artist:':
                ItemGenresManga['Artist'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY SỐ VIEW
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Total Views:':
                ItemGenresManga['Total Views'] = meta.findAll('dd')[index].text.strip()
            index+=1

        listGenresManga.append(ItemGenresManga)

    return listGenresManga

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=5001)