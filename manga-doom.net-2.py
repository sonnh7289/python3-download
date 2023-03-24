from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = Flask(__name__)

#LẤY PHÂN LOẠI TRANG MANGA
@app.route("/home", methods=["GET"])
def get_Home():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga = dict()

    listJsonManga['Popular_Update'] = []
    for PopularUpdateManga in soupManga_base.findAll('div', class_='item'):
        ItemPopularUpdateManga = dict()
        
        # LẤY TÊN
        ItemPopularUpdateManga['name_manga'] = PopularUpdateManga.a['title']

        # LẤY LINK
        ItemPopularUpdateManga['link_manga'] = PopularUpdateManga.a['href']

        # LẤY POSTER
        ItemPopularUpdateManga['poster_manga'] = PopularUpdateManga.img['src']

        listJsonManga['Popular_Update'].append(ItemPopularUpdateManga)

    listJsonManga['Latest'] = []
    for itemMangaLastUpdate in soupManga_base.findAll('dl'):
        LastUpdate = dict()
        
        # LẤY TÊN
        LastUpdate['name_manga'] = itemMangaLastUpdate.a['title']

        #LẤY DATA INFO
        LastUpdate['data_info'] = itemMangaLastUpdate.a['data-info']

        # LẤY LINK
        LastUpdate['link_manga'] = itemMangaLastUpdate.a['href']

        #LẤY TÁC GIẢ
        if itemMangaLastUpdate.dd is not None:
            LastUpdate['Author'] = itemMangaLastUpdate.dd.text.strip()

        # LẤY POSTER
        LastUpdate['poster_manga'] = itemMangaLastUpdate.img['src']

        # LÁY THỜI GIAN CẬP NHẬT
        LastUpdate['time_update'] = itemMangaLastUpdate.find('span', class_='time hidden-xs').text.strip()
        
        #LẤY CÁC CHAPTER
        # LastUpdate['list_chapter'] = []    
        # for cha in itemMangaLastUpdate.findAll('dd'):
        #     chapter = {}
        #     chapter['link_chapter'] = cha.find('a').get('href')
        #     chapter['name_chapter'] = cha.a.text.strip()
        #     LastUpdate['list_chapter'].append(chapter)

        listJsonManga['Latest'].append(LastUpdate)

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

            for p1 in PopularManga.findAll('p', class_='post-meta'):
                # LẤY THỜI GIAN 
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['time'] = p11.text.strip()
                index+=1

                listJsonManga['Popular_Manga'].append(itemPopularManga)

    listJsonManga['Genres'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-text-list'):
        for Genres in ul.findAll('li'):
            itemGenres = dict()
            itemGenres['Name'] = Genres.text.strip()
            itemGenres['Link'] = 'https://manga-doom.com'+Genres.a['href']

            listJsonManga['Genres'].append(itemGenres)
            
    
    return listJsonManga


#LẤY CHI TIẾT THÔNG TIN MANGA
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    FullDetailManga = dict()
    ListDetailManga = dict()
    index = 0

    ListDetailManga['info'] = []
    for meta in soupManga_base.findAll('dl', class_='dl-horizontal'):
        
        #LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Alternative Name:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Alternative_Name'] = alt.text.strip()
            index+=1
        
        #LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Status:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Status'] = alt.text.strip()
            index+=1

        #LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Categories:':
                FullDetailManga['Categories'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Type'] = alt.text.strip()
            index+=1

        #LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Author:':
                FullDetailManga['Author'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Artist:':
                for alt in soupManga_base.findAll('dd')[index]:
                    FullDetailManga['Artist'] = alt.text.strip()
            index+=1

        # LẤY SHARE
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Share':
                for alt in soupManga_base.findAll('dd')[index]:
                    if alt is not None:
                        FullDetailManga['Share'] = alt.text.strip()
            index+=1


    # LẤY GIỚI THIỆU TRUYỆN
    if soupManga_base.find('div', class_='note note-default margin-top-15') is not None:
        FullDetailManga['info'] = soupManga_base.find('div', class_='note note-default margin-top-15').text.strip()


    # LẤY CÁC CHAP TRUYỆN
    FullDetailManga['list_chapter'] = []    
    for cha in soupManga_base.findAll('ul', class_='chapter-list'):
        for chap in cha.findAll('li'):
            chapter = {}
            chapter['link_chapter'] = chap.find('a').get('href')
            if chap.find('span', class_='val') is not None:
                chapter['name_chapter'] = chap.find('span', class_='val').text.strip()
            if chap.find('span', class_='date') is not None:
                chapter['release_date'] = chap.find('span', class_='date').text.strip()
            FullDetailManga['list_chapter'].append(chapter)

    ListDetailManga['info'].append(FullDetailManga)

    ListDetailManga['Popular_Manga'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-post-list list-numbering'):
        for PopularManga in ul.findAll('div', class_='caption'):
            itemPopularManga = dict()
            index = 0

            for p in PopularManga.findAll('p', class_='category'):
                # LẤY TÊN MANGA
                itemPopularManga['name_manga'] = p.text.strip()

                # LẤY LINK MANGA
                itemPopularManga['link_manga'] = p.a['href']

            for p1 in PopularManga.findAll('p', class_='post-meta'):
                # LẤY THỜI GIAN 
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['time'] = p11.text.strip()
                index+=1

                ListDetailManga['Popular_Manga'].append(itemPopularManga)

    ListDetailManga['Genres'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-text-list'):
        for Genres in ul.findAll('li'):
            itemGenres = dict()
            itemGenres['Name'] = Genres.text.strip()
            itemGenres['Link'] = 'https://manga-doom.com'+Genres.a['href']

            ListDetailManga['Genres'].append(itemGenres)

    return ListDetailManga


#LẤY ẢNH CHAPTER
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


#LẤY PHÂN LOẠI TRANG MANGA
@app.route("/directory", methods=["GET"])
def get_Directory():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listDirectory = dict()

    listDirectory['Word'] = []
    for itemWord in soupManga_base.findAll('h5', class_='widget-heading'):
        for itemW in itemWord.findAll('a'):
            Item = dict()

            # LẤY LINK
            Item['link_word'] = itemW.get('href')

            # LẤY CHỮ CÁI
            Item['word'] = itemW.text.strip()

            listDirectory['Word'].append(Item)


    listDirectory['Manga'] = []
    for itemMangaDirectory in soupManga_base.findAll('a', class_='manga-info-qtip'):
        ItemDirectory = dict()

        # LẤY TÊN
        ItemDirectory['name_manga'] = itemMangaDirectory.text.strip()

        # LẤY LINK
        ItemDirectory['full_manga'] = itemMangaDirectory['href']

        # LẤY POSTER
        ItemDirectory['data_manga'] = itemMangaDirectory['data-info']

        
        listDirectory['Manga'].append(ItemDirectory)
        
    return listDirectory


#LẤY MANGA PHỔ BIẾN
@app.route("/popular", methods=["GET"])
def get_Popular():
    link_full = request.headers.get('Link-Full')
    listPopularManga = dict()
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    # index=0

    listPopularManga['Left'] = []
    for meta in soupManga_base.findAll('div', class_='row manga-list-style'):
        ItemPopularManga = dict()

        ItemPopularManga['link'] = meta.a['href']

        ItemPopularManga['poster'] = meta.img['src']

        ItemPopularManga['Name'] = meta.a['title']
        index = 0
        index+=1

        #LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Alternative Name:':
                ItemPopularManga['Alternative_Name'] = meta.findAll('dd')[index].text.strip()
            index+=1
        
        #LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Status:':
                ItemPopularManga['Status'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Categories:':
                ItemPopularManga['Categories'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                ItemPopularManga['Type'] = meta.findAll('dd')[index].text.strip()
            index+=1
    
        # LẤY TÁC GIẢ
        ItemPopularManga['Author'] = []
        for head in soupManga_base.findAll('dt')[index]:     
            Author = dict() 
            if head.text.strip() == 'Author:':
                Author['Author'] = meta.findAll('dd')[index].text.strip()
                Author['Author_link'] = 'https://manga-doom.com'+meta.findAll('dd')[index].a['href']
            index+=1
            ItemPopularManga['Author'].append(Author)

        # LẤY ARTIST
        ItemPopularManga['Artist'] = []
        for head in soupManga_base.findAll('dt')[index]:      
            Artist = dict()
            if head.text.strip() == 'Artist:':
                Artist['Artist'] = meta.findAll('dd')[index].text.strip()
                Artist['Artist_link'] = 'https://manga-doom.com'+meta.findAll('dd')[index].a['href']
            index+=1
            ItemPopularManga['Artist'].append(Artist)

        listPopularManga['Left'].append(ItemPopularManga)

    listPopularManga['Right'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-post-list list-numbering'):
        for PopularManga in ul.findAll('div', class_='caption'):
            itemPopularManga = dict()
            index = 0

            for p in PopularManga.findAll('p', class_='category'):
                # LẤY TÊN MANGA
                itemPopularManga['name_manga'] = p.text.strip()

                # LẤY LINK MANGA
                itemPopularManga['link_manga'] = p.a['href']

            for p1 in PopularManga.findAll('p', class_='post-meta'):
                # LẤY THỜI GIAN 
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['time'] = p11.text.strip()
                index+=1

                listPopularManga['Right'].append(itemPopularManga)

    listPopularManga['Genres'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-text-list'):
        for Genres in ul.findAll('li'):
            itemGenres = dict()
            itemGenres['Name'] = Genres.text.strip()
            itemGenres['Link'] = 'https://manga-doom.com'+Genres.a['href']

            listPopularManga['Genres'].append(itemGenres)

    return listPopularManga

@app.route("/latest", methods=["GET"])
def get_Latest():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga = dict()

    listJsonManga['Latest'] = []
    for itemMangaLatest in soupManga_base.findAll('dl'):
        Popular = dict()
        # LẤY TÊN
        Popular['name_manga'] = itemMangaLatest.a['title']

        #LẤY DATA INFO
        Popular['data_info'] = itemMangaLatest.a['data-info']

        #LẤY TÁC GIẢ
        if itemMangaLatest.dd is not None:
            Popular['Author'] = itemMangaLatest.dd.text.strip()

        # LẤY LINK
        Popular['link_manga'] = itemMangaLatest.a['href']

        # LẤY POSTER
        Popular['poster_manga'] = itemMangaLatest.img['src']

        # LÁY THỜI GIAN CẬP NHẬT
        Popular['time_update'] = itemMangaLatest.find('span', class_='time hidden-xs').text.strip()
        
        #LẤY CÁC CHAPTER
        # Popular['list_chapter'] = []    
        # for cha in itemMangaLastUpdate.findAll('dd'):
        #     chapter = {}
        #     chapter['link_chapter'] = cha.find('a').get('href')
        #     chapter['name_chapter'] = cha.a.text.strip()
        #     Popular['list_chapter'].append(chapter)

        listJsonManga['Latest'].append(Popular)

    listJsonManga['Popular'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-post-list list-numbering'):
        for PopularManga in ul.findAll('div', class_='caption'):
            itemPopularManga = dict()
            index = 0

            for p in PopularManga.findAll('p', class_='category'):
                # LẤY TÊN MANGA
                itemPopularManga['name_manga'] = p.text.strip()

                # LẤY LINK MANGA
                itemPopularManga['link_manga'] = p.a['href']

            for p1 in PopularManga.findAll('p', class_='post-meta'):
                # LẤY THỜI GIAN 
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['time'] = p11.text.strip()
                index+=1

                listJsonManga['Popular'].append(itemPopularManga)

    listJsonManga['Genres'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-text-list'):
        for Genres in ul.findAll('li'):
            itemGenres = dict()
            itemGenres['Name'] = Genres.text.strip()
            itemGenres['Link'] = 'https://manga-doom.com'+Genres.a['href']

            listJsonManga['Genres'].append(itemGenres)
    
    return listJsonManga


#LẤY TRANG SEARCH
@app.route("/search", methods=["GET"])
def get_Search():
    link_full = request.headers.get('Link-Full')
    listSearchManga = dict()
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')

    listSearchManga['Popular'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-post-list list-numbering'):
        for PopularManga in ul.findAll('div', class_='caption'):
            itemPopularManga = dict()
            index = 0

            for p in PopularManga.findAll('p', class_='category'):
                # LẤY TÊN MANGA
                itemPopularManga['name_manga'] = p.text.strip()

                # LẤY LINK MANGA
                itemPopularManga['link_manga'] = p.a['href']

            for p1 in PopularManga.findAll('p', class_='post-meta'):
                # LẤY THỜI GIAN 
                for p11 in p1.findAll('span')[index]:
                    itemPopularManga['time'] = p11.text.strip()
                index+=1

                listSearchManga['Popular'].append(itemPopularManga)

    listSearchManga['Genres'] = []
    for ul in soupManga_base.findAll('ul', class_='widget-text-list'):
        for Genres in ul.findAll('li'):
            itemGenres = dict()
            itemGenres['Name'] = Genres.text.strip()
            itemGenres['Link'] = 'https://manga-doom.com'+Genres.a['href']

            listSearchManga['Genres'].append(itemGenres)

    return listSearchManga

#LẤY TẤT CẢ THỂ LOẠI
@app.route("/allgenres", methods=["GET"])
def get_AllGenres():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listGenresManga = []

    for meta in soupManga_base.findAll('ul', class_='manga-list circle-list'):
        i=0
        for met in meta.findAll('li'):
            itemGenresManga = dict()

            #LẤY TÊN THỂ LOẠI
            itemGenresManga['Name'] = met.text.strip()

            #LẤY LINK THỂ LOẠI
            itemGenresManga['Link'] = met.find('a').get('href')

            listGenresManga.append(itemGenresManga)

    return listGenresManga

#LẤY TRUYỆN TỪ THỂ LOẠI
@app.route("/genres", methods=["GET"])
def get_Genres():
    link_full = request.headers.get('Link-Full')
    listGenresManga = []
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')


    for meta in soupManga_base.findAll('dl', class_='dl-horizontal'):
        
        index = 0
        index += 1
        ItemGenresManga = dict()

        ItemGenresManga['link'] = meta.a['href']

        ItemGenresManga['Name'] = meta.a['title']

        #LẤY TÊN THAY THẾ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Alternative Name:':
                ItemGenresManga['Alternative_Name'] = meta.findAll('dd')[index].text.strip()
            index+=1
        
        #LẤY TRẠNG THÁI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Status:':
                ItemGenresManga['Status'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY THỂ LOẠI
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Categories:':
                ItemGenresManga['Categories'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY KIỂU TRUYỆN
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Type :':
                ItemGenresManga['Type'] = meta.findAll('dd')[index].text.strip()
            index+=1

        #LẤY TÁC GIẢ
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Author:':
                ItemGenresManga['Author'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY ARTIST
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Artist:':
                ItemGenresManga['Artist'] = meta.findAll('dd')[index].text.strip()
            index+=1

        # LẤY SHARE
        for head in soupManga_base.findAll('dt')[index]:      
            if head.text.strip() == 'Share':
                for alt in soupManga_base.findAll('dd')[index]:
                    if alt is not None:
                        ItemGenresManga['Share'] = alt.text.strip()
            index+=1

        listGenresManga.append(ItemGenresManga)

    return listGenresManga

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=28883)