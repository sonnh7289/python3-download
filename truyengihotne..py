from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/home", methods=["GET"])
def get_home():
    listJsonManga_ngontinh = []
    listJsonManga_truyen18 = []
    listJsonManga_tieuthuyet = []
    listJsonManga_truyenmoi = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/index.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')

    for itemName1 in soupManga_base.findAll('img')[:10]:
        JsonManga_ngontinh = {}
        JsonManga_ngontinh['banner'] = itemName1.get('src')
        listJsonManga_ngontinh.append(JsonManga_ngontinh)

    count = 0
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title'), soupManga_base.findAll('a', class_='cw-list-item'), soupManga_base.findAll('span', class_='chapter-link')):
        if count >= 8:
            break
        JsonManga_ngontinh = {}
        JsonManga_ngontinh['name_manga'] = itemName2.text.strip()
        JsonManga_ngontinh['url_manga'] = itemName3.get('href')
        JsonManga_ngontinh['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_ngontinh['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_ngontinh.append(JsonManga_ngontinh)
        count += 1
    count = 0
    
        
    count = 0  # đếm số lượng truyện đã tìm được
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[8:], soupManga_base.findAll('a', class_='cw-list-item')[8:], soupManga_base.findAll('span', class_='chapter-link')[8:]):
        if count >= 8:
            break
        JsonManga_truyen18 = {}
        JsonManga_truyen18['name_manga'] = itemName2.text.strip()
        JsonManga_truyen18['url_manga'] = itemName3.get('href')
        JsonManga_truyen18['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_truyen18['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_truyen18.append(JsonManga_truyen18)
        count += 1
    count = 0  

    count = 0  
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[16:], soupManga_base.findAll('a', class_='cw-list-item')[16:], soupManga_base.findAll('span', class_='chapter-link')[16:]):
        if count >= 8:  
            break
        JsonManga_tieuthuyet = {}
        JsonManga_tieuthuyet['name_manga'] = itemName2.text.strip()
        JsonManga_tieuthuyet['url_manga'] = itemName3.get('href')
        JsonManga_tieuthuyet['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_tieuthuyet['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_tieuthuyet.append(JsonManga_tieuthuyet)
        count += 1
    count = 0
    
    count = 0  
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[24:], soupManga_base.findAll('a', class_='cw-list-item')[24:], soupManga_base.findAll('span', class_='chapter-link')[24:]):
        if count >= 16:
            break
        JsonManga_truyenmoi = {}
        JsonManga_truyenmoi['name_manga'] = itemName2.text.strip()
        JsonManga_truyenmoi['url_manga'] = itemName3.get('href')
        JsonManga_truyenmoi['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_truyenmoi['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_truyenmoi.append(JsonManga_truyenmoi)
        count += 1
    count = 0
    
    son = {"ngontinh": listJsonManga_ngontinh, "truyen18": listJsonManga_truyen18, "tieuthuyet": listJsonManga_tieuthuyet, "truyenmoi": listJsonManga_truyenmoi}
    return jsonify(son)

@app.route("/ngontinh", methods=["GET"])
def get_ngontinh():
    listJsonManga_truyendexuat = []
    listJsonManga_truyenmoicapnhat = []
    listJsonManga_auco = []
    listJsonManga_hiendai = []
    listJsonManga_shoujo = []
    listJsonManga_hanhdong = []
    listJsonManga_tonghop = []
    listJsonManga_truyentranhfull = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/ngon-tinh.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    for itemName1 in soupManga_base.findAll('img')[:4]:
        JsonManga_truyendexuat = {}
        JsonManga_truyendexuat['banner'] = itemName1.get('src')
        listJsonManga_truyendexuat.append(JsonManga_truyendexuat)

    count = 0
    for itemName2 in soupManga_base.findAll('div', class_='swiper-slide')[4:]:
        if count >= 12:
            break
        JsonManga_truyendexuat = {}
        JsonManga_truyendexuat['name_manga'] = itemName2.text.strip()
        JsonManga_truyendexuat['url_manga'] = itemName2.find('a').get('href')
        JsonManga_truyendexuat['image_manga'] = itemName2.find('img').get('src')
        listJsonManga_truyendexuat.append(JsonManga_truyendexuat)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title'), soupManga_base.findAll('a', class_='cw-list-item'), soupManga_base.findAll('span', class_='chapter-link')):
        if count >= 16:
            break
        JsonManga_truyenmoicapnhat = {}
        JsonManga_truyenmoicapnhat['name_manga'] = itemName2.text.strip()
        JsonManga_truyenmoicapnhat['url_manga'] = itemName3.get('href')
        JsonManga_truyenmoicapnhat['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_truyenmoicapnhat['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_truyenmoicapnhat.append(JsonManga_truyenmoicapnhat)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[2:]:
        if count >= 1:
            break
        JsonManga_auco = {}
        JsonManga_auco['banner'] = itemName1.find('img').get('src')
        listJsonManga_auco.append(JsonManga_auco)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[16:], soupManga_base.findAll('a', class_='cw-list-item')[16:], soupManga_base.findAll('span', class_='chapter-link')[15:]):
        if count >= 16:
            break
        JsonManga_auco = {}
        JsonManga_auco['name_manga'] = itemName2.text.strip()
        JsonManga_auco['url_manga'] = itemName3.get('href')
        JsonManga_auco['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_auco['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_auco.append(JsonManga_auco)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[3:]:
        if count >= 1:
            break
        JsonManga_hiendai = {}
        JsonManga_hiendai['banner'] = itemName1.find('img').get('src')
        listJsonManga_hiendai.append(JsonManga_hiendai)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[32:], soupManga_base.findAll('a', class_='cw-list-item')[32:], soupManga_base.findAll('span', class_='chapter-link')[31:]):
        if count >= 16:
            break
        JsonManga_hiendai = {}
        JsonManga_hiendai['name_manga'] = itemName2.text.strip()
        JsonManga_hiendai['url_manga'] = itemName3.get('href')
        JsonManga_hiendai['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_hiendai['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_hiendai.append(JsonManga_hiendai)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[4:]:
        if count >= 1:
            break
        JsonManga_shoujo = {}
        JsonManga_shoujo['banner'] = itemName1.find('img').get('src')
        listJsonManga_shoujo.append(JsonManga_shoujo)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[48:], soupManga_base.findAll('a', class_='cw-list-item')[48:], soupManga_base.findAll('span', class_='chapter-link')[46:]):
        if count >= 16:
            break
        JsonManga_shoujo = {}
        JsonManga_shoujo['name_manga'] = itemName2.text.strip()
        JsonManga_shoujo['url_manga'] = itemName3.get('href')
        JsonManga_shoujo['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_shoujo['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_shoujo.append(JsonManga_shoujo)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[5:]:
        if count >= 1:
            break
        JsonManga_hanhdong = {}
        JsonManga_hanhdong['banner'] = itemName1.find('img').get('src')
        listJsonManga_hanhdong.append(JsonManga_hanhdong)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[64:], soupManga_base.findAll('a', class_='cw-list-item')[64:], soupManga_base.findAll('span', class_='chapter-link')[62:]):
        if count >= 10:
            break
        JsonManga_hanhdong = {}
        JsonManga_hanhdong['name_manga'] = itemName2.text.strip()
        JsonManga_hanhdong['url_manga'] = itemName3.get('href')
        JsonManga_hanhdong['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_hanhdong['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_hanhdong.append(JsonManga_hanhdong)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[6:]:
        if count >= 1:
            break
        JsonManga_tonghop = {}
        JsonManga_tonghop['banner'] = itemName1.find('img').get('src')
        listJsonManga_tonghop.append(JsonManga_tonghop)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[74:], soupManga_base.findAll('a', class_='cw-list-item')[74:], soupManga_base.findAll('span', class_='chapter-link')[71:]):
        if count >= 16:
            break
        JsonManga_tonghop = {}
        JsonManga_tonghop['name_manga'] = itemName2.text.strip()
        JsonManga_tonghop['url_manga'] = itemName3.get('href')
        JsonManga_tonghop['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_tonghop['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_tonghop.append(JsonManga_tonghop)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[7:]:
        if count >= 1:
            break
        JsonManga_truyentranhfull = {}
        JsonManga_truyentranhfull['banner'] = itemName1.find('img').get('src')
        listJsonManga_truyentranhfull.append(JsonManga_truyentranhfull)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[90:], soupManga_base.findAll('a', class_='cw-list-item')[90:], soupManga_base.findAll('span', class_='chapter-link')[87:]):
        if count >= 16:
            break
        JsonManga_truyentranhfull = {}
        JsonManga_truyentranhfull['name_manga'] = itemName2.text.strip()
        JsonManga_truyentranhfull['url_manga'] = itemName3.get('href')
        JsonManga_truyentranhfull['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_truyentranhfull['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_truyentranhfull.append(JsonManga_truyentranhfull)
        count += 1
    count = 0
    
    son = {"truyendexuat": listJsonManga_truyendexuat, "truyenmoicapnhat": listJsonManga_truyenmoicapnhat, "auco": listJsonManga_auco, "hiendai": listJsonManga_hiendai, "shoujo": listJsonManga_shoujo, "hanhdong": listJsonManga_hanhdong, "tonghop": listJsonManga_tonghop, "truyentranhfull": listJsonManga_truyentranhfull}
    return jsonify(son)

@app.route("/truyen18", methods=["GET"])
def get_truyen18():
    listJsonManga_truyendexuat = []
    listJsonManga_truyenmoicapnhat = []
    listJsonManga_hentai = []
    listJsonManga_smut = []
    listJsonManga_dlsite = []
    listJsonManga_bl = []
    listJsonManga_gl = []
    listJsonManga_truyentranhfull = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/truyen-tranh.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName2 in soupManga_base.findAll('div', class_='swiper-slide')[4:]:
        if count >= 12:
            break
        JsonManga_truyendexuat = {}
        JsonManga_truyendexuat['name_manga'] = itemName2.text.strip()
        JsonManga_truyendexuat['url_manga'] = itemName2.find('a').get('href')
        JsonManga_truyendexuat['image_manga'] = itemName2.find('img').get('src')
        listJsonManga_truyendexuat.append(JsonManga_truyendexuat)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title'), soupManga_base.findAll('a', class_='cw-list-item'), soupManga_base.findAll('span', class_='chapter-link')):
        if count >= 16:
            break
        JsonManga_truyenmoicapnhat = {}
        JsonManga_truyenmoicapnhat['name_manga'] = itemName2.text.strip()
        JsonManga_truyenmoicapnhat['url_manga'] = itemName3.get('href')
        JsonManga_truyenmoicapnhat['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_truyenmoicapnhat['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_truyenmoicapnhat.append(JsonManga_truyenmoicapnhat)
        count += 1
    count = 0
    
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[2:]:
        if count >= 1:
            break
        JsonManga_hentai = {}
        JsonManga_hentai['banner'] = itemName1.find('img').get('src')
        listJsonManga_hentai.append(JsonManga_hentai)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[16:], soupManga_base.findAll('a', class_='cw-list-item')[16:], soupManga_base.findAll('span', class_='chapter-link')[13:]):
        if count >= 16:
            break
        JsonManga_hentai = {}
        JsonManga_hentai['name_manga'] = itemName2.text.strip()
        JsonManga_hentai['url_manga'] = itemName3.get('href')
        JsonManga_hentai['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_hentai['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_hentai.append(JsonManga_hentai)
        count += 1
    count = 0
    
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[3:]:
        if count >= 1:
            break
        JsonManga_smut = {}
        JsonManga_smut['banner'] = itemName1.find('img').get('src')
        listJsonManga_smut.append(JsonManga_smut)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[32:], soupManga_base.findAll('a', class_='cw-list-item')[32:], soupManga_base.findAll('span', class_='chapter-link')[28:]):
        if count >= 16:
            break
        JsonManga_smut = {}
        JsonManga_smut['name_manga'] = itemName2.text.strip()
        JsonManga_smut['url_manga'] = itemName3.get('href')
        JsonManga_smut['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_smut['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_smut.append(JsonManga_smut)
        count += 1
    count = 0
    
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[4:]:
        if count >= 1:
            break
        JsonManga_dlsite = {}
        JsonManga_dlsite['banner'] = itemName1.find('img').get('src')
        listJsonManga_dlsite.append(JsonManga_dlsite)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[48:], soupManga_base.findAll('a', class_='cw-list-item')[48:], soupManga_base.findAll('span', class_='chapter-link')[42:]):
        if count >= 16:
            break
        JsonManga_dlsite = {}
        JsonManga_dlsite['name_manga'] = itemName2.text.strip()
        JsonManga_dlsite['url_manga'] = itemName3.get('href')
        JsonManga_dlsite['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_dlsite['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_dlsite.append(JsonManga_dlsite)
        count += 1
    count = 0
    
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[5:]:
        if count >= 1:
            break
        JsonManga_bl = {}
        JsonManga_bl['banner'] = itemName1.find('img').get('src')
        listJsonManga_bl.append(JsonManga_bl)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[64:], soupManga_base.findAll('a', class_='cw-list-item')[64:], soupManga_base.findAll('span', class_='chapter-link')[57:]):
        if count >= 16:
            break
        JsonManga_bl = {}
        JsonManga_bl['name_manga'] = itemName2.text.strip()
        JsonManga_bl['url_manga'] = itemName3.get('href')
        JsonManga_bl['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_bl['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_bl.append(JsonManga_bl)
        count += 1
    count = 0
    
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[6:]:
        if count >= 1:
            break
        JsonManga_gl = {}
        JsonManga_gl['banner'] = itemName1.find('img').get('src')
        listJsonManga_gl.append(JsonManga_gl)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[80:], soupManga_base.findAll('a', class_='cw-list-item')[80:], soupManga_base.findAll('span', class_='chapter-link')[73:]):
        if count >= 16:
            break
        JsonManga_gl = {}
        JsonManga_gl['name_manga'] = itemName2.text.strip()
        JsonManga_gl['url_manga'] = itemName3.get('href')
        JsonManga_gl['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_gl['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_gl.append(JsonManga_gl)
        count += 1
    count = 0
    
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[7:]:
        if count >= 1:
            break
        JsonManga_truyentranhfull = {}
        JsonManga_truyentranhfull['banner'] = itemName1.find('img').get('src')
        listJsonManga_truyentranhfull.append(JsonManga_truyentranhfull)
        count += 1
    count = 0

    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[96:], soupManga_base.findAll('a', class_='cw-list-item')[96:], soupManga_base.findAll('span', class_='chapter-link')[89:]):
        if count >= 16:
            break
        JsonManga_truyentranhfull = {}
        JsonManga_truyentranhfull['name_manga'] = itemName2.text.strip()
        JsonManga_truyentranhfull['url_manga'] = itemName3.get('href')
        JsonManga_truyentranhfull['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_truyentranhfull['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_truyentranhfull.append(JsonManga_truyentranhfull)
        count += 1
    count = 0
    
    son = {"truyendexuat": listJsonManga_truyendexuat, "truyenmoicapnhat": listJsonManga_truyenmoicapnhat, "hentai": listJsonManga_hentai, "smut": listJsonManga_smut, "dlsite": listJsonManga_dlsite, "bl": listJsonManga_bl, "gl": listJsonManga_gl, "truyentranhfull": listJsonManga_truyentranhfull}
    return jsonify(son)

@app.route("/tieuthuyet", methods=["GET"])
def get_tieuthuyet():
    listJsonManga_truyendexuat = []
    listJsonManga_tieuthuyetmoicapnhat = []
    listJsonManga_tusangtac = []
    listJsonManga_codai = []
    listJsonManga_hiendai = []
    listJsonManga_tieuthuyetfull = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/tieu-thuyet.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    for itemName1 in soupManga_base.findAll('img')[:4]:
        JsonManga_truyendexuat = {}
        JsonManga_truyendexuat['banner'] = itemName1.get('src')
        listJsonManga_truyendexuat.append(JsonManga_truyendexuat)

    count = 0
    for itemName2 in soupManga_base.findAll('div', class_='swiper-slide')[4:]:
        if count >= 12:
            break
        JsonManga_truyendexuat = {}
        JsonManga_truyendexuat['name_manga'] = itemName2.text.strip()
        JsonManga_truyendexuat['url_manga'] = itemName2.find('a').get('href')
        JsonManga_truyendexuat['image_manga'] = itemName2.find('img').get('src')
        listJsonManga_truyendexuat.append(JsonManga_truyendexuat)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title'), soupManga_base.findAll('a', class_='cw-list-item'), soupManga_base.findAll('span', class_='chapter-link')):
        if count >= 16:
            break
        JsonManga_tieuthuyetmoicapnhat = {}
        JsonManga_tieuthuyetmoicapnhat['name_manga'] = itemName2.text.strip()
        JsonManga_tieuthuyetmoicapnhat['url_manga'] = itemName3.get('href')
        JsonManga_tieuthuyetmoicapnhat['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_tieuthuyetmoicapnhat['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_tieuthuyetmoicapnhat.append(JsonManga_tieuthuyetmoicapnhat)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[16:], soupManga_base.findAll('a', class_='cw-list-item')[16:], soupManga_base.findAll('span', class_='chapter-link')[16:]):
        if count >= 16:
            break
        JsonManga_tusangtac = {}
        JsonManga_tusangtac['name_manga'] = itemName2.text.strip()
        JsonManga_tusangtac['url_manga'] = itemName3.get('href')
        JsonManga_tusangtac['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_tusangtac['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_tusangtac.append(JsonManga_tusangtac)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[32:], soupManga_base.findAll('a', class_='cw-list-item')[32:], soupManga_base.findAll('span', class_='chapter-link')[32:]):
        if count >= 16:
            break
        JsonManga_codai = {}
        JsonManga_codai['name_manga'] = itemName2.text.strip()
        JsonManga_codai['url_manga'] = itemName3.get('href')
        JsonManga_codai['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_codai['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_codai.append(JsonManga_codai)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[48:], soupManga_base.findAll('a', class_='cw-list-item')[48:], soupManga_base.findAll('span', class_='chapter-link')[48:]):
        if count >= 16:
            break
        JsonManga_hiendai = {}
        JsonManga_hiendai['name_manga'] = itemName2.text.strip()
        JsonManga_hiendai['url_manga'] = itemName3.get('href')
        JsonManga_hiendai['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_hiendai['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_hiendai.append(JsonManga_hiendai)
        count += 1
    count = 0
    
    for itemName2, itemName3, itemName4 in zip(soupManga_base.findAll('span', class_='title')[70:], soupManga_base.findAll('a', class_='cw-list-item')[70:], soupManga_base.findAll('span', class_='chapter-link')[70:]):
        JsonManga_tieuthuyetfull = {}
        JsonManga_tieuthuyetfull['name_manga'] = itemName2.text.strip()
        JsonManga_tieuthuyetfull['url_manga'] = itemName3.get('href')
        JsonManga_tieuthuyetfull['img_manga'] = itemName3.find('span', class_='thumb').get('style')
        JsonManga_tieuthuyetfull['chapter_manga'] = itemName4.a.get('href')
        listJsonManga_tieuthuyetfull.append(JsonManga_tieuthuyetfull)
        
    son = {"truyendexuat": listJsonManga_truyendexuat, "tieuthuyetmoicapnhat": listJsonManga_tieuthuyetmoicapnhat, "tusangtac": listJsonManga_tusangtac, "codai": listJsonManga_codai, "hiendai": listJsonManga_hiendai, "tieuthuyetfull": listJsonManga_tieuthuyetfull}
    return jsonify(son)

@app.route("/anime", methods=["GET"])
def get_anime():
    listJsonManga_animemoicapnhat = []
    listJsonManga_phimbo = []
    listJsonManga_phimchieurap = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/anime.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='tray-item'):
        if count >= 12:
            break
        JsonManga_animemoicapnhat = {}
        JsonManga_animemoicapnhat['name_anime'] = itemName1.text.strip()
        JsonManga_animemoicapnhat['img_anime'] = itemName1.find('img').get('src')
        JsonManga_animemoicapnhat['url_anime'] = itemName1.find('a').get('href')
        listJsonManga_animemoicapnhat.append(JsonManga_animemoicapnhat)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='tray-item')[12:]:
        if count >= 8:
            break
        JsonManga_phimbo = {}
        JsonManga_phimbo['name_anime'] = itemName1.text.strip()
        JsonManga_phimbo['img_anime'] = itemName1.find('img').get('src')
        JsonManga_phimbo['url_anime'] = itemName1.find('a').get('href')
        listJsonManga_phimbo.append(JsonManga_phimbo)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='tray-item')[20:]:
        if count >= 8:
            break
        JsonManga_phimchieurap = {}
        JsonManga_phimchieurap['name_anime'] = itemName1.text.strip()
        JsonManga_phimchieurap['img_anime'] = itemName1.find('img').get('src')
        JsonManga_phimchieurap['url_anime'] = itemName1.find('a').get('href')
        listJsonManga_phimchieurap.append(JsonManga_phimchieurap)
        count += 1
    count = 0
    
    son = {"animemoicapnhat": listJsonManga_animemoicapnhat, "phimbo": listJsonManga_phimbo, "phimchieurap": listJsonManga_phimchieurap}
    return jsonify(son)

@app.route("/news", methods=["GET"])
def get_news():
    listJsonManga_khuvucreviewtruyen = []
    listJsonManga_khuvucspoiltruyen = []
    session = requests.Session()
    rManga_base = session.get('https://truyengihotne.com/tin-tuc.html')
    soupManga_base = BeautifulSoup(rManga_base._content, 'html.parser')
    count = 0
    for itemName1 in soupManga_base.findAll('div', class_='widget-main'):
        if count >= 1:
            break
        JsonManga_khuvucreviewtruyen = {}
        JsonManga_khuvucreviewtruyen['banner'] = itemName1.find('img').get('src')
        listJsonManga_khuvucreviewtruyen.append(JsonManga_khuvucreviewtruyen)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='tray-item'):
        if count >= 8:
            break
        JsonManga_khuvucreviewtruyen = {}
        JsonManga_khuvucreviewtruyen['name_anime'] = itemName1.text.strip()
        JsonManga_khuvucreviewtruyen['img_anime'] = itemName1.find('img').get('src')
        JsonManga_khuvucreviewtruyen['url_anime'] = itemName1.find('a').get('href')
        listJsonManga_khuvucreviewtruyen.append(JsonManga_khuvucreviewtruyen)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='widget-main')[1:]:
        if count >= 1:
            break
        JsonManga_khuvucspoiltruyen = {}
        JsonManga_khuvucspoiltruyen['banner'] = itemName1.find('img').get('src')
        listJsonManga_khuvucspoiltruyen.append(JsonManga_khuvucspoiltruyen)
        count += 1
    count = 0
    
    for itemName1 in soupManga_base.findAll('div', class_='tray-item')[8:]:
        if count >= 8:
            break
        JsonManga_khuvucspoiltruyen = {}
        JsonManga_khuvucspoiltruyen['name_anime'] = itemName1.text.strip()
        JsonManga_khuvucspoiltruyen['img_anime'] = itemName1.find('img').get('src')
        JsonManga_khuvucspoiltruyen['url_anime'] = itemName1.find('a').get('href')
        listJsonManga_khuvucspoiltruyen.append(JsonManga_khuvucspoiltruyen)
        count += 1
    count = 0
    
    son = {"khuvucreviewtruyen": listJsonManga_khuvucreviewtruyen, "khuvucspoiltruyen": listJsonManga_khuvucspoiltruyen}
    return jsonify(son)

