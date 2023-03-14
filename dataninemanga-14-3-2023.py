# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request,json,current_app,make_response
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup 
from json import dumps
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True # bat dinh dang file Json cua flask

def get_home_hot(link,full_hot_home):
    request_home = requests.get(link)
    soup_home = BeautifulSoup(request_home.text, 'html.parser')
    for hot_Updatein in soup_home.find_all('div',class_='rightbox'):
        ul_right = hot_Updatein.find('ul')
        for li_hot in ul_right.find_all('li'):
            homehot=dict()
            dt_hot= li_hot.find('dt')
            dd_hot = li_hot.find('dd')
            homehot['Name_hot'] = li_hot.find('img').get('alt')
            homehot['Image_hot'] = dt_hot.find('img').get('src')
            homehot['Chapter_hot'] = dd_hot.find('span').text
            full_hot_home.append(homehot)
    return full_hot_home
def get_home_hotUpdate(link, full_hot_update):
    request_home = requests.get(link)
    soup_home = BeautifulSoup(request_home.text, 'html.parser')
    for hot_Updatein in soup_home.find_all('div',class_='pop_update'):
        for li_hot in hot_Updatein.find_all('li'):
            homehot=dict()
            linkMangaHot = li_hot.find('a',class_='bookface')
            nameMangaHot = li_hot.find('a',class_='bookname')
            homehot['Name'] = li_hot.find('a',class_='bookname').get('title')
            homehot['Link_Manga'] = linkMangaHot.get('href')
            homehot['Image'] = linkMangaHot.find('img').get('src')
            homehot['Month_Update'] = nameMangaHot.find('font').text
            full_hot_update.append(homehot)
    return full_hot_update
def get_home_new_Manga(link,full_new_Manga):
    request_home = requests.get(link)
    soup_home = BeautifulSoup(request_home.text, 'html.parser') 
    for home in soup_home.find_all('div', class_='rightbox'):
        div_ = home.find_all('ul')
        for  div in div_[1].find_all('li'):
            new_manga = dict()
            new_manga['Name_Manga_New']= div.find('a',class_='show_book_desc').text.strip()
            new_manga['Chapter_New'] = div.find('span').text.strip()
            new_manga['Thumb'] = div.find('img').get('src')
            full_new_Manga.append(new_manga)
    return full_new_Manga
def get_home_lastMangaUpdate(link,full_latest_update):
    request_home = requests.get(link)
    soup_home = BeautifulSoup(request_home.text, 'html.parser')
    for latest_Update in soup_home.find_all('ul',class_='homeupdate'):
        for li_latest in latest_Update.find_all('li'):
            mangaDetai=dict()
            dtlast = li_latest.find('dl')
            mangaDetai['Name'] = li_latest.find('a',class_='show_book_desc').text
            mangaDetai['Chapter_Update'] = dtlast.find('a').text
            mangaDetai['Time_Update'] = dtlast.find('dd').text
            full_latest_update.append(mangaDetai)
    return full_latest_update
def get_link_anh_trong_page_chapter(link_dau_vao, page_chapter_list):#lay anh
    request_mangachapterlink_next = requests.get(link_dau_vao)
    soupchapter_next = BeautifulSoup(request_mangachapterlink_next.text,'html.parser')
    for emIndex in  soupchapter_next.findAll('a', class_='pic_download'):
        mageSrc = emIndex.get('href')
        page_chapter_list.append(mageSrc)
    return page_chapter_list
def get_All_anh_cua_tung_trang(linkpage, full_detail): #lay link
    requestPage = requests.get(linkpage)
    soupchapter = BeautifulSoup(requestPage.text, 'html.parser')
    selectchapter = soupchapter.find('div', class_='changepage')
    indexchapterstr = selectchapter.find('option')
    if indexchapterstr is not None:
        indexchapterstrs = indexchapterstr.text
        indexchapters = indexchapterstrs[2:]  #lay tong so chapter dang chuoi
        totalAllchapters = int(indexchapters) #chuyen chuoi sang ints
    for indexchapter in range(totalAllchapters): # doan nay la lay du lieu tung trang 
        link_chapter_10 = linkpage[:-6] + str(indexchapter+1) + '.html' # Day la link su dung kieu doc image 10 (-10-)
        request_All_link_chapter10 = requests.get(link_chapter_10)
        soup_All_linkchapter_10 = BeautifulSoup(request_All_link_chapter10.text,'html.parser')
        for image_All in soup_All_linkchapter_10.find_all('div', class_='pic_box'):
            mangaImg=dict()
            for image in image_All.findAll('img'): 
                full_detail.append(image.get('src'))
                print(image.get('src'))
                mangaImg['Image'] = full_detail
    return mangaImg
@app.route("/index/<indexpage>", methods=["GET"]) #indexpage la thu tu cua trang. VD: http://192.168.1.11:5000/home/1 
def get_index(indexpage):
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://www.ninemanga.com/category/index_' + str(indexpage)+ '.html',verify=False)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    for homeninemanga in soupManga_base.find_all('dl',class_='bookinfo'):   
        ItemJsonManga=dict()  
        ItemJsonManga['Manga_Name'] = homeninemanga.find('a',class_='bookname').text
        ItemJsonManga['Manga_Thumb'] = homeninemanga.find('img').get('src')
        for dd in homeninemanga.find_all('dd'):
            ItemJsonManga['View'] = dd.find('span').text
            ItemJsonManga['ChapterNew'] = dd.find('a',class_='chaptername').text
        listJsonManga.append(ItemJsonManga)
    return jsonify(listJsonManga)
