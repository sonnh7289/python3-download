from flask import Flask, jsonify, request
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route("/Mangaclash_home", methods=["GET"])

def get_home():
    Mangaclash =[]
    session = requests.Session()
    manga = session.get('https://mangaclash.com/')
    soup = BeautifulSoup(manga.content,'html.parser')
    for item in soup.findAll('div', class_="page-content-listing item-default"):
        Manga_Clash = dict()
        item11 = item.find_all('div', class_="page-item-detail manga")
        for item2 in item11:
            Manga_Clash['MangaClash_link']= item2.find('div').find('a').get('href')
            Manga_Clash['MangaClash_title']= item2.find('div').find('a').get('title')
            Manga_Clash['MangaClash_img']= item2.find('div').find('a').find('img').get('data-src')
            Manga_Clash['MangaClash_img1']= item2.find('div').find('a').find('img').get('data-srcset')
            Manga_Clash['MangaClash_img2']= item2.find('div').find('a').find('img').get('src')
            item12 = item2.find_all('div', class_='chapter-item')
            for item3 in item12:
                Manga_Clash['MangaClash_chapter_link']= item3.find('a').get('href')
                Manga_Clash['MangaClash_chapter']= item3.find('a').text
                Manga_Clash['MangaClash_time_day']= item3.find('span', class_="post-on font-meta").text
                Mangaclash.append(Manga_Clash.copy())
        return Mangaclash
@app.route("/Home/Manga", methods=["GET"])

def get_manga():
    link_full = request.headers.get('link_full')
    Manga =[]
    session = requests.Session()
    manga = session.get(link_full)
    soup = BeautifulSoup(manga.content,'html.parser')
    for item in soup.findAll('div', class_="post-content"):
        Manganame = dict()
        item11 = item.find_all('div', class_='post-content_item')
        for item1 in item11:
            Manganame['summary-heading'] = item1.find('div', class_='summary-heading').find('h5').text
            Manganame['summary_content']= item1.find('div', class_='summary-content').text
            Manga.append(Manganame.copy())
    for item2 in soup.findAll('div', class_='c-page__content'):
        Manga_summary= dict()
        Manga_summary['header'] = item2.find('h2', class_='h4').text
        Manga.append(Manga_summary.copy())
    for item3 in soup.findAll('ul', class_='main version-chap no-volumn'):
        Manga_RELEASES= dict()
        item33 = item3.find_all('li', class_='wp-manga-chapter')
        for item4 in item33:
            Manga_RELEASES['chapter_link'] = item4.find('a').get('href')
            Manga_RELEASES['chapter_name'] = item4.find('a').text
            Manga_RELEASES['chapter_time'] = item4.find('span').find('i').text
            Manga.append(Manga_RELEASES.copy())             
    return Manga

@app.route("/Home/Manga/detailManga", methods=["GET"])

def detailManga():
    link_full = request.headers.get('link_full')
    detailManga =[]
    session = requests.Session()
    manga = session.get(link_full)
    soup = BeautifulSoup(manga.content,'html.parser')
    for item1 in soup.findAll('ol', class_="breadcrumb"):
        detail_Manga = dict()
        item11 = item1.find_all('li')[2]
        for item12 in item11:
            detail_Manga['name'] = item12.text
            detailManga.append(detail_Manga.copy())
    for item2 in soup.findAll('select', class_='selectpicker single-chapter-select'):
        detail_Manga_link=dict()
        item22 = item2.find_all('option')
        for item3 in item22:
            detail_Manga_link['link']= item3.get('data-redirect')
            detail_Manga_link['chapter']= item3.text
            detailManga.append(detail_Manga_link.copy())
    for item4 in soup.findAll('div', class_='reading-content'):
        detail_Manga_content = dict()
        item44 = item4.find_all('div',class_="page-break no-gaps")
        for item5 in item44:
            detail_Manga_content['img'] = item5.find('img').get('data-src')
            detailManga.append(detail_Manga_content.copy())
    return detailManga

@app.route("/Search/<int:index>", methods=["GET"])   
# index: 1->224
def get_search(index):
    session = requests.Session()
    manga = session.get('https://mangaclash.com/page/'+str(index)+'/?s&post_type=wp-manga&op&author&artist&release&adult')
    soup = BeautifulSoup(manga.content,'html.parser')
    Mangasearch = []
    
    for item in soup.findAll('div', class_="c-tabs-item"):
        id=0
        item11 = item.find_all('div', class_='tab-thumb c-image-hover')
        for item1_1 in item11:
            Manga_search1= dict()
            id=id+1
            Manga_search1['link:'+str(id)] = item1_1.find('a').get('href')
            Manga_search1['name:'+str(id)] = item1_1.find('a').get('title')
            Manga_search1['img:'+str(id)] = item1_1.find('a').find('img').get('data-src')
            Manga_search1['img1:'+str(id)] = item1_1.find('a').find('img').get('src')
            Mangasearch.append(Manga_search1.copy())
        item12 = item.find_all('div', class_='post-content_item mg_alternative nofloat')
        id=0
        for item1_2 in item12:
            Manga_search2= dict()
            id=id+1
            Manga_search2['Alternative:'+str(id)] = item1_2.find('div', class_="summary-content").text
            Mangasearch.append(Manga_search2.copy())
        item13 = item.find_all('div', class_='post-content_item mg_genres nofloat')
        id=0
        for item1_3 in item13:
            Manga_search3= dict()
            id=id+1
            item131 = item1_3.find_all('div',class_='summary-content')
            for item1_3_1 in item131:
                Manga_search3['Genres_title:'+str(id)] = item1_3_1.text
               # Manga_search3['Genres_link'] = item1_3_1.find('a').get('href')
                Mangasearch.append(Manga_search3.copy())
        item14 = item.find_all('div', class_='post-content_item mg_status nofloat')
        id=0
        for item1_4 in item14:
            Manga_search4= dict()
            id=id+1
            Manga_search4['Status:'+str(id)] = item1_4.find('div', class_="summary-content").text
            Mangasearch.append(Manga_search4.copy())
        item15 = item.find_all('div', class_="tab-meta")
        id=0
        for item1_5 in item15:
            Manga_search5= dict()
            id=id+1
            Manga_search5['chapter_link:'+str(id)] = item1_5.find('div',class_='meta-item latest-chap').find('span',class_="font-meta chapter").find('a').get('href')
            Manga_search5['Latest_chapter:'+str(id)] = item1_5.find('div',class_='meta-item latest-chap').find('span',class_="font-meta chapter").find('a').text
            Manga_search5['time:'+str(id)] = item1_5.find('div',class_='meta-item post-on').find('span',class_="font-meta").text
            Manga_search5['rating:'+str(id)] = item1_5.find('div',class_='meta-item rating').find('span',class_="score font-meta total_votes").text

            Mangasearch.append(Manga_search5.copy())
        return Mangasearch
if __name__ == "__main__":
   app.run(host='0.0.0.0')