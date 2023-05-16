from flask import Flask, jsonify, request
from flask_restful import Api, Resource
#from utils.utils import beetoon_api
import base64
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
app = Flask(__name__)

# Trang home
@app.route("/home", methods=["GET"])
def get_Home():
    link_full = request.headers.get('Link-Full')
    
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    ListMangaNew = []
    
    for itemMangaNew in soupManga_base.findAll('div', class_= 'col-6 col-md-3 badge-pos-2'):
        ItemJsonMangaNew = dict()
        ItemJsonMangaNew['name_manga'] = itemMangaNew.a['title']
        ItemJsonMangaNew['link_detail'] = itemMangaNew.a['href']
        for itemSpan in itemMangaNew.findAll('span', class_='post-on font-meta'):
            if len(itemSpan.text) > 2:
                ItemJsonMangaNew['time_update'] = itemSpan.text.replace('\n','')
        ItemJsonMangaNew['img_manga'] = itemMangaNew.img['src']
        ListMangaNew.append(ItemJsonMangaNew)
    return ListMangaNew   

#Trang detai managa
@app.route("/detailmanga", methods = ["GET"])
def get_detail():
    link_full = request.headers.get('Link-Full')
    
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')

    detail = {}
    
    #Lấy anh manga
    detail['poster_manga'] = soup.find('div', class_='summary_image').img['src']

    #Lay ten manga
    detail['title_manga'] = soup.find('div', class_='post-title').text.strip()

    index = 0
    #Lay rating
    list = []
    if soup.find('div', class_='summary-content vote-details') is not None:
        for rate in soup.find('div', class_='summary-content vote-details'):
            list.append(rate.text.split('\n'))
        detail['rating_manga'] = ''.join(list[2]+list[3]+list[4]).strip()
        index+=1

    #Lay rank
    for item in soup.findAll('div', class_='summary-heading'):
        if item.text.strip() == 'Rank':
            for rank in soup.findAll('div', class_='summary-content')[index]:
                detail['rank_manga'] = rank.text.strip()
    index+=1
    
    #Lay ten thay the
    for head in soup.findAll('div', class_='summary-heading'):      
        if head.text.strip() == 'Alternative':
            for alt in soup.findAll('div', class_='summary-content')[index]:
                detail['alternative_manga'] = alt.text.strip()
            index+=1

    #Lay ten tac gia
    if soup.find('div', class_='author-content') is not None:
        detail['author_manga'] = soup.find('div', class_='author-content').text.strip()
        index+=1
                
    #Lay nghe si
    if soup.find('div', class_='artist-content') is not None:
        detail['artist_manga'] = soup.find('div', class_='artist-content').text.strip()
        index+=1

    #Lay the loai
    genre = ''
    if soup.find('div', class_='genres-content') is not None:
        genre = soup.find('div', class_='genres-content').text.strip()
        if 'Adult' in genre:
            return 'Truyen co noi dung khong phu hop'
        elif 'Ecchi' in genre:
            return 'Truyen co noi dung khong phu hop'
        elif 'Seinen' in genre:
            return 'Truyen co noi dung khong phu hop'
        elif 'Smut' in genre:
            return 'Truyen co noi dung khong phu hop'
        detail['genre_manga'] = soup.find('div', class_='genres-content').text.strip()
        index+=1

    #Lay loai
    for head in soup.findAll('div', class_='summary-heading'):
        if (head.text.strip() == 'Type'):
            for alt in soup.findAll('div', class_='summary-content')[index]:
                detail['type_manga'] = alt.text.strip()
            index+=1
    
    #Lay trang thai
    for item in soup.findAll('div', class_='summary-content')[-1]:
        detail['status_manga'] = item.text.strip()

    #Lay tom tat truyen
    detail['summary_manga'] = soup.find('div', class_='summary__content show-more').find('p').text.strip()

    #Lay list chapter
    detail['list_chapter'] = []    
    for chap in soup.findAll('li', class_='wp-manga-chapter'):
        chapter = {}
        chapter['link_chapter'] = chap.find('a').get('href')
        chapter['name_chapter'] = chap.find('a').text.strip()
        if chap.find('span', class_='chapter-release-date') is not None:
            chapter['release_date'] = chap.find('span', class_='chapter-release-date').text.strip()
        detail['list_chapter'].append(chapter)
    return detail

