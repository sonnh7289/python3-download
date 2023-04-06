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
    # soup = getdata(link_full)

    for itemmeta in soup.findAll('div', class_='banner_container'):
        ItemJson = {}
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['img'] = itemmeta.img['src']
        ItemJson['span'] = itemmeta.text
        listdData.append(ItemJson)
    for module in soup.findAll('div', class_='slot_products'):
        module1={}
        module1['module_a']=module.a['href']
        module1['module_span']=module.text
        listdData.append(module1)
    for bobyw in soup.findAll('li', class_='supplement supplement_link'):
        body={}
        body['body_link']=bobyw.a['href']
        listdData.append(body)
    for relea in soup.findAll('td', class_='top_releases_left'):
        rela={}
        rela['releases_href']=relea.a['href']
        rela['releases_img']=relea.img['src']  
        listdData.append(rela)
    for relearrr in soup.findAll('td', class_='top_releases_right'):
        relarr={}
        relarr['releases_href']=relearrr.a['href']
        relarr['releases_img']=relearrr.img['src']  
        listdData.append(relarr)
    for releasesright in soup.findAll('span', class_='title_col'):
        relar={}
        relar['reler_href']=releasesright.a['href']
        relar['reler_text']=releasesright.text

        listdData.append(relar)
    return listdData 
                
            
# phần game cả phần movie https://www.metacritic.com/browse/movies/release-date/theaters/date
# và phần tv and music
@app.route('/home/all', methods = ["GET"])
def get_all():
    link_full = request.headers.get('link_full')
    listdDataq=[]
    s = HTMLSession()
    # url='https://www.metacritic.com/game'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')    
        return soup    
    soupe = getdata(link_full)

    for newlink in soupe.findAll('div' , class_='product_image'):
        josonaq2={}
        josonaq2['newlink'] = newlink.a['href']
        josonaq2['newimg'] = newlink.img['src']
        listdDataq.append(josonaq2)
        
          
         
       
    for itemgame in soupe.findAll('td', class_='clamp-image-wrap'):        
        josona= dict()
        josona['link_img'] = itemgame.img['src']
        josona['link'] = itemgame.a['href']
        listdDataq.append(josona)
        for wrap in soupe.findAll('td', class_='clamp-summary-wrap'):   
            josona3={}
            
            josona3['summary'] = wrap.a['href']
            listdDataq.append(josona3)
            josona3['time_update'] = wrap.text.strip() 
        # for itemSpanw in wrap.findAll('div', class_='clamp-details'):
        #     josona1={}
        #     josona1['time_update'] = itemSpanw.text.strip() 
        #     listdDataq.append(josona1)
    return listdDataq 
    
# thông tin game  
@app.route('/home/rats', methods = ["GET"])
def get_rats():
    link_full = request.headers.get('link_full')
    listdDataq=[]
    s = HTMLSession()
    # url='https://www.metacritic.com/game/playstation-5/curse-of-the-sea-rats?fbclid=IwAR17_fdkNXy8H91lq-hG04hgbs0gPhJ3t3bB0HENr3Pf053gj78Q_jeA4VM'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')    
        return soup    
    soupe = getdata(link_full)   
    # soupe = getdata(link_full)
    # print(soupe)
    for itemgame in soupe.findAll('div', class_='module product_data product_data_summary'):
        
        josona= dict()
        josona['link_anh'] = itemgame.img['src']
        josona['link_reviews']=itemgame.a['href']
        josona['text']=itemgame.text
        # print(josona) 

    #     for timetex in soupe.findAll('td', class_='clamp-summary-wrap'):
        
    #         josona['link'] = timetex.a['href']
    #         for itemSpanw in timetex.findAll('div', class_='clamp-details'):
            
    #             josona['time_update'] = itemSpanw.text.strip()
    #             # for chu in timetex.findAll('div', class_='summary'):
    #             #     josona['chuq'] = chu.text
    listdDataq.append(josona)
    return listdDataq        
        
   

# @app.route('/home/date', methods = ["GET"])
# def get_date():

#     link_full = request.headers.get('link_full')
#     listdDataw=[]
#     s = HTMLSession()
#     # url='https://www.metacritic.com/browse/games/release-date/new-releases/all/date'
    
    
#     def getdata(url):
#         r=s.get(url)
#         soup=BeautifulSoup(r.text, 'html.parser')    
#         return soup    
#     soupe = getdata(link_full)   

    
#     for newlink in soupe.findAll('div' , class_='product_image'):#day
#             josonaq= dict()
#             josonaq['newlink'] = newlink.a['href']#day
#             josonaq['newimg'] = newlink.img['src']
#             for platform in soupe.findAll('div', class_='platform_wrap'):
#                 josonaq['newplatfom'] = platform.a['href']
#                 for wards in soupe.findAll('div', class_='body_wrap'):
#                     josonaq['wardsa'] = wards.a['href']
#                     for itemgame in soupe.findAll('table', class_='clamp-list'):
#             # print(itemgame) 
#                         josona= dict()
#                         josona['link_game'] = itemgame.img['src']
        

#                         for timetex in soupe.findAll('td', class_='clamp-summary-wrap'):
                        
#                             josona['link'] = timetex.a['href']
#                             for itemSpanw in timetex.findAll('div', class_='clamp-details'):
                            
#                                 josona['time_update'] = itemSpanw.text.strip()

                                
# tìm kiếm game
@app.route('/seach', methods=["GET"])
def seach():
        link_full = request.headers.get('link_full')
        seach = []
        s = HTMLSession()
        # url = f'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page={index}&fbclid=IwAR3bvfe8veIW0C0ZBqRJtUZjR8HX8yoQVjto7uS8JFkkqsRTR7XVTNllv1Y'
        # url = 'https://www.metacritic.com/search/game/results?plats[72496]=1&search_type=advanced'
       
        def getdata(url):
            r = s.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup

        soupe = getdata(link_full)
        # print(soupe)
        for itemgame in soupe.findAll('div', class_='result_wrap'):
            # print(itemgame)
            josona = dict()
            josona['link_anh'] = itemgame.img['src']
            josona['text'] = itemgame.text.strip()
            josona['link'] = itemgame.a['href']

            # for timetex in soupe.findAll('td', class_='clamp-summary-wrap'):

              
                # for itemSpanw in timetex.findAll('div', class_='clamp-details'):
                    
                    # for chu in timetex.findAll('div', class_='summary'):
                    #     josona['chuq'] = chu.text
        
            
            seach.append(josona)
        
        return seach   


@app.route('/home/movie', methods=["GET"])
def get_movie():
    # link_full = request.headers.get('link_full')
    listdData=[]
    s = HTMLSession()
    url='https://www.metacritic.com/movie'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
        return soup

    soup = getdata(url)
    # soup = getdata(link_full)

    for itemmeta in soup.findAll('div', class_='img_wrapper'):
        ItemJson = {}
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['img'] = itemmeta.img['src']
       
        listdData.append(ItemJson)
    for custom in soup.findAll('div', class_='custom_item'):
        item={}
        item['item_href']=custom.a['href']
        item['span']=custom.text.strip()
        listdData.append(item)
       

    for trailes in soup.findAll('tr', class_='list_item'):
        traile={}
        traile['triales_link']=trailes['data-bgimg']
        traile['triales_data-mctrailerurl']=trailes['data-mctrailerurl']
        traile['triales_data-mcvideourll']=trailes['data-mcvideourl']
        traile['triales_data-mcsummaryurl']=trailes['data-mcsummaryurl']
        traile['triales_data-mctrailerimg']=trailes['data-mctrailerimg']

        listdData.append(traile)
    return listdData    




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5353)
