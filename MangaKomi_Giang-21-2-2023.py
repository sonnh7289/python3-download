from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import json
app = Flask(__name__)



@app.route('/ver', methods = ["GET"])
def get_home():
    #session = requests.Session()
    #request = session.get('https://mangakomi.io')
    #soup = BeautifulSoup(request.content, 'html.parser')
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    manga_list = []
    for manga in soup.findAll('div', class_='col-12 col-md-6 badge-pos-1'):
        manga_info = {}
        #Lấy link manga
        manga_info['link_manga'] = manga.find('a').get('href')

        #Lấy tên manga
        manga_info['title_manga'] = manga.find('a').get('title')

        #Lấy ảnh manga
        manga_info['poster_manga'] = manga.find('img').get('src')

        #Lấy lượng rating
        manga_info['rating_manga'] = manga.find('span', class_='score font-meta total_votes').text

        #Lấy chapter mới nhất
        manga_info['lastest_chapter_manga'] = manga.find('span', class_='chapter font-meta').find('a').get('href')

        #Lấy thời gian phát hành
        for time in manga.findAll('span', class_='post-on font-meta')[-1]:
            manga_info['release_date_manga'] = time.text.strip()
            
        manga_list.append(manga_info)
    #with open("data_manga.json", "w") as outfile: json.dump(manga_list, outfile)
    return manga_list

@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    detail = {}
    
    #Lấy anh manga
    detail['poster_manga'] = soup.find('div', class_='summary_image').find('img').get('src')

    #Lay ten manga
    detail['title_manga'] = soup.find('span', property='name').get('title')

    #Lay rating
    list = []
    for rate in soup.find('div', class_='summary-content vote-details'):
        list.append(rate.text.split('\n'))
    detail['rating_manga'] = ''.join(list[2]+list[3]+list[4]).strip()

    #Lay rank
    for item in soup.findAll('div', class_='summary-content')[1]:
        detail['rank_manga'] = item.text.strip()
    
    #Lay ten thay the
    for item in soup.findAll('div', class_='summary-content')[2]:
        detail['alternative_manga'] = item.text.strip()

    #Lay the loai
    detail['genre_manga'] = soup.find('div', class_='genres-content').text.strip()

    #Lay ten tac gia
    for item in soup.findAll('div', class_='summary-content')[4]:
        detail['author_manga'] = item.text.strip()

    #Lay trang thai
    for item in soup.findAll('div', class_='summary-content')[5]:
        detail['status_manga'] = item.text.strip()
    

    return detail

@app.route('/chapter', methods=['GET'])
def get_chapter():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    num_img = []
    for num in soup.findAll('div', class_='page-break no-gaps'):
        num_img.append(num.find('img').get('data-src').strip())
    img = {}
    img['image'] = num_img
    
    return img

@app.route('/searchmanga', methods=['GET'])
def search():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    manga_info = []
    for item in soup.findAll('div', class_='tab-thumb c-image-hover'):
        info = {}
        #Lay link manga
        info['link_manga'] = item.find('a').get('href')
        #Lay ten manga 
        info['title_manga'] = item.find('a').get('title')
        #Lay poster
        info['poster_manga'] = item.find('img').get('src')
        #Lay ten thay the
        for alt in soup.findAll('div', class_='summary-content')[0]:
            info['alternative_manga'] = alt.text.strip()
        
        #Lay the loai 
        genre = []
        for gen in soup.findAll('div', class_='summary-content'):
            genre.append(gen.text.strip())
        info['genre_manga'] = genre[1]

        #Lay trang thai
        for stt in soup.findAll('div', class_='summary-content')[2]:
            info['status_manga'] = stt.text.strip()

        #Lay chapter moi nhat
        info['lastest_chapter_manga'] = soup.find('span', class_='font-meta chapter').find('a').get('href')

        #Lay rating
        info['rating_manga'] = soup.find('div', class_='meta-item rating').text.strip()

        manga_info.append(info)

    return manga_info

@app.route('/category', methods=['GET'])
def category():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    cate_manga = []
    #Lay mo ta the loai
    des = {}
    des['description_manga'] = soup.find('h1', class_='item-title h4').text.strip() + ': ' +soup.find('p', class_='item-description').text.strip()
    cate_manga.append(des)

    for item in soup.findAll('div', class_='col-12 col-md-6 badge-pos-1'):
        info = {}
        #Lay link manga
        info['link_manga'] = item.find('a').get('href')
        #Lay ten manga
        info['title_manga'] = item.find('a').get('title')
        #Lay poster manga
        info['poster_manga'] = item.find('img').get('data-src')
        #Lay rating manga
        info['rating_manga'] = item.find('div', class_='meta-item rating').text.strip()
        #Lat chapter moi nhat
        info['lastest_chapter_manga'] = item.find('span', class_='chapter font-meta').find('a').get('href')
        #Lay ngay phat hanh
        for time in item.findAll('span', class_='post-on font-meta')[-1]:
            info['release_manga'] = time.text.strip()

        cate_manga.append(info)

    return cate_manga


if __name__ == "__main__":
   app.run()




