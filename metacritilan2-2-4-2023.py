from flask import Flask, jsonify, request
from flask_restful import Api, Resource
# from python_utils import beetoon_api
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
@app.route("/home", methods=["GET"])
def get_Home():
    # link_full = request.headers.get('link_full')
    listdData=[]
    s = HTMLSession()
    url='https://www.metacritic.com/'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
        return soup

    soup = getdata(url)


    
    soupf= soup.find('table', class_='banner_table')
    # print(fhajh)
   
    for itemmeta in soupf.findAll('div', class_='banner_container'):
        ItemJson = dict()
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['link'] = itemmeta.img['src']
        ItemJson['span'] = itemmeta.text
        # print(itemmeta)
        # print('---------------------------------------------------------------')
        # spans=itemManga.find('', class_='hpb_item_deck')
        listdData.append(ItemJson)
        # print(listdData)

        for itemtd in soup.findAll('table', class_='top_releases'):
            Itemtds = dict()
            Itemtds['href'] = itemtd.img['src']
            Itemtds['thea'] = itemtd.a['href']
            listdData.append(Itemtds)
            # print(Itemtds)
        
        
            for aheas in soup.findAll('a', class_='title'):
                dfs = dict()
                dfs['thera']=aheas.text
                dfs['hrefr']=aheas.get('href')
                listdData.append(dfs)
              
            return listdData
                
            


@app.route('/home/game', methods = ["GET"])
def get_game():
    listdDataq=[]
    s = HTMLSession()
    url='https://www.metacritic.com/game'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')    
        return soup    
    soupe = getdata(url)   

    for itemgame in soupe.findAll('table', class_='clamp-list'):
        # print(itemgame) 
        josona= dict()
        josona['link_game'] = itemgame.img['src']
    

        for timetex in soupe.findAll('td', class_='clamp-summary-wrap'):
        
            josona['link'] = timetex.a['href']
            for itemSpanw in timetex.findAll('div', class_='clamp-details'):
            
                josona['time_update'] = itemSpanw.text.strip()
                # for chu in timetex.findAll('div', class_='summary'):
                #     josona['chuq'] = chu.text
            listdDataq.append(josona)
        return listdDataq
    
    
        
        
   

@app.route('/home/date', methods = ["GET"])
def get_date():

    link_full = request.headers.get('link_full')
    listdDataw=[]
    s = HTMLSession()
    # url='https://www.metacritic.com/browse/games/release-date/new-releases/all/date'
    
    
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')    
        return soup    
    soupe = getdata(link_full)   

    
    for newlink in soupe.findAll('div' , class_='product_image'):#day
            josonaq= dict()
            josonaq['newlink'] = newlink.a['href']#day
            josonaq['newimg'] = newlink.img['src']
            for platform in soupe.findAll('div', class_='platform_wrap'):
                josonaq['newplatfom'] = platform.a['href']
                for wards in soupe.findAll('div', class_='body_wrap'):
                    josonaq['wardsa'] = wards.a['href']
                    for itemgame in soupe.findAll('table', class_='clamp-list'):
            # print(itemgame) 
                        josona= dict()
                        josona['link_game'] = itemgame.img['src']
        

                        for timetex in soupe.findAll('td', class_='clamp-summary-wrap'):
                        
                            josona['link'] = timetex.a['href']
                            for itemSpanw in timetex.findAll('div', class_='clamp-details'):
                            
                                josona['time_update'] = itemSpanw.text.strip()

@app.route('/seach', methods=["GET"])
def seach():
    index=0
    while True:
        seach = []
        s = HTMLSession()
        url = f'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page={index}&fbclid=IwAR3bvfe8veIW0C0ZBqRJtUZjR8HX8yoQVjto7uS8JFkkqsRTR7XVTNllv1Y'
        index +=1
        def getdata(url):
            r = s.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup

        soupe = getdata(url)

        for itemgame in soupe.findAll('table', class_='clamp-list'):
            # print(itemgame)
            josona = dict()
            josona['link_game'] = itemgame.img['src']

            for timetex in soupe.findAll('td', class_='clamp-summary-wrap'):

                josona['link'] = timetex.a['href']
                for itemSpanw in timetex.findAll('div', class_='clamp-details'):
                    josona['time_update'] = itemSpanw.text.strip()
                    # for chu in timetex.findAll('div', class_='summary'):
                    #     josona['chuq'] = chu.text
                seach.append(josona)
        if index == 2:
            break
    return seach

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3250)




                    
        

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3250)       
            
    




        
