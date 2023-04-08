from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
app = Flask(__name__)

#/home : Lấy màn hình home
#/page : Lấy các thể loại trang
#/detail : Lấy thông tin chi tiết một manga
#/chapter: Lấy nội dung từng chapter




#Home
@app.route('/home', methods = ["GET"])
def get_home():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    home_list = []
    for item in soup.findAll('section'):
        list = []
        list.append(item.find('div', class_='s-title').text.strip())
        manga_info = {} 
        if soup.find('section', class_='group-recommended'):
                if item.find('div', class_='col-1'):
                    manga_info['manga_poster'] = item.find('div', class_='col-1').find('div', class_='under').get('style')
                    manga_info['manga_link'] = item.find('div', class_='col-1').find('a').get('href')
                    manga_info['manga_title'] = item.find('div', class_='col-1').find('div', class_='inner').text.strip()
                    manga_info['manga_rating'] = item.find('div', class_='col-1').find('div', class_='r-container').text.strip()
                    manga_info['manga_author'] = item.find('div', class_='col-1').find('div', class_='author').text.split('\n')[-1]
                    manga_info['manga_genre'] = item.find('div', class_='col-1').find('div', class_='genre').text.split('\n')[-1]
                    manga_info['manga_description'] = item.find('div', class_='col-1').find('p', class_='excerpt').text.strip()
                    list.append(manga_info)
                if item.find('div', class_='col-2'):
                    for rcm in item.findAll('a', class_='entry'):
                        manga_info['manga_poster'] = rcm.get('style')
                        manga_info['manga_link'] = rcm.get('href')
                        manga_info['manga_title'] = rcm.get('title')
                        list.append(manga_info)
        
        for manga in item.findAll('div', class_='entry vertical'):                         
            manga_info['manga_link'] = manga.find('a').get('href')
            manga_info['manga_title'] = manga.find('a').get('title')
            manga_info['manga_poster'] = manga.find('img').get('src')
            manga_info['last_chapter_link'] = manga.find('a', class_='chap').get('href')
            manga_info['last_chapter_name'] = manga.find('a', class_='chap').text.strip()
            list.append(manga_info)
        home_list.append(list)
    return home_list

#Category pages
@app.route('/page', methods=['GET'])
def get_page():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    manga_list = []
    manga_list.append(soup.find('div', class_='s-title').text.strip())
    for manga in soup.findAll('div', class_='entry'):
        manga_info = {}
        manga_info['manga_link'] = manga.find('a').get('href')
        if manga.find('a').get('title') is not None:
            manga_info['manga_title'] = manga.find('a').get('title')
        elif manga.find('div', class_='content').find('span', class_='name') is not None:
             manga_info['manga_title'] = manga.find('div', class_='content').find('span', class_='name').text.strip()
        manga_info['manga_poster'] = manga.find('img').get('src')
        manga_info['manga_rating'] = manga.find('div', class_='rateYo').get('data-rateyo-rating')
        st = manga.find('div', class_='status')
        if st is not None:
            for i in st.findAll('span'):
                manga_info['manga_status'] = i.text 
        view = manga.find('div', class_='view')
        if view is not None:
            for i in view.findAll('span'):
                manga_info['manga_view'] = i.text 
        if manga.find('a', class_='chap') is not None:
            manga_info['manga_last_chapter'] = manga.find('a', class_='chap').get('href')
        manga_list.append(manga_info)
    return manga_list

#Detail manga
@app.route('/detail', methods=['GET'])
def get_detail():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    detail_manga = {} 
    if soup.find('h1', class_='name bigger') is not None:
        detail_manga['manga_title'] = soup.find('h1', class_='name bigger').text.strip()
    elif soup.find('h3', class_='name') is not None:
        detail_manga['manga_title'] = soup.find('h3', class_='name').text.strip()
    list = []
    with open('/Users/macbook/Documents/List_Manga_Blocked.txt', mode='r',  encoding='UTF-8') as file:
        list.append(file.read().split('\n'))
    for i in list:
        for j in i:
            if detail_manga['manga_title'].lower().strip() == j.lower().strip():
                return 'Truyen co noi dung khong hop le'
    detail_manga['manga_link'] = link_full
    if soup.find('div', class_='thumb text-center') is not None:
        detail_manga['manga_poster'] = soup.find('div', class_='thumb text-center').find('img').get('src')  
    if  soup.find('div', class_='rating-container') is not None:
        detail_manga['manga_rate'] =  soup.find('div', class_='rating-container').text.strip()
    if soup.find('div', class_='rating-result') is not None:
        detail_manga['manga_rating'] = soup.find('div', class_='rating-result').text.split(': ')[-1]
    if soup.find('div', class_='alternative') is not None:
        detail_manga['manga_alternative'] = soup.find('div', class_='alternative').text.split('\n')[-1]
    if soup.find('div', class_='author') is not None:
        detail_manga['manga_author'] = soup.find('div', class_='author').text.split('\n')[-1]
    if soup.find('div', class_='genre') is not None:
        detail_manga['manga_genre'] = soup.find('div', class_='genre').text.split('\n')[-1]
    if soup.find('div', class_='new-chap') is not None:
        detail_manga['manga_total_chapter'] = soup.find('div', class_='new-chap').text.split(': ')[-1]
    if soup.find('div', class_='view-times') is not None:
        detail_manga['manga_view'] = soup.find('div', class_='view-times').text.split('\n')[2]
    if soup.find('div', class_='update') is not None:
        detail_manga['manga_status'] = soup.find('div', class_='update').text.split('\n')[2]
    detail_manga['manga_description'] = soup.find('div', class_='comic-description').text.split('\n')[4:-5]
    return detail_manga
    
#Content chapter
@app.route('/chapter', methods=['GET'])
def get_chapter():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    list_manga = []
    for num in soup.find('div', class_='chapter-content').findAll('img'):
        list_manga.append(num.get('src'))
    return list_manga



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5008)