@app.route("/detail_Manga/<fullname>", methods=["GET"]) #fullname phần tên trong link của truyện muốn scraping data, VD: http://192.168.1.11:5000/detail_Manga/Hard%20na%20Choukyoushi
def detailManga(fullname):
    session = requests.Session()
    linkDetail = 'https://www.ninemanga.com/manga/' + str(fullname) + '.html'
    rManga_base =  session.get(linkDetail)
    soup_DetailManga = BeautifulSoup(rManga_base.content,'html.parser')
    full_author_detail = [] #list cua author
    full_genre_detail = [] #list cua genre
    full_chapter_detail=[]#list all chapter
    full_detail=[]
    manga_detail = {} #dict    
    manga_detail['Detail_Name'] = soup_DetailManga.find('h1', itemprop='name').text
    for message in soup_DetailManga.find_all('div', class_='bookintro'):
        for ul in message.find_all('ul', class_='message'):
            div_ = ul.find_all('li')
            for  div in div_[1]:
                manga_detail['Alternative'] = div.text.strip()
    manga_detail['Author'] = soup_DetailManga.find('a', itemprop='author').text
    for genre in soup_DetailManga.find_all('li', itemprop='genre'):
            manga_categories = genre.text
            full_genre_detail.append(manga_categories)
            manga_detail['Gener'] = full_genre_detail
    # manga_detail['Year'] = soup_DetailManga.find('a', itemprop='year').text
    chapterlink = soup_DetailManga.find('a', class_='chapter_list_a')
    manga_detail['Year'] = soup_DetailManga.find('a', itemprop='year').text
    
    for chaptersoup in soup_DetailManga.find_all('ul', class_='sub_vol_ul'):
        for lichapter in chaptersoup.find_all('li'):
            listchapter = lichapter.find('a', class_='chapter_list_a').text
            full_chapter_detail.append(listchapter)
        manga_detail['chapter'] = full_chapter_detail
    
    return jsonify(manga_detail)
@app.route('/home')
def get_home():
    linkhome = 'https://www.ninemanga.com/'
    home_Manga_dict = dict()
    full_hot_update=[]
    full_latest_update=[]
    full_hot_home = []
    full_new_Manga=[]
    full_hot_home = get_home_hot(linkhome,full_hot_home)
    full_hot_update =  get_home_hotUpdate(linkhome,full_hot_update)
    full_latest_update = get_home_lastMangaUpdate(linkhome,full_latest_update)
    full_new_Manga = get_home_new_Manga(linkhome,full_new_Manga)
    home_Manga_dict['Hot_Update'] = full_hot_update
    home_Manga_dict['Latest_Update'] = full_latest_update
    home_Manga_dict['Hot_Manga']= full_hot_home
    home_Manga_dict['New_Manga'] = full_new_Manga
    return jsonify(home_Manga_dict)
@app.route('/search/<nameSearch>')
def get_search(nameSearch):
    link = 'https://www.ninemanga.com/search/?wd=' + str(nameSearch)
    request = requests.get(link)
    soup= BeautifulSoup(request.text,'html.parser')
    for ul in soup.find_all('ul', class_='direlist'):
        manga_error = dict()
        li = ul.find('li')
        list_search = []
        if li is not None:
            for li2 in ul. find_all('li'):
                for dd in li2.find_all('dl', class_='bookinfo'):
                    # for dd in dl.find_all('dd'):
                    manga_search = dict()
                    manga_search['Name_Search'] = dd.find('a', class_='bookname').text
                    manga_search['Description'] = dd.find('p').text
                    manga_search['Views'] = dd.find('span').text
                    manga_search['Chapter'] = dd.find('a', class_='chaptername').text
                    manga_search['Thumb'] = dd.find('img').get('src')
                    print(dd.find('a', class_='bookname').text)
                    list_search.append(manga_search)
        else:
            manga_error['error'] = 'Khong tim thay truyen  ' + str(nameSearch)
            list_search.append(manga_error)
    return jsonify(list_search)

@app.route("/chapter/<Manga>/<linkchapter>", methods=["GET"]) #fullname phần tên trong link của truyện muốn scraping data, VD: http://192.168.1.11:5000/detail_Manga/Hard%20na%20Choukyoushi
def detailChapter(linkchapter,Manga):
    session = requests.Session()
    linkDetail = 'https://www.ninemanga.com/chapter/'+ str(Manga) + '/' + str(linkchapter) + '-1.html'
    rManga_base =  session.get(linkDetail)
    soup_chapter = BeautifulSoup(rManga_base.content,'html.parser')
    chapter_detail = dict()
    full_image_chapter = []
    full_image_chapter = get_All_anh_cua_tung_trang(linkDetail,full_image_chapter)
    for mainbox in soup_chapter.find_all('div', class_='mainbox'):
        chapter_detail['Name_chap'] = mainbox.find('a').text
    chapter_detail['ThumB'] = full_image_chapter
    return jsonify(chapter_detail)
if __name__ == "__main__":
   app.run(host='0.0.0.0',port=190003)
