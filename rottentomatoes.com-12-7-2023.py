from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import mysql.connector
import sqlite3
import time
app = Flask(__name__)

#LẤY PHÂN LOẠI TRANG flim
@app.route("/home", methods=["GET"])
def get_Home():
    # link_full = requests.headers.get('Link-Full')
     
    listJsonflim = dict()
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    listJsonflim['NEWS TV THIS WEEK'] = []
    for itemflimLastUpdate in soupflim_base.findAll('a', class_='news-tile'):
        for flimLastUpdate in itemflimLastUpdate('tile-dynamic', orientation='landscape'):
            ItemJsonflim = dict()

            # LẤY link
            ItemJsonflim['link'] = itemflimLastUpdate.get('href')
            #lay ten
            ItemJsonflim['name_flim'] = flimLastUpdate.find('div', slot='caption').text.strip()

            #LẤY POSTER
            ItemJsonflim['poster_flim'] = flimLastUpdate.img['src']

            listJsonflim['NEWS TV THIS WEEK'].append(ItemJsonflim)
    json_data1 = json.dumps(listJsonflim['NEWS TV THIS WEEK'])
    
    try:
        conn = sqlite3.connect("./rottentomatoes2.db")
        c = conn.cursor()
        print("Connected to SQLite")
        sqlite_insert_with_param = """ 
                        INSERT INTO Home (attribute_name, attribute_value) VALUES (?, ?);"""
        values = ('NEWS TV THIS WEEK', json_data1)
        c.execute(sqlite_insert_with_param, values)
        conn.commit()
        c.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")   
            
            
    for inew in soupflim_base.findAll('section', id="media-lists"):
        id2 = inew.find_all('section', class_="dynamic-poster-list")
        # for id3 in id2:
        #     i3= i.find_all('tiles-carousel-responsive-item')
        #     for i5 in i3:
        #         a=i5.find('a').get('href')
        #         print(a)
        for i in id2:
            h= i.find('h2').text
            listJsonflim[h] = []
            i3= i.find_all('tiles-carousel-responsive-item')
            for i5 in i3:
                a=i5.find('a').get('href')
                print(a)
            i2 = i.find_all('tile-dynamic')
            for itemflimLastUpdate,i5 in zip(i2,i3):
                ItemJsonflim = dict()
                ItemJsonflim['poster_flim'] = itemflimLastUpdate.find('img').get('src')
                # a_element = itemflimLastUpdate.find('a')
                # if a_element:
                ItemJsonflim['link'] =  a=i5.find('a').get('href')
                # else:
                #     ItemJsonflim['link'] = inew.find('tiles-carousel-responsive-item',slot="tile").find('a').get('href')
                ItemJsonflim['name'] = itemflimLastUpdate.find('span').text.strip()
                listJsonflim[h].append(ItemJsonflim)
            json_data = json.dumps(listJsonflim[h])
            
            try:
                conn = sqlite3.connect("./rottentomatoes2.db")
                c = conn.cursor()
                print("Connected to SQLite")
                sqlite_insert_with_param = """ 
                                INSERT INTO Home (attribute_name, attribute_value) VALUES (?,?);"""
                values = (h, json_data)
                c.execute(sqlite_insert_with_param, values)
                conn.commit()
                c.close()

            except sqlite3.Error as error:
                print("Failed to insert Python variable into sqlite table", error) 
    
    return listJsonflim



        # NEW & UPCOMING MOVIES
        
@app.route("/popular", methods=["GET"])
def get_Popular():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                listPopularflim.append(ItemPopularflim)
    

    return listPopularflim



    # MOST POPULAR TV ON RT
    
@app.route("/movies", methods=["GET"])
def get_movies():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/movies_at_home/sort:popular')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim



#   NEW TV THIS WEEK

@app.route("/New", methods=["GET"])
def get_New():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/tv_series_browse/sort:newest')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim



    # POPULAR IN THEATERS
@app.route("/TV", methods=["GET"])
def get_TV():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                # ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                element = P.find('span',class_= 'smaller')
                if element:
                    ItemPopularflim['time_update'] = element.text.strip()
                else:
                    ItemPopularflim['time_update'] = None
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim



    #   POPULAR IN THEATERS

@app.route("/Best", methods=["GET"])
def get_Best():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim



#   LATEST CERTIFIED FRESH MOVIES

@app.route("/Fresh", methods=["GET"])
def get_Fresh():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/movies_at_home/critics:certified_fresh')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim



#   LATEST CERTIFIED FRESH MOVIES

@app.route("/h", methods=["GET"])
def get_h():
    # link_full = request.headers.get('Link-Full')
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/browse/movies_in_theaters/critics:certified_fresh,fresh~sort:newest')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    index=0

    for Popularflim in soupflim_base.findAll('div', class_='discovery-grids-container'):
        for Popular in Popularflim.findAll('div', class_='js-tile-link'):
            po = Popular.find_all('tile-dynamic', skeleton='panel')
            
            for P in po:
                
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                ItemPopularflim['poster'] = P.find('img').get('src')
                
                ItemPopularflim['name_flim'] = P.find('img').get('alt')

            # LÁY THỜI GIAN CẬP NHẬT
            
                ItemPopularflim['time_update'] = P.find('span',class_= 'smaller').text.strip()
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim


