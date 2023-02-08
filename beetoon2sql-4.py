from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mira@123",
    database="hub_manga"
)
mycursor = mydb.cursor()

beetoon_crawl = list()

'''
genre : Chủ đề
start : Trang bắt đầu crawl
end   : Trang kết thúc crawl
'''
def crawl_beetoon_data(genre, start, end):
    cnt = start
    base = 'https://ww5.beetoon.net/'
    url = base + genre
    idmanga = 10000
    # XỬ LÝ TỪNG TRANG TRONG MỤC ĐÃ CHỌN (LASTEST-UPDATE)
    while (cnt <= end):
        # LẤY SOURCE CODE CỦA TRANG
        pageUrl = url + '/page-' + str(cnt)
        r = requests.get(pageUrl)
        soup = BeautifulSoup(r.content, 'html.parser')

        # TẤT CẢ CÁC BỘ MANGA TRONG PAGE
        comics = soup.find('div', class_="comics-grid")

        # CRAWL DATA TỪNG Chapter TRUYỆN --> 
        # manga_id = int, manga_name = str , thumbnail = jpg, author = str,
        # categories = list, last-update = str, chapters = dict
        for link in comics.findAll('div', class_="entry"):

            linkManga_base = link.a['href']
            rManga_base = requests.get(linkManga_base)
            soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
            table_name = 'manga'
            manga_id = None
            manga_name = None
            author = None
            categories = None
            datetime = "Ongoing"
            chapter_list = []
            chapterid = 1
            chapters = list()
            data_crawl = dict()

            # MANGA NAME
            manga_name = soupManga_base.find('h1', class_='name bigger').text

            # THUMBNAIL MANGA
            thumbnail = soupManga_base.find('div', 'thumb text-center').img['src']

            # AUTHORS MANGA
            author = ""
            authors = soupManga_base.find('div', 'author')
            for a in authors.find_all('a', title=True):
                name_author = a['title'] + ", "
                author += name_author
            author = author[:-2]

            # MANGA DESCRIPTION
            desc = soupManga_base.find('div', {"id": "desc"}).text

            # CATEGORIES
            categories = []
            cats = soupManga_base.find('div', class_="genre")
            for category in cats.find_all('a', href=True):
                categories.append(category.text)
            
            try:
                # LAST UPDATE
                datetime = soupManga_base.find('div', class_='chapter-date')['title']
                
                # MANGA ID
                yyyy = datetime[6:10]
                mm = datetime[:2]
                dd = datetime[3:5]
                time = "".join(datetime[11:].split(':'))
                manga_id = yyyy + mm + dd + time

                datetime = datetime.split(" ")[0]
            except Exception as e:
                print(e)
            
            print("Manga_ID:", idmanga)
            print("\nManga_NAME:", manga_name)
            print("\nThumbail URL:", thumbnail)
            print("\nAuthor:", author)
            print("\nCategory:",categories)
            print("\nTime:", datetime)
            print("\nManga URL:", linkManga_base)
            idmanga = idmanga + 1
            # DUYỆT TỪNG PAGE TRUYỆN TRONG 1 MANGA
            last_page = 1
            cnt_page = 1
            for pageManga in soupManga_base.findAll('a', class_ = 'next page-numbers')[1:2]:
                last_page = int(pageManga.get('href').split("/")[4].split("-")[1])
                # print("\npageManga:",pageManga.get('href').split("/"))
            print("\nLast_page:", last_page)

            # LẤY URL TỪNG CHAPTER
            while last_page>=cnt:
                # LẤY LINK MANGA
                linkManga = linkManga_base + '/page-' + str(last_page)
                print("Page{}".format(last_page), linkManga)

                # LẤY DATA TỪ MANGA
                rManga = requests.get(linkManga)
                soupManga = BeautifulSoup(rManga.content, 'html.parser')

                # LẤY TÊN CÁC CHAPTER TRONG PAGE
                for chaptername in soupManga.findAll('h2', class_="chap")[::-1]:
                    chaptername = chaptername.text.replace("  ", "-").lower()
                    chapter_list.append((chaptername[:-1].replace(".","-"), chapterid))
                    
                    chapterid += 1
                last_page -= 1
            
            # print("\nChapter list:", chapter_list)
            if len(chapter_list) > 0:
                for i in range(len(chapter_list)):
                    # chapter_id, chapter_name, page_list
                    chapter_id = chapter_list[i][1]
                    chaptername = None
                    chapter_name = None
                    chapter = dict()
                    page_list = []

                    # LẤY DATA TỪNG CHAPTER
                    linkChapter = linkManga_base + '-' + chapter_list[i][0] + '/'
                    # print("Link chapter : \n\n", linkChapter)
                    rChapter = requests.get(linkChapter)
                    soupChapter = BeautifulSoup(rChapter.content, 'html.parser')

                    # TÊN CHAPTER + KIỂM TRA ĐÃ CRAWL CHƯA
                    try:
                        soup_content = soupChapter.find('div', class_='chapter-content-inner text-center')
                        chaptername = soup_content.img['alt']
                        chapter_name = chaptername[:-14]
                        print("\nChapter Name: ", chaptername)
                    except Exception as e:
                        print(e)
                    
                    # CRAWL ẢNH TỪNG CHAPTER
                    for img in soupChapter.findAll('img', attrs={'alt': chaptername}):
                        src = img['src'].replace('\n', '')
                        page_list.append(src)
                    # THÊM KEY Chapters vào DATA CHÍNH
                    chapter['chapter_id'] = chapter_id
                    chapter['chapter_name'] = chapter_name
                    chapter['page_list'] = page_list
                    chapters.append(chapter)

                    insert_query = f"""INSERT INTO {table_name} (manga_id,manga_name,thumbnail,author,last_update,categories,chapter_id,chapter_name,page_list) VALUES 
                    ("{manga_id}","{manga_name}","{thumbnail}","{author}","{datetime}","{categories}","{chapter_id}","{chapter_name}","{page_list}")"""
                    mycursor.execute(insert_query)
                    mydb.commit()
            
            # print("\nchapters:", chapters)
            data_crawl['manga_id'] = manga_id
            data_crawl['manga_name'] = manga_name
            data_crawl['thumbnail'] = thumbnail
            data_crawl['author'] = author
            data_crawl['last-update'] = datetime
            data_crawl['categories'] = categories
            data_crawl['chapters'] = chapters
            beetoon_crawl.append(data_crawl)
            # print("\ndata beetoon crawl:", beetoon_crawl)
            print("---"*20)
        cnt+=1

crawl_beetoon_data('latest-update', 1, 500)

with open('data1.json', 'w', encoding="utf-8") as f:
    json.dump(beetoon_crawl, f, indent=4)