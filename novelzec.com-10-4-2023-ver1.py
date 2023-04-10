from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from urllib.parse import urlparse
from urllib.parse import parse_qs
#from utils.utils import beetoon_api
import requests
import json
from bs4 import BeautifulSoup
import jsonpickle
_BASE_URL = 'https://novelzec.com'
_DEFAULT_LINK = 'novel-seri-88888736'
_DEFAULT_MORE_PAGE_LINK = 'novel_list?type=latest&category=all&state=all&page=1'
app = Flask(__name__)

# Danh sach tat ca category
@app.route("/home", methods=["GET"])
def get_Home():
    JsonHomePage = dict()
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get(_BASE_URL)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    for itemMangaLastUpdate in soupManga_base.findAll('div', class_='itemupdate first'):
        ItemJsonManga = dict()
        ItemJsonManga['name manga'] = itemMangaLastUpdate.find('a').find('img').get('alt')
        ItemJsonManga['full manga'] = itemMangaLastUpdate.a['href']
        ItemJsonManga['time update'] = itemMangaLastUpdate.find('ul').find('li').find('i').text   
        ItemJsonManga['poster manga'] = itemMangaLastUpdate.img['src']
        listJsonManga.append(ItemJsonManga)
    listType = []
    listCategory = []
    ListDiv = soupManga_base.find('div', {"class": "side-bar"}).find('div').find_all('div', {"class" : "box category-list"})
    ListLiType = ListDiv[0].find('ul').select('li')
    ListLiCategory = ListDiv[1].find('ul').select('li')
    for index in ListLiType:
        ItemJsonType = dict()
        ItemJsonType['title'] = index.find('a').text
        ItemJsonType['link search by title'] = index.find('a').get('href')
        listType.append(ItemJsonType)
    for index in ListLiCategory:
        ItemJsonType = dict()
        ItemJsonType['title'] = index.find('a').text
        ItemJsonType['link search by title'] = index.find('a').get('href')
        listCategory.append(ItemJsonType)

    JsonHomePage['list manga'] = listJsonManga
    JsonHomePage['list type'] = listType
    JsonHomePage['list category'] = listCategory

    return jsonpickle.encode(JsonHomePage)

@app.route("/morepage/<link>")
def MorePage(link):
    type = request.args.get('type')
    category = request.args.get('category')
    state = request.args.get('state')
    page = request.args.get('page')
    print('-----------------')
    print(link)
    print(type)
    print(category)
    print(state)
    print(page)
    print('-----------------')
    JsonMorePage = dict()
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get(_BASE_URL + '/' + link + "?type=" + type + "&category=" + category + "&state=" + state + "&page=" + page)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    for add in soupManga_base.findAll('div', class_='box story-list truyen-list'):
        UL = add.find('ul')
        ListLI = UL.select('li')
        for index in ListLI:
            ItemJsonManga = dict()
            ItemJsonManga['name manga'] = index.find('h3').find('a').text
            ItemJsonManga['full manga'] = index.find('a').get('href')
            ListP = index.select('p')
            ItemJsonManga['last update'] = ListP[0].text.split(' ', 2)[2]
            ItemJsonManga['view'] = ListP[1].text.split()[1]
            listJsonManga.append(ItemJsonManga)
        break
    JsonMorePage['list manga'] = listJsonManga
    return jsonpickle.encode(JsonMorePage)


@app.route("/search_novel/<name>")
def SearchNovel(name):
    page = request.args.get('page')
    page = 0 if page == None else page
    print('-------------')
    print(page)
    JsonSearchPage = dict()
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get(_BASE_URL + '/' + 'search_novel' + '/' + name + "?page=" + str(page))
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    for add in soupManga_base.findAll('div', class_='box story-list truyen-list author-list'):
        UL = add.find('ul')
        ListLI = UL.select('li')
        for index in ListLI:
            ItemJsonManga = dict()
            ItemJsonManga['name manga'] = index.find('h3').find('a').text
            ItemJsonManga['full manga'] = index.find('a').get('href')
            ListP = index.select('p')
            ItemJsonManga['last update'] = ListP[0].text.split(' ', 2)[2]
            ItemJsonManga['view'] = ListP[1].text.split()[1]
            listJsonManga.append(ItemJsonManga)
        break
    JsonSearchPage['list manga'] = listJsonManga
    return jsonpickle.encode(JsonSearchPage)

@app.route("/detailmanga/<link>", methods=["GET"])
def get_DetailManga(link):
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(_BASE_URL + '/' + link)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    FullDetailManga = dict()
    for add in soupManga_base.findAll('ul', class_='truyen-info entry-header'):
        ListLI = add.select('li')
        FullDetailManga['name manga'] = ListLI[1].find('h1').text
        FullDetailManga['author'] = ListLI[2].find('a').text
        Genres = ListLI[3]
        ListGenres = []
        for index in Genres.findAll('a'):
            ListGenres.append(index.text)
        FullDetailManga['genres'] = ListGenres
        FullDetailManga['status'] = ListLI[4].find('a').text
        FullDetailManga['view'] = ListLI[5].text.split()[2]
        FullDetailManga['last updated'] = ListLI[6].text.split(': ', 1)[1]
        FullDetailManga['link first chapter'] = ListLI[7].find('a').get('href')
        FullDetailManga['link latest chapter'] = ListLI[8].find('a').get('href')
        FullDetailManga['rating(5star)'] = ListLI[9].find('p').find('em').find('span').find('span', {"rel":"v:rating"}).find('span').find('span').text
        FullDetailManga['vote'] = ListLI[9].find('p').find('em').find('span').find('span', {"property":"v:votes"}).text
        break
    for add in soupManga_base.findAll('div', class_='noi-dung-truyen'):
        FullDetailManga['novel summary'] = add.find('h2').text + add.find('p').text
        break
    listChapter = []
    ListLI = soupManga_base.find('div', {"class" : "box chap-list"}).find('ul').select('li')
    for index in ListLI:
        IteamChapter = dict()
        IteamChapter['name'] = index.find('a').text
        IteamChapter['link chapter'] = index.find('a').get('href')
        IteamChapter['update time'] = index.find('p').text
        listChapter.append(IteamChapter)
    NovelPage = dict()
    NovelPage['detail novel'] = FullDetailManga
    NovelPage['all chapter'] = listChapter
    return jsonpickle.encode(NovelPage)

@app.route("/detailmanga/<link>/<chapter>", methods=["GET"])
def AllContentManga(link, chapter):
    session = requests.Session()
    rManga_base = session.get(_BASE_URL + '/' + link + '/' + chapter)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    FullDetailManga = dict()
    FullDetailManga['name chapter'] = soupManga_base.find('div', {"class" : "content-story-get-size content-story lam-nham-chap"}).find('h3').text
    print(FullDetailManga['name chapter'])

    Content = []
    ListP = soupManga_base.find('div', {"class" : "content-story-get-size content-story lam-nham-chap"}).select('p')
    for index in ListP:
        print("------------------")
        print(index)
        Content.append(index.text)
    FullDetailManga['content'] = Content
    return jsonpickle.encode(FullDetailManga)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3993)