@app.route("/search", methods=["GET"])
def get_Search():
    textSearch = request.headers.get('text-search')
    textLinkSearch = textSearch.replace(' ', '%20')
    listJsonflim = dict()
    suays=[]
    session = requests.Session()
    linksearch = "https://www.rottentomatoes.com/search?search=" + textLinkSearch
    rflim_base = session.get(linksearch)
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    listJsonflim['movie'] = []
    listJsonflim['franchise'] = []
    listJsonflim['tvSeries'] = []
    listJsonflim['celebrity'] = []
    for typeSearch in soupflim_base.findAll('search-page-result',type="franchise"):    
        item = typeSearch.find_all('search-page-item-row')
        for flimLastUpdate in item:
            ItemJsonflim1 = dict()
           
            ItemJsonflim1['link'] = 'https://www.rottentomatoes.com/' + flimLastUpdate.find('a').get('href')
            #LẤY POSTER
            ItemJsonflim1['poster_flim'] = flimLastUpdate.find('a').img['src']
            #lay ten
            ItemJsonflim1['name_flim'] = flimLastUpdate.find('a').img['alt']
            listJsonflim['franchise'].append(ItemJsonflim1)
    
                    # 
    for typeSearch in soupflim_base.findAll('search-page-result',type="movie"):    
        item = typeSearch.find_all('search-page-media-row')
        for flimLastUpdate in item:
            ItemJsonflim2 = dict()
            
            ItemJsonflim2['link'] =  flimLastUpdate.find('a').get('href')
            #LẤY POSTER
            ItemJsonflim2['poster_flim'] = flimLastUpdate.find('a').img['src']
            #lay ten
            ItemJsonflim2['name_flim'] = flimLastUpdate.find('a').img['alt']
            listJsonflim['movie'].append(ItemJsonflim2)
    
    # 
    for typeSearch in soupflim_base.findAll('search-page-result', type="tvSeries"):    
        item = typeSearch.find_all('search-page-media-row')
        for flimLastUpdate in item:
            ItemJsonflim3 = dict()
            
            ItemJsonflim3['link'] = flimLastUpdate.find('a').get('href')
            #LẤY POSTER
            ItemJsonflim3['poster_flim'] = flimLastUpdate.find('a').img['src']
            #lay ten
            ItemJsonflim3['name_flim'] = flimLastUpdate.find('a').img['alt']
            listJsonflim['tvSeries'].append(ItemJsonflim3)
    # 
    for typeSearch in soupflim_base.findAll('search-page-result',type="celebrity"):    
        item = typeSearch.find_all('search-page-item-row')
        for flimLastUpdate in item:
            ItemJsonflim4 = dict()
            
            ItemJsonflim4['link'] = 'https://www.rottentomatoes.com/' + flimLastUpdate.find('a').get('href')
            #LẤY POSTER
            ItemJsonflim4['poster_flim'] = flimLastUpdate.find('a').img['src']
            #lay ten
            ItemJsonflim4['name_flim'] = flimLastUpdate.find('a').img['alt']
            listJsonflim['celebrity'].append(ItemJsonflim4)  
        
    return listJsonflim    

@app.route("/detail", methods=["GET"])
def get_Detail():
    linkDetail = request.headers.get('link-detail')
    detailFullFilm = dict()
    session = requests.Session()
    rflim_base = session.get(linkDetail)
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    for meta in soupflim_base.findAll('meta'):
        if meta.get('property') == 'og:title':
            detailFullFilm['title'] = meta.get('content')
        if meta.get('property') == 'og:description':
            detailFullFilm['description'] = meta.get('content')
        if meta.get('property') == 'og:image':
            detailFullFilm['image'] = meta.get('content')
            break
    detailFullFilm['listimages'] = []
    for div in soupflim_base.findAll('div',class_ = 'PhotosCarousel__item'):
        for img in div.findAll('img'):
            itemImage = dict()
            itemImage['image'] = img.get('src')
            detailFullFilm['listimages'].append(itemImage)
            break
    detailFullFilm['crewcasting'] = []
    for div in soupflim_base.findAll('div',class_ = 'cast-and-crew-item'):
        castItem = dict()
        for ahref in div.findAll('a'):
            castItem['link'] = ahref.get('href')
        for img in div.findAll('img'):
            castItem['name'] = img.get('alt')
            castItem['image'] = img.get('src')
            detailFullFilm['crewcasting'].append(castItem)
            break
    detailFullFilm['review'] = []
    for div in soupflim_base.findAll('review-speech-balloon'):
        reviewList = dict()
        reviewList['reviewquote'] = div.get('reviewquote')
        reviewList['createdate'] = div.get('createdate')
        reviewList['criticimageurl'] = div.get('criticimageurl')
        detailFullFilm['review'].append(reviewList)
    
    return detailFullFilm


if __name__ == "__main__":
   app.run(host='0.0.0.0')