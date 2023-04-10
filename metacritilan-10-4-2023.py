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
    # url='https://www.metacritic.com/game/playstation-5/resident-evil-4?fbclid=IwAR1l02QVNMNMiUj3_EirS9FU479XNxIbfVNsVaakeYfWg-di0upb2QUqH9Y'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')    
        return soup    
    soupe = getdata(link_full)   
    # soupe = getdata(url)
    # print(soupe)
    for itemgame in soupe.findAll('div', class_='left'):
        
        josona= dict()
        josona['link_anh'] = itemgame.img['src']
        josona['link_reviews']=itemgame.a['href']
        josona['text']=itemgame.text
        listdDataq.append(josona)
    for timetex in soupe.findAll('div', class_='module critic_user_reviews'):
        josona3= {}
        josona3['link'] = timetex.a['href']
        listdDataq.append(josona3)
    for itemSpanw in timetex.findAll('div', class_='review_btm review_btm_r'):
        josona4= {}
        josona4['comment'] = itemSpanw.text
        # for chu in timetex.findAll('div', class_='summary'):
        #     josona['chuq'] = chu.text
        listdDataq.append(josona4)
    for itemnone in soupe.findAll('div', class_='ranking_title'):
        josona5= {}
        josona5['link_rankings'] = itemnone.a['href']         #supplement supplement_link
        josona5['text_rankings']=itemnone.text
        listdDataq.append(josona5)
    for itemnone3 in soupe.findAll('div', class_='body_wrap'):
        josona6= {}
        josona6['link_rankings'] = itemnone3.a['href']         #supplement supplement_link
        josona6['text_rankings']=itemnone3.text
        listdDataq.append(josona6)

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

@app.route("/new", methods=["GET"])
def get_new():
    # link_full = request.headers.get('link_full')
    listdData=[]
    s = HTMLSession()
    url='https://www.metacritic.com/news/'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
        return soup

    soup = getdata(url)
    # soup = getdata(link_full)

    for itemmeta in soup.findAll('div', class_='c-articleSummary c-articleSummary_featured'):
        ItemJson = {}
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['source_'] = itemmeta.source['srcset']
        ItemJson['img'] = itemmeta.img['src']
        ItemJson['text'] = itemmeta.text

       
        listdData.append(ItemJson)
    for custom in soup.findAll('div', class_='c-articleSummary c-articleSummary_latest'):
        item={}
        item['item_href']=custom.a['href']
        item['span']=custom.text
        listdData.append(item)
       


    return listdData  


@app.route("/new/tv", methods=["GET"])
def get_tv():
    link_full = request.headers.get('link_full')
    listdData=[]
    s = HTMLSession()
    # url='https://www.metacritic.com/feature/tv-premiere-dates?ref=fa'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
        return soup

    # soup = getdata(url)
    soup = getdata(link_full)

    for itemmeta in soup.findAll('div', class_='col main_col'):
        ItemJson = {}
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['text'] = itemmeta.text
        listdData.append(ItemJson)
       


    return listdData

@app.route("/review", methods=["GET"])
def get_review():
    link_full = request.headers.get('link_full')
    listdData=[]
    s = HTMLSession()
    # url='https://www.metacritic.com/movie/the-super-mario-bros-movie'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
        return soup

    # soup = getdata(url)
    soup = getdata(link_full)

    for itemmeta in soup.findAll('td', class_='maskedcenter'):
        ItemJson = {}
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['text'] = itemmeta.text
        
        listdData.append(ItemJson)
    for vod in itemmeta.findAll('div',id='videoContainer_wrapper'):
        ItemJson1 = {}
        ItemJson1['link_vd'] = vod['data-mcvideourl']
        listdData.append(ItemJson1)

    for fxdrow2 in soup.findAll('div', class_='fxdrow'):
        ItemJson2 = {}
        ItemJson2['href'] = fxdrow2.a['href']
        ItemJson2['text'] = fxdrow2.text
        listdData.append(ItemJson2)
       
       
    return listdData  
# lay phaanf new
@app.route("/str", methods=["GET"])
def get_str():
    # link_full = request.headers.get('link_full')
    listdData=[]
    s = HTMLSession()
    url='https://www.metacritic.com/feature/more/streaming?ref=fa'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
        return soup

    soup = getdata(url)
    # soup = getdata(link_full)

    for itemmeta in soup.findAll('div', class_='story_wrap has_story_img'):
        ItemJson = {}
        ItemJson['href'] = itemmeta.a['href']
        ItemJson['img'] = itemmeta.img['src']
        ItemJson['text'] = itemmeta.text

       
        listdData.append(ItemJson)
    for custom in soup.findAll('li', class_='supplement supplement_link'):
        item={}
        item['item_href']=custom.a['href']
        
        listdData.append(item)
    for custom2 in soup.findAll('li', class_='recent_comment_story'):
        custo={}
        custo['custom2_href'] = custom2.a['href']
        custo['custom2_img'] = custom2.img['src']
        custo['custom2_text'] = custom2.text

        listdData.append(custo)


    return listdData 


@app.route('/ngoaitruyen', methods = ["GET"])
def get_ngoaitruyen():
    link_full = request.headers.get('link_full')
    listdDataq=[]
    s = HTMLSession()
    # url='https://gamefaqs.gamespot.com/switch/395915-metroid-prime-remastered/cheats'
    def getdata(url):
        r=s.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')    
        return soup    
    soupe = getdata(link_full)   
    # soupe = getdata(url)
    # print(soupe)
    for itemgame in soupe.findAll('div', class_='span8'):

        
        josona= dict()
        # josona['link_anh'] = itemgame.get.style
        josona['link_reviews']=itemgame.a['href']
        josona['text']=itemgame.text
        listdDataq.append(josona)
        
    for link in soupe.findAll('a',class_='link_color'):
        fdfds={}
        fdfds['duonglink']=link['href']
        listdDataq.append(fdfds)
        
    for hrefhg in soupe.findAll('aside', class_='span4'):
        phan3={}  
        phan3['chu']=hrefhg.text
        listdDataq.append(fdfds)
    for gsdj in soupe.findAll('div',class_='content'):
        phan4={}
        phan4['duongdan']=gsdj.a['href']
        listdDataq.append(phan4)
        print(phan4)
    for link2 in soupe.findAll('img',class_='crop imgboxart'):
        fdfdse={}
        fdfdse['amh']=link2['src']
        listdDataq.append(fdfdse)
    return listdDataq

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3234)
