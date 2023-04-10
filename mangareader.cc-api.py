from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

for ii in range(1,3):
    url = 'https://mangareader.cc/latest-manga?page='+str(ii)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html')
    link_all_anime = soup.find_all('div',class_='thumb')

    lis_all_anime=[]
    for i in link_all_anime:
        #print(i.find('a').get('href'))
        lis_all_anime.append(i.find('a').get('href'))
    s=0
    name_one =''
    for i_link in lis_all_anime:
        s=s+1
        request = requests.get(i_link)
        soup = BeautifulSoup(request.text, 'html')

        list_item=[]
        item1={}
        item1['manga_id']=s

        df = soup.find_all('h1',itemprop="name")
        for i in df:
            item1['manga_name'] = str(i.text).replace("?","")
            name_one = str(i.text).replace("?","")
            #list_item.append(item1)

        for trailer_wrap in soup.find_all('div',class_='imgdesc'):
            item1['thumbnail'] = trailer_wrap.find('img').get('src')
            item1['author']='N/a'
            #list_item.append(item1)

        data1 = soup.find('div',class_='listinfo')

        des = soup.find_all('div',id='noidungm')
        for i in des:
            item1['descriptions'] = i.text.replace("\r","").replace("\n","").replace(" ","")
            #list_item.append(item1)

        def ac ():
            name_imgs = data1.find_all('li')
            lis = []
            for i in name_imgs[5]:
                text_a = i.text.replace("\r","").replace("\n","").replace(" ","").replace(",","").replace(":","")
                lis.append(str(text_a)) 
            del lis[1::2]
            return lis[1:]

        for li in data1.find_all("li"):
            item1['categories'] = str(ac()).replace("[","").replace("]","").replace("'","")
            #list_item.append(item1)

        item1['last_update'] = "1676279680"

        # lấy giá trị link và các link con
        link_all = []
        data_link = soup.find('div', class_='rm').find('div', class_='cl').find_all('li')
        for link in data_link:
            link_all.append(link.find('a').get('href'))

        # đảo chiều link. 
        reversed_link_all = list(reversed(link_all))
        reversed_link_all = reversed_link_all[:2] # nếu bỏ dòng này sẽ lấy tất cả chapter. Thay [:2]  thành một số khác để lấy nhiều chapter hơn ví dụ: [:5] là lấy 5 chapter

        #get link img con
        #def get_link_img(url_link):
        #    link_imgs=[] 
        #    request = requests.get(url_link)
        #    soup = BeautifulSoup(request.text, 'html')
        #    data_img = soup.find('div',id="readerarea").find('p').text
        #    data_img = data_img.split(",")
        #    link_imgs.append(data_img)
        #    return link_imgs
        
        def get_link_img(url_name):
            link_imgs=[] 
            request = requests.get(url_name)
            soup = BeautifulSoup(request.text, 'html')
            try:
                data_img = soup.find('div',id="readerarea").find('p').text
                data_img = data_img.split(",")
                link_imgs.append(data_img)
                return link_imgs
            except AttributeError:
                link_img = soup.find('div',class_="reading-content").find('p').text
                data_img = link_img.split(",")
                link_imgs.append(data_img)
                return link_imgs

        #get name img con
        #def get_name_img(url_name):
        #    request = requests.get(url_name)
        #    soup = BeautifulSoup(request.text, 'html')
        #    name_imgs = soup.find('div',class_="title_chap container").find('h1',class_='chapter-title').text
        #    return name_imgs
        def get_name_img(url_name):
            request = requests.get(url_name)
            soup = BeautifulSoup(request.text, 'html')
            try:
                name_imgs = soup.find('div',class_="title_chap container").find('h1',class_='chapter-title').text
                return name_imgs
            except AttributeError:
                name_imgs1 = soup.find('div',class_="main-col col-md-12 col-sm-12 sidebar-hidden").find('h1').text
                return name_imgs1
    
        link_all_img = []
        for link_img in range(0,len(reversed_link_all)):
            item_img={}
            #print(reversed_link_all[link_img])
            a = 'chapter_link' +str(link_img+1)
            item_img['chapter_id']=link_img+1
            item_img['chapter_name']=get_name_img(reversed_link_all[link_img])
            item_img[a]=get_link_img(reversed_link_all[link_img])
            link_all_img.append(item_img)

        item1['chapter']=str(link_all_img)
        item1['created_at']='1676279680'
        item1['updated_at']='1676279680'
        item1['deleted_at']='0'
        list_item.append(item1)
        name_one_anime ='C:/Users/ADMIN/OneDrive/Desktop/tozi/done/data/page'+str(ii)+ str(name_one)+str(s)+'.json'
        name = 'page'+str(ii)+ str(name_one)+str(s)+'.json'

        with open(name_one_anime, 'w', encoding='utf-8') as f:
            json.dump(list_item, f, ensure_ascii=False, indent=4)
      