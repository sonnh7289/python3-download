from flask import Flask, request
from flask_restful import Api, Resource
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/home', methods = ["Get"])
def get_Home():
    listJsonManga = []
    session = requests.Session()
    rManga_base = session.get('https://mangajar.com/')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')    
        
    for latest_item in soupManga_base.findAll('article', class_='flex-item-mini mx-1 splide__slide'):
        ItemJsonManga = dict()
        div_ItemJsonManga = latest_item.find('div', class_= 'poster-container')
        ItemJsonManga['manga_title'] = div_ItemJsonManga.a['title']
        ItemJsonManga['manga_link'] = div_ItemJsonManga.a['href']
        
        ItemJsonManga['manga_poster'] = div_ItemJsonManga.find('img').get('data-splide-lazy')
        
        div1_ItemJsonManga = latest_item.find('div', class_= 'manga-mini-last-chapter list-group-item position-absolute p-0 border-0')
        ItemJsonManga['link_chapter'] = div1_ItemJsonManga.find('a').get('href') 
        ItemJsonManga['chapter_name'] = div1_ItemJsonManga.a.text
        
        listJsonManga.append(ItemJsonManga)
        
        # ItemJsonManga['time_update'] = latest_item.span.text
    
        
    return listJsonManga

@app.route('/home/daymanga', methods = ["Get"])
def get_Home_day():
    day_item_manga = []
    session = requests.Session()
    rManga_base = session.get('https://mangajar.com/')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')    
        
    for manga_day in soupManga_base.findAll('div', class_= 'col-md-4'):
        DayItemJsonManga = dict()     
        day_manga =  manga_day.find('article')        
        DayItemJsonManga['link_manga_day'] = day_manga.find('a').get('href')
        DayItemJsonManga['title_manga_day'] = day_manga.find('a').get('title')
        DayItemJsonManga['poster_manga'] = day_manga.find('img').get('data-src')
        
        day_item_manga.append(DayItemJsonManga)
        
    return day_item_manga

@app.route('/home/newchapter', methods = ["Get"])
def get_new_chapter():
    listnewchapter = []
    session = requests.Session()
    rManga_base = session.get('https://mangajar.com/')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')    
     
          
    for new_chapter in soupManga_base.findAll('div', style='max-height: 400px;overflow-x: hidden;'):    
        newChapterJsonManga = dict()
        newChapterJsonManga['link_new'] = new_chapter.a['href']   
        newChapterJsonManga['chapter'] = new_chapter.find('span').text    
        small = new_chapter.findAll('small')
        number=1
        for i in small:            
            if number==1:
                newChapterJsonManga['manga'] = i.text
            if number==2:
                newChapterJsonManga['date'] = i.text
            number+=1
        
        listnewchapter.append(newChapterJsonManga)
    return listnewchapter

@app.route('/home/topmanga', methods = ["Get"])
def get_topmanga():
    listtopgenre = []
    session = requests.Session()
    rManga_base = session.get('https://mangajar.com/manga')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser') 
          
    for article in soupManga_base.findAll('article', class_='flex-item card mx-1 mx-md-2 mb-3 shadow-sm rounded'):
        topmangaJsonManga = dict()  
        print(article)  
        topmangaJsonManga['link_detail'] = article.a['href']   
        topmangaJsonManga['title_manga'] = article.find('a').get('title')    
        topmangaJsonManga['link_poster'] = article.find('img').get('src')
        
        post_description = article.find('div', class_='post-description')
        li = post_description.findAll('li')
        number=1
        for i in li:            
            if number==1:
                topmangaJsonManga['card-genres-item_1'] = i.text
            if number==2:
                topmangaJsonManga['card-genres-item_2'] = i.text
            number+=1
        topmangaJsonManga['chapter'] = post_description.find('span').text
        topmangaJsonManga['card-text'] = post_description.find('p', class_='card-text').text
        
        post_footer = article.find('ul', class_='post-footer list-group list-group-flush')
        topmangaJsonManga['number-chapter'] = post_footer.find('li').text
        topmangaJsonManga['link-chapter'] = post_footer.find('a').get('href')
        listtopgenre.append(topmangaJsonManga)
        
    return listtopgenre

@app.route('/home/genre', methods = ["Get"])
def get_genre():
    listgenre = []
    session = requests.Session()
    rManga_base = session.get('https://mangajar.com/genre')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser') 
          
    for genre in soupManga_base.findAll('div', class_='col-6 col-md-4 py-2'):
        genreJsonManga = dict()  
        print(genre)  
        
        genreJsonManga['link_genre'] = genre.a['href']   
        genreJsonManga['name_genre'] = genre.find('a').text    
        genreJsonManga['number'] = genre.find('span').text 
        listgenre.append(genreJsonManga)
        
    return listgenre



@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    FullDetailManga = dict()
    for chapter in soupManga_base.findAll('div', class_= 'container manga-container'):
        print(chapter)
        
        poster = chapter.find('div', class_='col-md-5 col-lg-4 text-center')        
        FullDetailManga['link_poster']= poster.find('img').get('src')
        FullDetailManga['title_chapter']= poster.find('img').get('title')  
        
        title = chapter.find('div', class_='col-md-7 col-lg-8')    
        FullDetailManga['content_chapter']= title.find('h2').text
        
        post_info = title.find('div', class_='post-info')
        
        div_button = title.find('div', class_='btn-group')
        FullDetailManga['Subscribe'] = div_button.find('button', class_='subscribe btn mt-1 btn-outline-danger').text  
        FullDetailManga['Readlater'] = chapter.find('button', class_='read-later btn mt-1 btn-outline-primary').text
        FullDetailManga['h5']= title.find('h5').text 
        FullDetailManga['description'] = title.find('div', class_='manga-description entry').text       
                
        
    return FullDetailManga

@app.route("/detailmanga/listchapter", methods=["GET"])
def get_listchapter():
    link_full = request.headers.get('Link-Full')
    print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonchapter = []
    for list_chapter in soupManga_base.findAll('li', class_= 'list-group-item chapter-item'):
        print(list_chapter)
        listchapter = dict()
        listchapter['link_poster']= list_chapter.find('a').get('href')
        span = list_chapter.find('span', class_= 'chapter-title')
        listchapter['chapter_title']= span.text
        listchapter['name_chapter']= list_chapter.find('a').text
        span2 = list_chapter.find('span', class_='chapter-date')
        listchapter['chapter_date'] = span2.text
        
        listJsonchapter.append(listchapter)
    return listJsonchapter

@app.route("/detailmanga/pageItem", methods=["GET"])
def get_detail_pageItem():
    link_full = request.headers.get('Link-Full')
    print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    pageItem = dict()
    for page_item in soupManga_base.findAll('ul', class_= 'pagination'):
        print(page_item)
        item = page_item.find('a', class_='page-link')
        pageItem['page_item'] =item.get('href')
        
    return pageItem


if __name__ == '__main__':
    app.run(host='0.0.0.0' port=2002)