@app.route("/timkiem", methods=["GET"])
def get_timkiem():
    link_full = request.headers.get('Link-Full')
    listJsonManga_danhsachtruyentranh = []
    session = requests.Session()
    rManga_base = session.get(link_full)
    #rManga_base = session.get('https://truyengihotne.com/tim-kiem-nang-cao.html?text_add=')
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    for itemName1, itemName2, itemName3 in zip(soupManga_base.findAll('span', class_='title'), soupManga_base.findAll('a', class_='cw-list-item'), soupManga_base.findAll('span', class_='chapter-link')):
        JsonManga_danhsachtruyentranhn = {}
        JsonManga_danhsachtruyentranhn['name_anime'] = itemName1.text.strip()
        JsonManga_danhsachtruyentranhn['url_manga'] = itemName2.get('href')
        JsonManga_danhsachtruyentranhn['img_manga'] = itemName2.find('span', class_='thumb').get('style')
        JsonManga_danhsachtruyentranhn['chapter_manga'] = itemName3.a.get('href') 
        listJsonManga_danhsachtruyentranh.append(JsonManga_danhsachtruyentranhn)
    
    son = {"danhsachtruyentranh": listJsonManga_danhsachtruyentranh}
    return jsonify(son)

@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    maa =[]
    link_full = request.headers.get('Link-Full')
    #print(link_full)
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    
    for div in soupManga_base.findAll('div', class_='cover-wrapper'):
        FullDetailManga = {}
        # print(div)    
        FullDetailManga['img_manga'] = div.img('src')
        FullDetailManga['url_manga'] = div.a('href')
        FullDetailManga['title_manga'] = div.text
        

    maa.append(FullDetailManga)

    return FullDetailManga

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=1234)
