from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import json
app = Flask(__name__)

@app.route("/search", methods=["GET"])
def searchManga():
    listJsonManga = {}
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga['latest_uptate'] = 'READ MANGA ONLINE - LATEST UPDATES'
    chapter=soupManga_base.find('div',class_='content-homepage-item-right') 
    link_full= []
    
    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all('div', class_='search-story-item'):    
        item={}
        item2={}
        item['title'] =itemMangaLastUpdate.find('a', class_='item-img').text
        item['link']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.a['href']
        item['poster']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.img['src']
        item['authod']=itemMangaLastUpdate.find('span',class_='text-nowrap item-author').text
        index2 = 0
        link_full2= [] 
        for chap in  itemMangaLastUpdate.find_all('a',class_='item-chapter a-h text-nowrap'):
            item2 = 'https://ww5.manganelo.tv' +  chap.get('href')
            link_full2.append(item2)
            item['chapter_home']=link_full2
        indexRun = indexRun + 1    
        link_full.append(item)            
    listJsonManga['manga_link'] = link_full
    return listJsonManga


@app.route("/categorieslist", methods=["GET"])
def categorieslist():
    listJsonManga = {}
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga['latest_uptate'] = 'READ MANGA ONLINE - LATEST UPDATES'
    chapter=soupManga_base.find('div',class_='content-homepage-item-right') 
    link_full= []
    
    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all('div', class_='content-genres-item'):    
        item={}
        item2={}
        item['title'] =itemMangaLastUpdate.find('a', class_='genres-item-img').text
        item['link']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.a['href']
        item['poster']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.img['src']
        item['descript_note']=itemMangaLastUpdate.find('div',class_='genres-item-description').text
        index2 = 0
        link_full2= [] 
        for chap in  itemMangaLastUpdate.find_all('a',class_='genres-item-chap text-nowrap a-h'):
            item2 = 'https://ww5.manganelo.tv' +  chap.get('href')
            link_full2.append(item2)
            item['chapter_home']=link_full2
        indexRun = indexRun + 1    
        link_full.append(item)            
    listJsonManga['manga_link'] = link_full
    return listJsonManga

#Lấy category ở home
#Lấy link chapter
@app.route("/homenelo", methods=["GET"])
def get_Home():
    listJsonManga = {}
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga['latest_uptate'] = 'READ MANGA ONLINE - LATEST UPDATES'
    chapter=soupManga_base.find('div',class_='content-homepage-item-right') 
    link_full= []
    
    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all('div', class_='content-homepage-item'):    
        item={}
        item2={}
        item['title'] =itemMangaLastUpdate.find('a', class_='tooltip a-h text-nowrap').text
        item['link']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.a['href']
        item['poster']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.img['data-src']
        item['author_home']=itemMangaLastUpdate.find('span',class_='text-nowrap item-author').text.replace("\r","").replace("\n"," ").replace(" ","")
        index2 = 0
        link_full2= [] 
        for chap in  itemMangaLastUpdate.find_all('p',class_='a-h item-chapter'):
            item2 = chap.text.replace("\r","-").replace("\n"," ") 
            link_full2.append(item2)
            item['chapter_home']=link_full2
        indexRun = indexRun + 1    
        link_full.append(item)            
    listJsonManga['manga_link'] = link_full
    return listJsonManga
#Lấy category ở home
@app.route("/category_home", methods=["GET"])
def get_category():
    listJsonMang = {}
    item=[]
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonMang['genres']='MANGA BY GENRES'
    soup=soupManga_base.find('div', class_='panel-category')
    category=soup.find_all('p', class_='pn-category-row')
    list_cate=[]
    for item in category:
        text_cate=item.text.replace("\r","").replace("\n"," ")
        list_cate.append(str(text_cate))
    listJsonMang['category_home'] = list_cate
    return listJsonMang
