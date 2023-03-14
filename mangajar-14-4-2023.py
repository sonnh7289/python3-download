from flask import Flask, request
from flask_restful import Api, Resource
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/home', methods = ["Get"])
def get_Home():
    home = dict()
    listJsonManga = []
    mangaDay= []
    newChapter = []
    session = requests.Session()
    rManga_base = session.get('https://mangajar.com/')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')    
    
    home_list = soupManga_base.find('div', class_='col-md-8 mb-2')
    numb = 1
    for homedemo in home_list.findAll('div', class_='card-body py-2'):
        
        article_class = homedemo.findAll('article', class_ = 'flex-item-mini mx-1 splide__slide')
        
        for item_manga in article_class:
                ItemJsonManga = dict()
                div_ItemJsonManga = item_manga.find('div', class_= 'poster-container')
                ItemJsonManga['manga_link'] = div_ItemJsonManga.find('a').get('href')
                ItemJsonManga['manga_title'] = div_ItemJsonManga.a['title']
                
                ItemJsonManga['manga_poster'] = div_ItemJsonManga.find('img').get('data-splide-lazy')
        
                div1_ItemJsonManga = item_manga.find('div', class_= 'manga-mini-last-chapter list-group-item position-absolute p-0 border-0')
                ItemJsonManga['link_chapter'] = div1_ItemJsonManga.find('a').get('href') 
                ItemJsonManga['chapter_name'] = div1_ItemJsonManga.a.text
                listJsonManga.append(ItemJsonManga)
        if numb == 1:
                home['top_manga_update']=  listJsonManga
                listJsonManga = []
        if numb == 2:
                home['new_trending']=  listJsonManga
                listJsonManga = []
        if numb == 3:
                home['Popular']=  listJsonManga
                listJsonManga = []
        if numb == 4:
                home['Recently_added']=  listJsonManga
                listJsonManga = []
        numb +=1
    
    fullListChapter = []
    for fullList in soupManga_base.findAll('span', class_= 'ml-2 d-inline-block'):
        full_list = dict()
        full_list['link'] = fullList.find('a').get('href')
        
        fullListChapter.append(full_list)
    home['full_list']=  fullListChapter
    
        
    for manga_day in soupManga_base.findAll('div', class_= 'col-md-4'):
        DayItemJsonManga = dict()     
        day_manga =  manga_day.find('article')        
        DayItemJsonManga['link_manga_day'] = day_manga.find('a').get('href')
        DayItemJsonManga['title_manga_day'] = day_manga.find('a').get('title')
        DayItemJsonManga['poster_manga'] = day_manga.find('img').get('data-src')
        
        mangaDay.append(DayItemJsonManga)
    home['manga_of_the_day']=  mangaDay
    
    
    table =  soupManga_base.find('div', style='max-height: 400px;overflow-x: hidden;')
    tbodyy = table.find('tbody')
    for new_chapter in tbodyy.findAll('tr'):    
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
        
        newChapter.append(newChapterJsonManga)
    home['new_chapter']=  newChapter
        
    return home



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

@app.route("/home/fullList", methods=["GET"])
def get_fullList():
    link_full = request.headers.get('Link-Full')
    print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listItemJsonchapter = []
    
    
    full_list = soupManga_base.find('form', class_='row w-100 filters-form')
    link_full_page = dict()
    full_link_manga = dict()
    seach = []
    numb = 1
    for manga_catalogue in full_list.findAll('select', class_='form-control selectpicker col-9'):
            
        optiondemo  = manga_catalogue.findAll('option')            
        for item_manga in optiondemo:
                ItemfullJsonManga = dict()

                ItemfullJsonManga['option'] = item_manga.text
                
                seach.append(ItemfullJsonManga)
        if numb == 1:
                full_link_manga['sort'] = seach
                seach = []
        if numb == 2:
                full_link_manga['genre'] = seach
                seach = []
                
        if numb == 3:
                full_link_manga['year'] = seach
                seach = []
        if numb == 4:
                full_link_manga['status'] = seach
                seach = []
        numb +=1
    
    
    link_full_page['seach'] = full_link_manga
    
    
    for list_item in soupManga_base.findAll('article', class_= 'flex-item card mx-1 mx-md-2 mb-3 shadow-sm rounded'):
        print(list_item)
        item = dict()
        item['link_detail']= list_item.find('a').get('href')
        item['title']= list_item.find('a').get('title')
        item['link_poster']= list_item.find('img').get('src')
        
        span = list_item.find('li', class_='card-numbers-item')
        item['name_chapter'] = span.find('span').text
        
        item['cart_text'] = list_item.find('p', class_='card-text').text
        li=list_item.find('li', class_='list-group-item px-1 py-1 small text-center')
        item['read_chapter'] = li.find('a').get('href')
        
        listItemJsonchapter.append(item)
    link_full_page['item'] = listItemJsonchapter
    
    
    list_page = []
    page_item = soupManga_base.find('ul', class_= 'pagination')
    page_number = page_item.findAll('a', class_='page-link')
    for link_page in page_number:
        pageItem = dict()
        pageItem['link_page']= link_page.get('href')
        pageItem['page_number']= link_page.text
        list_page.append(pageItem)
    link_full_page['page'] = list_page
    return link_full_page


@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    detailmanga = dict()
    
    content_detail = []
    for chapter in soupManga_base.findAll('div', class_= 'container manga-container'):
        FullDetailManga = dict()
        
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
        content_detail.append(FullDetailManga)   
    detailmanga['detail'] = content_detail
    
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
    detailmanga['list_chapter'] = listJsonchapter
    
      
    return detailmanga


@app.route("/detailmanga/pageItem", methods=["GET"])
def get_detail_pageItem():
    link_full = request.headers.get('Link-Full')
    print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    list_page = []
    page_item = soupManga_base.find('ul', class_= 'pagination')
    page_number = page_item.findAll('a', class_='page-link')
    for link_page in page_number:
        pageItem = dict()
        pageItem['link_page']= link_page.get('href')
        pageItem['page_number']= link_page.text
        list_page.append(pageItem)
    return list_page


if __name__ == '__main__':
    app.run()