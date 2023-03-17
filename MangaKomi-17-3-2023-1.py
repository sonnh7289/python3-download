from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import json
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
app = Flask(__name__)

# /ver : Lấy loại trang manga
# /detailmanga : Thông tin chi tiết một manga
# /chapter : Ảnh chapter manga
# /searchmanga : Thông tin tìm kiếm manga
# /category : Thể loại manga 

file = Document('/var/www/truyen-sex-remove.docx')
rels = file.part.rels
urls = []
for rel in rels:
    if rels[rel].reltype == RT.HYPERLINK:
        urls.append(rels[rel]._target)

#LẤY PHÂN LOẠI TRANG MANGA
@app.route('/ver', methods = ["GET"])
def get_home():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    
    manga_list = []
    for manga in soup.findAll('div', class_='col-12 col-md-6 badge-pos-1'):
        manga_info = {}

        link_check = manga.find('a').get('href')
        if link_check not in urls: 
            #Lấy link manga           
            manga_info['link_manga'] = manga.find('a').get('href')

            #Lấy tên manga
            manga_info['title_manga'] = manga.find('a').get('title')

            #Lấy ảnh manga
            manga_info['poster_manga'] = manga.find('img').get('data-src')

            #Lấy lượng rating
            manga_info['rating_manga'] = manga.find('span', class_='score font-meta total_votes').text

            #Lấy chapter mới nhất
            manga_info['lastest_chapter_manga'] = manga.find('span', class_='chapter font-meta').find('a').get('href')

            #Lấy thời gian phát hành
            for time in manga.findAll('span', class_='post-on font-meta')[-1]:
                if time.text.strip() != '':
                    manga_info['release_date_manga'] = time.text.strip()
                    
            manga_list.append(manga_info)
                
    #with open("data_manga.json", "w") as outfile: json.dump(manga_list, outfile)
    return manga_list

#LẤY CHI TIẾT THÔNG TIN MANGA
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
   
    if link_full in urls:
            return 'Truyen co noi dung khong phu hop'
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')

    detail = {}
    
    #Lấy anh manga
    detail['poster_manga'] = soup.find('div', class_='summary_image').find('img').get('data-src')

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

#LẤY ẢNH CHAPTER
@app.route('/chapter', methods=['GET'])
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
        num_img.append(num.find('img').get('data-src').strip())    
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
        link_check = item.find('a').get('href')
        if link_check not in urls:
            info['link_manga'] = item.find('a').get('href')
            #Lay ten manga 
            info['title_manga'] = item.find('a').get('title')
            #Lay poster
            info['poster_manga'] = item.find('img').get('data-src')
            
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
            info['lastest_chapter_manga'] = item.find('span', class_='font-meta chapter').find('a').get('href')

            #Lay rating
            info['rating_manga'] = item.find('div', class_='meta-item rating').text.strip()

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
    cate_manga = []
    #Lay mo ta the loai
    des = {}
    if soup.find('h1', class_='item-title h4').text.strip() is not None:
        des['description_manga'] = soup.find('h1', class_='item-title h4').text.strip()
        if des['description_manga'] == 'Adult' or des['description_manga'] == 'Ecchi' or des['description_manga'] == 'Seisen' or des['description_manga'] == 'Smut':
            return 'Loai truyen khong phu hop'
    if soup.find('p', class_='item-description') is not None:
        des['description_manga'] = soup.find('h1', class_='item-title h4').text.strip() + ': ' + soup.find('p', class_='item-description').text.strip()
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
            if time.text.strip() != '':
                info['release_manga'] = time.text.strip()

        cate_manga.append(info)

    return cate_manga


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5008)