#lấy thông tin của manga
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    detail = {}
    data1 = soup.find('table',class_='variations-tableInfo')
    lis = []
    def ac ():
        name_imgs = data1.find_all('tr')
        lis = []
        for i in name_imgs[3]:
            text_a = i.text.replace("\r","").replace("\n","").replace(" - ",",").replace(" ","")
            lis.append(str(text_a)) 
        del lis[0:3]
        return lis[:-1]
    #LẤY POSTER
    detail['poster_manga'] = 'https://ww5.manganelo.tv' + soup.find('div', class_='story-info-left').find('img', class_="img-loading").get('src')
    df = soup.find_all('h1')
    #LẤY TIÊU ĐỀ
    for i in df:
        detail['title_manga'] = i.text
    #LẤY AUTHOR
    list_au=[]
    for au in data1.find_all('td', class_='table-value'):
        text_au=au.text.replace("\r","").replace("\n"," ")
        list_au.append(text_au)
    detail['author']=list_au[1]
    #LẤY DESCRIPTIONS
    des = soup.find('div' , class_='story-info-right').findAll('h2')
    for ii in des:
        detail['descriptions'] = ii.text.replace("\r","").replace("\n","").replace(" ","")
    #Lấy status
    status=soup.find('div', class_='story-info-right').find_all('tr')
    for st in status[2].find('td', class_='table-value'):
        detail['status']=st.text.strip()
    #Lấy thể loại
    for li in data1.find_all("tr"):
        detail['categories'] = ac()
    detail['last_update'] = "27/12/2014"
    #Lấy lượt xem
    view=soup.find('div', class_='story-info-right-extent').find_all('p')
    for st in view[1].find('span', class_='stre-value'):
        detail['View']=st.text.strip()  
    #lấy xếp hạng
    list_xh=[]
    for xh in view:
        text=xh.text.replace("\r","").replace("\n","")
        list_xh.append(text)
    detail['Rating']=list_xh[3]
    #LẤY IMG BOOKMARK
    view2=soup.find('div', class_='story-info-right-extent').find('p', class_='info-bookmark')
    detail['infor_bookmark']='https://ww5.manganelo.tv/' + view2.find('img').get('src')
    #LẤY NỘI DUNG
    list_nd=[]
    nd=soup.find('div', class_='panel-story-info-description')
    for text1 in nd:
        text_nd=text1.text.replace("\r","").replace("\n","")
        list_nd.append(text_nd)
    detail['Description']= list_nd[2]
    return detail
#Lấy  link chapter
@app.route("/chapter", methods=["GET"])
def get_Chapter():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    item = {}
    data1 = soup.find('table',class_='variations-tableInfo')
    data_link = soup.find('div', class_='panel-story-chapter-list').find('ul', class_='row-content-chapter').find_all('li', class_='a-h')
    link_all = []
    for link in data_link:
        link_all.append(link.find('a').get('href'))
        reversed_link_all = list(reversed(link_all))
    def get_link_img(url_link):
        link_imgs=[] 
        request = requests.get('https://ww5.manganelo.tv/'+str(url_link))
        soup = BeautifulSoup(request.text, 'html.parser')
        data_img=soup.find('div',class_="container-chapter-reader").find_all('img' ,class_='img-loading')
        for item in data_img:
            link_imgs.append(item.get('data-src')) 
        return link_imgs
    def get_name_img(url_name):
            request = requests.get('https://ww5.manganelo.tv/'+str(url_name))
            soup = BeautifulSoup(request.text, 'html.parser')
            name_imgs = soup.find('div',class_="panel-chapter-info-top").find('h1').text
            return name_imgs
    link_all_img = []
    for link_img in range(0,len(reversed_link_all)):
        item_img={}
        a = 'page_list' + str(link_img+1)
        item_img['chapter_id']=link_img+1
        item_img['chapter_name']=get_name_img(reversed_link_all[link_img])
        item_img[a]=get_link_img(reversed_link_all[link_img])
        link_all_img.append(item_img)
    item['chapters']=link_all_img
    return item
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1983)

