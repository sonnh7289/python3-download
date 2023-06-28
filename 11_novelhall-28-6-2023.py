import urllib, json
import datetime
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

_LINK_SAVE_DB = "G:\Project App Manga ThinkDrff\son.db" # Đường dẫn đến database
_BASE_LINK = "https://www.novelhall.com" # Không thay đổi dòng này (Trang chủ manga)
_API_KEY = "938c8d9c19d7ec0c6f5225d69a3ef3ae"#TK: kaidodo002 Không thay đổi dòng này
_IMGBB_UPLOAD_LINK = "https://api.imgbb.com/1/upload" # Không thay đổi dòng này
_WORK_DIR = 'G:\\Project App Manga ThinkDrff\\Truyen chu\\novelhall.com' # Đường dẫn đến folder Manga Truyện chữ
_DEFAULT_RATE = 3
START_PAGE = 6
END_PAGE = 210

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

def insertChapterIntoTable(id_chapter, id_manga, content_chapter, thoi_gian_release, id_server):
    try:
        sqliteConnection = sqlite3.connect(_LINK_SAVE_DB)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO ListChapterTruyenChu
                          (id_chapter, id_manga, content_chapter, thoi_gian_release, id_server) 
                          VALUES (?, ?, ?, ?, ?);"""
        
        data_tuple = (id_chapter, id_manga, content_chapter, thoi_gian_release, id_server)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Chapter inserted successfully into SqliteDb_developers table: " + id_chapter)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
def uploadImagetoImgbb(LinkImagePoster_linkgoc):
    LinkPostImage = _IMGBB_UPLOAD_LINK + "?key=" + _API_KEY + "&image=" + LinkImagePoster_linkgoc
    linktmp = ""
    try:
        response = Request(LinkPostImage, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urlopen(response).read().decode(urlopen(response).info().get_param('charset') or 'utf-8'))
    except:
        linktmp = ""
    else:
        linktmp = data["data"]["image"]["url"]
    return linktmp

def insertMangaIntoTable(ID_Manga,
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
        print("Manga inserted successfully into SqliteDb_developers table: " + ID_Manga)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


for pageIndex in range(START_PAGE,END_PAGE,1):
    linkListManga = _BASE_LINK + "/all2022-" + str(pageIndex) + ".html"
    while True:
        try:
            requestListManga = requests.get(linkListManga, headers={"User-Agent": "Mozilla/5.0"})
            soupListManga = BeautifulSoup(requestListManga.text, 'html.parser')
        except:
            print("Trying to connect to Page : " + linkListManga)
            continue
        else:
            break

    mangaPoint = open(_WORK_DIR + "\\page" + str(pageIndex) + ".txt", 'a')
    for mangaIndex in soupListManga.findAll('li', class_="btm"):
        try:
            ID_Manga = _BASE_LINK + '/' + mangaIndex.find('a').get('href')
        except:
            continue
        Link_Detail_Manga = ID_Manga
        id_Server = _BASE_LINK
        Rate = _DEFAULT_RATE
        SoLuongView = 0

        # Vào manga
        while True:
            try:
                requestMangaIndex = requests.get(Link_Detail_Manga, headers={"User-Agent": "Mozilla/5.0"})
                soupMangaIndex = BeautifulSoup(requestMangaIndex.text, 'html.parser')
            except:
                print("Trying to connect to Manga : " + Link_Detail_Manga)
                continue
            else:
                break
        
        try:
            Title_Manga = soupMangaIndex.find('div', {"class":"book-info"}).find('h1').text.replace("\n","").replace("\t","").strip('. ')
        except:
            continue
        mode = 0o777
        if os.path.exists(_WORK_DIR) == False:
            os.mkdir(_WORK_DIR, mode)
        os.chdir(_WORK_DIR)
        # Cập nhật manga đang crawl
        mangaPoint = open(_WORK_DIR + "\\page" + str(pageIndex) + ".txt", 'r')
        data = mangaPoint.read()
        data = data.split(',')
        if len(data) != 0:
            if ID_Manga in data:
                continue
        mangaPoint = open(_WORK_DIR + "\\page" + str(pageIndex) + ".txt", 'a')
        mangaPoint.write(ID_Manga + ',')
        mangaPoint = open(_WORK_DIR + "\\page" + str(pageIndex) + ".txt", 'r')
        # Tạo folder manga
        mode = 0o777
        pathFolderManga = os.path.join(_WORK_DIR, re.sub("[\\/:*?\"<>|]","",Title_Manga))
        if os.path.exists(pathFolderManga) == False:
            os.mkdir(pathFolderManga, mode)
        
        try:
            LinkImagePoster_linkgoc = soupMangaIndex.find('div', {"class":"book-img hidden-xs"}).find('img').get('src')
        except:
            LinkImagePoster_linkgoc = ''
        LinkImagePoster_link_Upload = ''
        # LinkImagePoster_link_Upload = uploadImagetoImgbb(LinkImagePoster_linkgoc)
        try:
            ListCategories = soupMangaIndex.find('div', {"class":"total booktag"}).find('a').text
        except:
            ListCategories = ''

        try:
            ListSpan = soupMangaIndex.find('div', {"class":"total booktag"}).select('span')
            try:
                Tac_Gia = ListSpan[0].text.replace('Author', '').strip('：').strip('0')
            except:
                Tac_Gia = ''
            try:
                Status = ListSpan[2].text.replace('Status', '').strip('：')
            except:
                Status = ''
        except:
            Tac_Gia = ''
            Status = ''

        try:
            DescriptManga = soupMangaIndex.find('span', {"class":"js-close-wrap"}).text.strip()
        except:
            DescriptManga = ''
        
        ListChapter = []
        ListLinkChapter = []
        thoi_gian_release = []
        notErorrChapter = True
        try:
            for chapterIndex in soupMangaIndex.find('div', {"id":"morelist"}).findAll('li', class_="post-11 post type-post status-publish format-standard hentry tag-wurulanghuai"):
                try:
                    ListChapter.append(chapterIndex.find('a').text.replace('\n','').strip('. '))
                    ListLinkChapter.append(_BASE_LINK + chapterIndex.find('a').get('href'))
                except:
                    notErorrChapter = False
                    break
                thoi_gian_release.append(str(datetime.datetime.now().date()))
        except:
            notErorrChapter = False

        if notErorrChapter:
            for indexI in range(len(ListChapter)):
                # Tạo folder Chapter

                nameFileChapter = re.sub("[\\/:*?\"<>|]","",ListChapter[indexI])
                pathContentChapter = os.path.join(pathFolderManga, nameFileChapter + ".txt")
                pathContentChapter = pathContentChapter[:245]

                chapterPoint = open(pathFolderManga + '\\chapterPoint.txt', 'a')
                chapterPoint = open(pathFolderManga+ '\\chapterPoint.txt', 'r')
                dowChapScList = chapterPoint.read()
                dowChapScList = dowChapScList.split(',')
                
                if len(dowChapScList) != 0:
                    if ListLinkChapter[indexI] in dowChapScList:
                        continue
                while True:
                    try:
                        requestChapterIndex = requests.get(ListLinkChapter[indexI], headers={"User-Agent": "Mozilla/5.0"})
                        soupChapterIndex = BeautifulSoup(requestChapterIndex.text, 'html.parser')
                    except:
                        print("Trying to connect to Chapter : " + ListLinkChapter[indexI])
                        continue
                    else:
                        break
                Content = []
                print('ID_Manga: ' + ID_Manga)
                print('ID_Chapter: ' + ListLinkChapter[indexI])
                fileContent = open (pathContentChapter , 'w', encoding='utf-8')

                try:
                    index = str(soupChapterIndex.find('div', {"class" : "entry-content"}))
                    index = index.replace('<div class="entry-content" id="htmlContent">', '').replace('</div>', '').strip().replace('<br/><br/>', '\n').replace('<br/>', '\n')
                    try:
                        fileContent.write(index)
                    except:
                        fileContent.write("")
                except:
                    fileContent.write("")
                content = ""
                os.chdir(pathFolderManga)
                try: 
                    fileContent = open(nameFileChapter + ".txt", 'r', encoding='utf-8')
                except:
                    content = ""
                else:
                    content = fileContent.read()
                finally:
                    content_chapter = content
                insertChapterIntoTable(ListLinkChapter[indexI], ID_Manga, content_chapter, thoi_gian_release[indexI], id_Server)
                chapterPoint = open(pathFolderManga + '\\chapterPoint.txt', 'a', encoding='utf-8')
                chapterPoint.write(ListLinkChapter[indexI] + ',')
                chapterPoint = open(pathFolderManga+ '\\chapterPoint.txt', 'r')

            ListChapter = ','.join(ListChapter)
        else:
            chapterPoint = open(pathFolderManga + '\\ChapterERROR.txt', 'a')
            chapterPoint.write('Chapter ERORR')
        insertMangaIntoTable(ID_Manga,SoLuongView, Rate, DescriptManga, LinkImagePoster_linkgoc, Link_Detail_Manga, ListChapter, Tac_Gia, ListCategories, Status, Title_Manga, id_Server, LinkImagePoster_link_Upload)
        