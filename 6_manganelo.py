import urllib, json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import sqlite3
import re


#############################################
#                                           #
#   Thay đổi const theo đúng yêu cầu        #
#                                           #
#############################################

_LINK_SAVE_DB = "D:\Project App Manga ThinkDriff\Crawl Data\Database\MangaServer.db" # Đường dẫn đến database
_BASE_LINK = "https://ww5.manganelo.tv" # Không thay đổi dòng này
_API_KEY = "fd81b5da86e162ade162a05220c0eb89"#TK: kaidodo10 Không thay đổi dòng này
_IMGBB_UPLOAD_LINK = "https://api.imgbb.com/1/upload" # Không thay đổi dòng này
_WORK_DIR = 'D:\\Project App Manga ThinkDriff\\Crawl Data\\Data Manga Image' # Đường dẫn đến folder chứa ảnh
PAGE = 1 # Số trang muốn crawl

def processing_SoLuongView(SoLuongView):
    if SoLuongView.isnumeric() :
        return SoLuongView
    elif SoLuongView.find('K') != -1:
        SoLuongView = SoLuongView.replace("K", "")
        return int(float(SoLuongView) * 1000)
    elif SoLuongView.find('M') != -1:
        SoLuongView = SoLuongView.replace("M", "")
        return int(float(SoLuongView) * 1000000)
    elif SoLuongView.find('B') != -1:
        SoLuongView = SoLuongView.replace("B", "")
        return int(float(SoLuongView) * 1000000000)
    return 0

def insertVaribleIntoTable(ID_Manga,
       SoLuongView,
       Rate,
       DescriptManga,
       LinkImagePoster_linkgoc,
       Link_Detail_Manga,
       ListChapter,
       Tac_Gia,
       ListCategories,
       Status,
       Title_Manga,
       id_Server,
       LinkImagePoster_link_Upload):
    try:
        sqliteConnection = sqlite3.connect(_LINK_SAVE_DB)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO ListManga
                          (ID_Manga,SoLuongView, Rate, DescriptManga, LinkImagePoster_linkgoc, Link_Detail_Manga, ListChapter, Tac_Gia, ListCategories, Status, Title_Manga, id_Server, LinkImagePoster_link_Upload) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        data_tuple = (ID_Manga,
       SoLuongView,
       Rate,
       DescriptManga,
       LinkImagePoster_linkgoc,
       Link_Detail_Manga,
       ListChapter,
       Tac_Gia,
       ListCategories,
       Status,
       Title_Manga,
       id_Server,
       LinkImagePoster_link_Upload)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


for pageIndex in range(PAGE):
    linkListManga = _BASE_LINK + "/genre?page=" + str(pageIndex + 1)
    requestListManga = requests.get(linkListManga)
    soupListManga = BeautifulSoup(requestListManga.text, 'html.parser')
    for mangaIndex in soupListManga.findAll('div', class_='content-genres-item'):

        ID_Manga = _BASE_LINK + mangaIndex.find('div', {"class": "genres-item-info"}).find('h3').find('a').get("href")
        SoLuongView = processing_SoLuongView(mangaIndex.find('div', {"class": "genres-item-info"}).find('p', {"class" : "genres-item-view-time text-nowrap"}).find('span', {"class" : "genres-item-view"}).text.strip())
        Rate = mangaIndex.find('a').find('em').text
        DescriptManga = mangaIndex.find('div', {"class": "genres-item-info"}).find('div', {"class" : "genres-item-description"}).text.strip()
        LinkImagePoster_linkgoc = _BASE_LINK + mangaIndex.find('a', {"class" : "genres-item-img"}).find('img', {"class" : "img-loading"}).get('src')
        Link_Detail_Manga = _BASE_LINK + mangaIndex.find('div', {"class": "genres-item-info"}).find('h3').find('a').get("href")
        Tac_Gia = mangaIndex.find('div', {"class": "genres-item-info"}).find('p', {"class" : "genres-item-view-time text-nowrap"}).find('span', {"class" : "genres-item-author"}).text
        Title_Manga =  mangaIndex.find('div', {"class": "genres-item-info"}).find('h3').find('a').text
        id_Server = _BASE_LINK

        # Đang test link_Upload
        # -------------------------------------------
        LinkImagePoster_link_Upload = ""
        # -------------------------------------------

        LinkPostImage = _IMGBB_UPLOAD_LINK + "?key=" + _API_KEY + "&image=" + LinkImagePoster_linkgoc
        linktmp = ""
        try:
            response = Request(LinkPostImage, headers={"User-Agent": "Mozilla/5.0"})
            data = json.loads(urlopen(response).read().decode(urlopen(response).info().get_param('charset') or 'utf-8'))
        except:
            linktmp = ""
        else:
            linktmp = data["data"]["image"]["url"]
        finally:
            LinkImagePoster_link_Upload = linktmp
        
        _WORK_DIR = 'D:\\Project App Manga ThinkDriff\\Crawl Data\\Data Manga Image'
        os.chdir(_WORK_DIR)
        pathFolderManga = os.path.join(_WORK_DIR, re.sub("[\\/:*?\"<>|]","",Title_Manga))
        os.mkdir(pathFolderManga)

        requestMangaIndex = requests.get(Link_Detail_Manga)
        soupMangaIndex = BeautifulSoup(requestMangaIndex.text, 'html.parser')

        ListChapter = []
        ListLinkChapter = []
        ListCategories = []
        for chapterIndex in soupMangaIndex.findAll('li', class_='a-h'):
            ListChapter.append(chapterIndex.find('a').text)
            ListLinkChapter.append(_BASE_LINK + chapterIndex.find('a').get('href'))

        for indexI in range(len(ListChapter)):
            pathFolderChapter = os.path.join(pathFolderManga, re.sub("[\\/:*?\"<>|]","",ListChapter[indexI]))
            os.mkdir(pathFolderChapter)
            os.chdir(pathFolderChapter)
            
            requestChapterIndex = requests.get(ListLinkChapter[indexI])
            soupChapterIndex = BeautifulSoup(requestChapterIndex.text, 'html.parser')
            cnt = 1
            for Image in soupChapterIndex.findAll('img', class_='img-loading'):
                linkImage = Image.get('data-src')
                response = requests.get(linkImage)
                with open( str(cnt) + ".jpg", "wb") as f:
                    f.write(response.content)
                cnt += 1
        
        ListChapter = ', '.join(ListChapter)
        for categoryIndex in soupMangaIndex.find('div', {"class" : "story-info-right"}).find('table', {"class" : "variations-tableInfo"}).find('tbody').select('tr')[3].find('td', {"class" : "table-value"}).findAll('a', class_='a-h'):
            ListCategories.append(categoryIndex.text)
        ListCategories = ', '.join(ListCategories)
        Status = soupMangaIndex.find('div', {"class" : "story-info-right"}).find('table', {"class" : "variations-tableInfo"}).find('tbody').select('tr')[2].find('td', {"class" : "table-value"}).text.strip()
        #print(str(ListCategories) + "|")
        insertVaribleIntoTable(ID_Manga,SoLuongView, Rate, DescriptManga, LinkImagePoster_linkgoc, Link_Detail_Manga, ListChapter, Tac_Gia, ListCategories, Status, Title_Manga, id_Server, LinkImagePoster_link_Upload)
        
        
    break