#Lay anh chapter
@app.route("/chapter", methods = ['GET'])
def get_chapter():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    img = {}
    num_img = []
    if soup.find('div', class_='nav-previous') is not None:
        img['prev'] = soup.find('div', class_='nav-previous').find('a').get('href')
    for num in soup.findAll('div', class_='page-break no-gaps'):
        num_img.append( num.find('img').get('src').strip())
    img['image'] = num_img
    img['next'] = soup.find('div', class_='nav-next').find('a').get('href')
    
    return img

#LẤY THÔNG TIN TÌM KIẾM MANGA
@app.route('/searchmanga', methods=['GET'])
def search():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    manga_info = []
    for item in soup.findAll('div', class_='row c-tabs-item__content'):
        info = {}
        #Lay link manga
        info['link_manga'] = item.find('a').get('href')
        #Lay ten manga 
        info['title_manga'] = item.find('a').get('title')
        #Lay poster
        info['poster_manga'] = item.find('img').get('src')
        
        index = 0
        list = []
        for all in item.findAll('div', class_='summary-content'):
            list.append(all.text.strip())
        #info['manga'] = list
        #Lay ten thay the
        for head in item.findAll('div', class_='summary-heading'):      
            if head.text.strip() == 'Alternative':
                info['alternative_manga'] = list[index]
                index+=1
        
        #Lay ten tac gia
        for head in item.findAll('div', class_='summary-heading'):      
            if head.text.strip() == 'Authors':
                info['author_manga'] = list[index]
                index+=1

        #Lay nghe si
        for head in item.findAll('div', class_='summary-heading'):      
            if head.text.strip() == 'Artists':
                info['artist_manga'] = list[index]
                index+=1

        #Lay the loai 
        for head in item.findAll('div', class_='summary-heading'):      
            if head.text.strip() == 'Genres':
                info['genre_manga'] = list[index]
                index+=1
     
        #Lay trang thai
        info['status_manga'] = list[-1]

        #Lay chapter moi nhat
        sonpro = item.find('span', class_='font-meta chapter')
        if sonpro != None:
            find1 = sonpro.find('a')
            if find1 != None:
                info['lastest_chapter_manga'] = find1.get('href') 

        #Lay rating
        rating = item.find('div', class_='meta-item rating')
        if rating != None:
            info['rating_manga'] = rating.text.strip()

        #Lay thoi gian phat hanh
        if item.find('div', class_='meta-item post-on') is not None:
            if item.find('div', class_='meta-item post-on').find('span', class_='font-meta').text.strip() != '':
                info['release_manga'] = item.find('div', class_='meta-item post-on').find('span', class_='font-meta').text.strip()
        

        manga_info.append(info)

    return manga_info

#LẤY LOẠI MANGA 
@app.route('/category', methods=['GET'])
def category():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    category_full = dict()
    cate_manga = []
    #Lay mo ta the loai
    des = {}
    des['description_manga'] = soup.find('h1', class_='item-title h4').text.strip()
    if soup.find('p', class_='item-description') is not None:
        des['description_manga'] = soup.find('h1', class_='item-title h4').text.strip() + ': ' + soup.find('p', class_='item-description').text.strip()
    cate_manga.append(des)

    for item in soup.findAll('div', class_='col-6 col-md-2 badge-pos-2'):
        info = {}
        #Lay link manga
        info['link_manga'] = item.find('a').get('href')
        #Lay ten manga
        info['title_manga'] = item.find('a').get('title')
        #Lay poster manga
        info['poster_manga'] = item.find('img').get('src')
        #Lay rating manga
        info['rating_manga'] = item.find('div', class_='meta-item rating').text.strip()
        #Lat chapter moi nhat
        info['lastest_chapter_manga'] = item.find('span', class_='chapter font-meta').find('a').get('href')
        #Lay ngay phat hanh
        for time in item.findAll('span', class_='post-on font-meta')[-1]:
            if time.text.strip() != '':
                info['release_manga'] = time.text.strip()

        cate_manga.append(info)
    category_full['cate_manga']= cate_manga
    
    
    page = dict()
    
    if soup.find('nav', class_= 'navigation paging-navigation') is not None:        
        older_post = soup.find('div', class_='nav-previous float-left').a['href']
        page['link_older_post'] = older_post
        newer_post = soup.find('div', class_='nav-next float-right').a['href']
        page['link_newer_post'] = newer_post
        category_full['page'] = page
    return category_full


if __name__ == "__main__" :
    app.run(host='0.0.0.0')
    #get_detail()