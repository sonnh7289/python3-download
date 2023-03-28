from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = Flask(__name__)

# LẤY PHÂN LOẠI TRANG MANGA


@app.route("/home", methods=["GET"])
def get_Home():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga = dict()
    listJsonManga['HotUpdate'] = []
    for itemMangaLastUpdate in soupManga_base.findAll('div', class_='item'):
        ItemJsonManga = dict()

        # LẤY TÊN
        ItemJsonManga['name_chapter_update'] = itemMangaLastUpdate.a['title']

        # LẤY LINK
        ItemJsonManga['link_chap_update'] = itemMangaLastUpdate.a['href']

        # LẤY POSTER
        ItemJsonManga['poster_manga'] = itemMangaLastUpdate.img['src']

        listJsonManga['HotUpdate'].append(ItemJsonManga)

    listJsonManga['Latest'] = []
    for itemMangaLastUpdate in soupManga_base.findAll('dl'):

        Popular = dict()
        # print(itemMangaLastUpdate)
        for itemManga in itemMangaLastUpdate.findAll('div', class_='manga-cover'):
            # LẤY TÊN
            Popular['name'] = itemManga.find('a').get('title')

            # LẤY LINK
            Popular['link_chap_update'] = itemMangaLastUpdate.a['href']

            # LẤY POSTER
            Popular['poster_manga'] = itemMangaLastUpdate.img['src']

            Popular['time_update'] = itemMangaLastUpdate.find(
                'span', class_='time hidden-xs').text.strip()

            # LẤY CÁC CHAPTER
            Popular['list_chapter'] = []
        for cha in itemMangaLastUpdate.findAll('dd'):
            chapter = {}
            chapter['link_chapter'] = cha.find('a').get('href')
            chapter['name_chapter'] = cha.a.text.strip()
            Popular['list_chapter'].append(chapter)

        listJsonManga['Latest'].append(Popular)

    listJsonManga['Popular_Manga'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-post-list list-numbering'):
        for PopularManga in ul.findAll('div', class_='caption'):
            itemPopularManga = dict()
            index = 0
            for p in PopularManga.findAll('p', class_='category'):
                # LẤY TÊN MANGA
                itemPopularManga['name_manga'] = p.text.strip()

                # LẤY LINK MANGA
                itemPopularManga['link_manga'] = p.a['href']

            for h5 in PopularManga.findAll('h5', class_='post-title'):
                # LẤY TÊN CHAPTER
                itemPopularManga['name_chapter'] = h5.text.strip()

                # LẤY LINK CHAPTER
                itemPopularManga['link_chapter'] = h5.a['href']

            for p1 in PopularManga.findAll('p', class_='post-meta'):
                # LẤY THỜI GIAN
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['time'] = p11.text.strip()
                index += 1

                # LẤY SỐ VIEW
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['view'] = p11.text.strip()
                index += 1

                listJsonManga['Popular_Manga'].append(itemPopularManga)
    return listJsonManga


@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    FullDetailManga = dict()
    ListDetailManga = []
    index = 0

    for meta in soupManga_base.findAll('dl', class_='dl-horizontal'):

        # LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Alternative Name:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Alternative Name'] = alt.text.strip()
            index += 1

        # LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Status:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Status'] = alt.text.strip()
            index += 1

        # LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Categories:':
                FullDetailManga['Categories'] = meta.findAll('dd')[
                    index].text.strip()
            index += 1

        # LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Type :':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Type'] = alt.text.strip()
            index += 1

        # LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Author:':
                FullDetailManga['Author'] = meta.findAll(
                    'dd')[index].text.strip()
            index += 1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Artist:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Artist'] = alt.text.strip()
            index += 1

        # LẤY SỐ VIEW
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Total Views:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Total Views'] = alt.text.strip()
            index += 1
    # LẤY GIỚI THIỆU TRUYỆN
    if soupManga_base.find('div', class_='note note-default margin-top-15') is not None:
        FullDetailManga['info'] = soupManga_base.find(
            'div', class_='note note-default margin-top-15').text.strip()

    FullDetailManga['list_chapter'] = []
    for cha in soupManga_base.findAll('ul', class_='chapter-list'):
        for chap in cha.findAll('li'):
            chapter = {}
            chapter['link_chapter'] = chap.find('a').get('href')
            if chap.find('span', class_='val') is not None:
                chapter['name_chapter'] = chap.find(
                    'span', class_='val').text.strip()
            if chap.find('span', class_='date') is not None:
                chapter['release_date'] = chap.find(
                    'span', class_='date').text.strip()
            FullDetailManga['list_chapter'].append(chapter)

    ListDetailManga.append(FullDetailManga)

    return ListDetailManga

# LẤY ẢNH CHAPTER


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
        index += 1

        # LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Alternative Name:':
                ItemPopularManga['Alternative Name'] = meta.findAll('dd')[
                    index].text.strip()
            index += 1

        # LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Status:':
                ItemPopularManga['Status'] = meta.findAll(
                    'dd')[index].text.strip()
            index += 1

        # LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Categories:':
                ItemPopularManga['Categories'] = meta.findAll('dd')[
                    index].text.strip()
            index += 1

        # LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Type :':
                ItemPopularManga['Type'] = meta.findAll(
                    'dd')[index].text.strip()
            index += 1

        # LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Author:':
                ItemPopularManga['Author'] = meta.findAll(
                    'dd')[index].text.strip()
            index += 1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Artist:':
                ItemPopularManga['Artist'] = meta.findAll(
                    'dd')[index].text.strip()
            index += 1

        # LẤY SỐ VIEW
        for head in soupManga_base.findAll('dt')[index]:
            if head.text.strip() == 'Total Views:':
                ItemPopularManga['Total Views'] = meta.findAll('dd')[
                    index].text.strip()
            index += 1

        listPopularManga.append(ItemPopularManga)

    return listPopularManga


@app.route("/latest-chapters", methods=["GET"])
def get_LatestChapters():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    # index=0

    listJsonManga = []
    for itemMangaLastUpdate in soupManga_base.findAll('dl'):

        Popular = dict()
        # print(itemMangaLastUpdate)
        for itemManga in itemMangaLastUpdate.findAll('div', class_='manga-cover'):
            # LẤY TÊN
            Popular['name'] = itemManga.find('a').get('title')

            # LẤY LINK
            Popular['link_chap_update'] = itemMangaLastUpdate.a['href']

            # LẤY POSTER
            Popular['poster_manga'] = itemMangaLastUpdate.img['src']

            Popular['time_update'] = itemMangaLastUpdate.find(
                'span', class_='time hidden-xs').text.strip()

            # LẤY CÁC CHAPTER
            Popular['list_chapter'] = []
        for cha in itemMangaLastUpdate.findAll('dd'):
            chapter = {}
            chapter['link_chapter'] = cha.find('a').get('href')
            chapter['name_chapter'] = cha.a.text.strip()
            Popular['list_chapter'].append(chapter)

        listJsonManga.append(Popular)
    return listJsonManga
# LẤY TRANG SEARCH


@app.route("/search", methods=["GET"])
def get_Search():
    link_full = request.headers.get('Link-Full')
    listGenresManga = []
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')

    for met in soupManga_base.findAll('ul', class_='widget-text-list'):
        for meta in met.findAll('li'):
            itemGenresManga = dict()

            itemGenresManga['link'] = meta.a['href']
            itemGenresManga['genres'] = meta.a['title']

            listGenresManga.append(itemGenresManga)

    return listGenresManga


if __name__ == "__main__":
    app.run(host='0.0.0.0')
