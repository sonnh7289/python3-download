from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = Flask(__name__)

#LẤY PHÂN LOẠI TRANG flim
@app.route("/home", methods=["GET"])
def get_Home():
    # link_full = requests.headers.get('Link-Full')
    listJsonflim = dict()
    session = requests.Session()
    rflim_base = session.get('https://www.rottentomatoes.com/?fbclid=IwAR1EJtTrCMG7W_WEWnOj9mRK1suKjz_t2ATX_v3KlFJb4Bm9yMYlnZRMpiY')
    soupflim_base = BeautifulSoup(rflim_base.content, 'html.parser')
    listJsonflim['a'] = []
    for itemflimLastUpdate in soupflim_base.findAll('a', class_='news-tile'):
        for flimLastUpdate in itemflimLastUpdate('tile-dynamic', orientation='landscape'):
            ItemJsonflim = dict()

            # LẤY link
            ItemJsonflim['link'] = itemflimLastUpdate.get('href')
            #lay ten
            ItemJsonflim['name_flim'] = flimLastUpdate.find('div', slot='caption').text.strip()

            #LẤY POSTER
            ItemJsonflim['poster_flim'] = flimLastUpdate.img['src']

            listJsonflim['a'].append(ItemJsonflim)

    listJsonflim['b'] = []         
    for itemflimLastUpdate in soupflim_base.findAll('section', class_='dynamic-poster-list'):    
        for itemflimLastUpdate in soupflim_base.findAll('tiles-carousel-responsive', skeleton='panel'):
            for itemflim in itemflimLastUpdate.findAll('tiles-carousel-responsive-item', slot='tile'): 
                # ItemJsonflim['link'] = flim.a['href']
                for flim in itemflim.findAll('tile-dynamic'):
                    ItemJsonflim = dict()

                    ItemJsonflim['poster_flim'] = flim.img['src']

                    for f in flim.findAll('a'):
                        
                        ItemJsonflim['link'] = f.get('href')
                        
                    for f in flim.findAll('span', class_='sr-only'):
                        ItemJsonflim['name'] = f.text.strip()
                       
                listJsonflim['b'].append(ItemJsonflim)

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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
            # LẤY LINK

                ItemPopularflim['link'] = P.a['href']

                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)

            # LÁY THỜI GIAN CẬP NHẬT

            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
                ItemPopularflim['link'] = P.a['href']
                            
                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)
            
            # LÁY THỜI GIAN CẬP NHẬT
            
            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
                ItemPopularflim['link'] = P.a['href']
                            
                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)
            
            # LÁY THỜI GIAN CẬP NHẬT
            
            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
                ItemPopularflim['link'] = P.a['href']
                            
                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)
            
            # LÁY THỜI GIAN CẬP NHẬT
            
            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
                ItemPopularflim['link'] = P.a['href']
                            
                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)
            
            # LÁY THỜI GIAN CẬP NHẬT
            
            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
                ItemPopularflim['link'] = P.a['href']
                            
                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)
            
            # LÁY THỜI GIAN CẬP NHẬT
            
            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
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
            
            for P in Popular.findAll('tile-dynamic', skeleton='panel'):
            
                ItemPopularflim = dict()
            
                ItemPopularflim['link'] = P.a['href']
                            
                listPopularflim.append(ItemPopularflim)
            # LẤY poster
            for P in Popular.findAll('img', class_='posterImage'):
        
                ItemPopularflim = dict()
            
                ItemPopularflim['poster'] = P.get('src')
                
                ItemPopularflim['name_flim'] = P.get('alt')
                
                listPopularflim.append(ItemPopularflim)
            
            # LÁY THỜI GIAN CẬP NHẬT
            6532
            for itemSpan in Popular.findAll('span', class_= 'smaller'):
                ItemPopularflim['time_update'] = itemSpan.text.strip()
                listPopularflim.append(ItemPopularflim)
                                    
    return listPopularflim
    

if __name__ == "__main__":
   app.run(host='0.0.0.0')