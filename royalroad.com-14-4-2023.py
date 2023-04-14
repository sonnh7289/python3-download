from flask import Flask, jsonify, request
from bs4 import BeautifulSoup as bs
from flask_restful import Api, Resource
import json as js
import requests

app = Flask(__name__)
follower = "Followers"
page = "Pages"
view = "Views"
chapter = " Chapters"
fiction = "                             Fictions"
post = "Posts"
threads = "Threads"
joined = "Joined:"
last_active = "Last Active:"
gender = "Gender:"
location = "Location:"
bio = "Bio:"
follows = "Follows"
favorites = "Favorites"
ratings = "                             Ratings" 
fictions = "Fictions:"
total_words = "Total Words:"
total_reviews_received = "Total Reviews Received:"
total_rating_received = "Total Ratings Received:"
comments = "Comments" 
reviews = "                             Reviews"
# HOME
@app.route("/welcome", methods=["GET"])
def getWelcome():
    data = dict()
    home_nav = []
    home_manga = []
    home_author = list()
    session = requests.Session()
    Link_home_page =  session.get("https://www.royalroad.com/welcome")
    soupWelcome = bs(Link_home_page.content,'html.parser')
    for navbar in soupWelcome.find_all('li',class_= 'dropdown menu-dropdown classic-menu-dropdown'):
        item = list()
        list_navbar = dict()
        list_navbar['title'] = navbar.find('a').get('aria-label').strip()
        list_navbar['link'] = navbar.find('a').get('href')
        for navItem in navbar.find_all('a',class_= 'nav-link'):
            listItem = dict()
            listItem['title'] = navItem.text.strip()
            listItem['link'] = navItem.get('href')
            item.append(listItem)
            list_navbar['navitem'] = item     
            # print(navItem)
        home_nav.append(list_navbar)
        
    # POPULAR THIS WEEK AT WELCOME
    for manga_popular in soupWelcome.find_all('div',class_='col-md-4'):
        manga_popular_data = dict()
        manga_popular_data['name'] = manga_popular.find('h3').text.strip()
        manga_popular_data['link'] = manga_popular.find('a').get('href')
        manga_popular_data['image'] = manga_popular.find('img').get('src')
        manga_popular_data['content'] = manga_popular.find('div',class_='synopsis').text.strip()
        manga_popular_data['vote'] = float(manga_popular.find('span').get('title'))
        home_manga.append(manga_popular_data)
    # Published and well-known authors of our community
    for author in soupWelcome.find_all('div',class_='portlet light'):
        author_data = dict()
        author_data['name'] = author.find('div',class_='title').find('span').text.strip()
        author_data['publised_manga'] = author.find('a').text.strip()
        author_data['link_manga_published'] = author.find('a').get('href')
        author_data['avatar'] = author.find('img').get('src')
        author_data['description'] = author.find('div',class_='desc').find('span').text.strip()
        home_author.append(author_data)
    data['navbar'] = home_nav
    data['manga_home'] = home_manga
    data['published_author'] = home_author
    # print(soupWelcome)
    # return js.dumps(data,indent=4)
    return data
    
# BEST RATE
@app.route("/fictions/best-rated", methods=["GET"])
def getBestRate():
    data_best_rate = dict()
    list_manga = list()
    link_best_rate = request.headers.get('link-page') 
    session = requests.Session()
    # Link_home_page =  session.get("https://www.royalroad.com/fictions/best-rated")
    Link_home_page =  session.get(link_best_rate)
    best_rate_manga = bs(Link_home_page.content,'html.parser')
    for manga in best_rate_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        manga_data['descrition'] = manga.find('div',class_='margin-top-10 col-xs-12').text.replace("\n","")
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        infor = list(manga.find_all('span'))
        for i in infor:
            if follower in i.text:
                manga_data['followers'] = int(i.text.replace(follower,'').replace(',','').strip())
        for i in infor:
            if page in i.text:
                manga_data['pages'] = int(i.text.replace(page,'').replace(',','').strip()) 
        for i in infor:
            if view in i.text:
                manga_data['views'] = int(i.text.replace(view,'').replace(',','').strip())
        for i in infor:
            if chapter in i.text:
                manga_data['chapter'] = int(i.text.replace(chapter,'').replace(',','').strip())
        for i in infor:
            if i.get('title'):
                manga_data['vote'] = float(i.get('title'))
        manga_data['time'] = manga.find('time').text 
        list_manga.append(manga_data)
    data_best_rate['list_manga'] = list_manga
    return data_best_rate
 
# TRENDING   
@app.route("/fictions/trending", methods=["GET"])
def getTrending():
    data_trending = dict()
    list_manga = list()
    link_trending = request.headers.get('link-page')
    session = requests.Session()
    Link_home_page =  session.get("https://www.royalroad.com/fictions/trending")
    Link_home_page =  session.get(link_trending)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        manga_data['descrition'] = manga.find('div',class_='margin-top-10 col-xs-12').text.replace("\n","")
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        infor = list(manga.find_all('span'))
        for i in infor:
            if follower in i.text:
                manga_data['followers'] = int(i.text.replace(follower,'').replace(',','').strip())
        for i in infor:
            if page in i.text:
                manga_data['pages'] = int(i.text.replace(page,'').replace(',','').strip()) 
        for i in infor:
            if view in i.text:
                manga_data['views'] = int(i.text.replace(view,'').replace(',','').strip())
        for i in infor:
            if chapter in i.text:
                manga_data['chapter'] = int(i.text.replace(chapter,'').replace(',','').strip())
        for i in infor:
            if i.get('title'):
                manga_data['vote'] = float(i.get('title'))
        manga_data['time'] = manga.find('time').text 
        list_manga.append(manga_data)
    data_trending['trending_manga'] = list_manga
    return data_trending
    
# ON GOING FICTIONS
@app.route("/fictions/active-popular", methods=["GET"])
def getOnGoing():
    data_on_going = dict()
    list_manga = list()
    session = requests.Session()
    link_on_going = request.headers.get('link-page')
    Link_home_page =  session.get(link_on_going)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        manga_data['description'] = manga.find('div',class_='margin-top-10 col-xs-12').text.replace("\n","")
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        infor = list(manga.find_all('span'))
        for i in infor:
            if follower in i.text:
                manga_data['followers'] = int(i.text.replace(follower,'').replace(',','').strip())
        for i in infor:
            if page in i.text:
                manga_data['pages'] = int(i.text.replace(page,'').replace(',','').strip()) 
        for i in infor:
            if view in i.text:
                manga_data['views'] = int(i.text.replace(view,'').replace(',','').strip())
        for i in infor:
            if chapter in i.text:
                manga_data['chapter'] = int(i.text.replace(chapter,'').replace(',','').strip())
        for i in infor:
            if i.get('title'):
                manga_data['vote'] = float(i.get('title'))
        manga_data['time'] = manga.find('time').text 
        list_manga.append(manga_data)
    data_on_going['on_going_manga'] = list_manga
    return data_on_going

# COMPLETED MANGA
@app.route("/fictions/complete", methods=["GET"])
def getCompleted():
    data_complete = dict()
    list_manga = list()
    link_completed = request.headers.get('link-page')
    session = requests.Session()
    # Link_home_page =  session.get("https://www.royalroad.com/fictions/complete")
    Link_home_page =  session.get(link_completed)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        manga_data['description'] = manga.find('div',class_='hidden-content').text.replace("\n","")
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        list_manga.append(manga_data)
    data_complete['manga_completed'] = list_manga
    return data_complete

# POPULAR THIS WEEK
@app.route("/fictions/weekly-popular", methods=["GET"])
def getPopularWeek():
    data_popular_week = dict()
    list_manga = list()
    link_popular__week = request.headers.get('link-page')
    session = requests.Session()
    # Link_home_page =  session.get("https://www.royalroad.com/fictions/weekly-popular")
    Link_home_page =  session.get(link_popular__week)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        manga_data['description'] = manga.find('div',class_='margin-top-10 col-xs-12').text.replace("\n","")
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        infor = list(manga.find_all('span'))
        for i in infor:
            if follower in i.text:
                manga_data['followers'] = int(i.text.replace(follower,'').replace(',','').strip())
        for i in infor:
            if page in i.text:
                manga_data['pages'] = int(i.text.replace(page,'').replace(',','').strip()) 
        for i in infor:
            if view in i.text:
                manga_data['views'] = int(i.text.replace(view,'').replace(',','').strip())
        for i in infor:
            if chapter in i.text:
                manga_data['chapter'] = int(i.text.replace(chapter,'').replace(',','').strip())
        for i in infor:
            if i.get('title'):
                manga_data['vote'] = float(i.get('title'))
        manga_data['time'] = manga.find('time').text 
        list_manga.append(manga_data)
    data_popular_week['popular_this_week'] = list_manga
    return data_popular_week

# LATEST UPDATE
@app.route("/fictions/latest-updates", methods=["GET"])
def getLatestUpdate():
    data_latested_update = dict()
    list_manga = list()
    link_latest_update = request.headers.get('link-page')
    session = requests.Session()
    # Link_home_page =  session.get("https://www.royalroad.com/fictions/latest-updates")
    Link_home_page =  session.get(link_latest_update)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        manga_data['new_chapter'] = list()
        for chapter in manga.find_all('li',class_='list-item'):
            new_chapter = dict()
            new_chapter['link'] = chapter.find('a').get('href')
            new_chapter['title'] = chapter.find('span', class_='col-xs-8').text
            new_chapter['time'] = chapter.find('time').get('datetime')
            manga_data['new_chapter'].append(new_chapter)
        list_manga.append(manga_data)
    data_latested_update['latested_update'] = list_manga
    return data_latested_update

# NEW RELEASE
@app.route("/fictions/new-releases", methods=["GET"])
def getNewRelease():
    data_new_release = dict()
    list_manga = list()
    link_new_release = request.headers.get('link-page')
    session = requests.Session()
    # Link_home_page =  session.get("https://www.royalroad.com/fictions/new-releases")
    Link_home_page =  session.get(link_new_release)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        manga_data['content'] = manga.find('div',class_='hidden-content').text.replace("\n","")
        list_manga.append(manga_data)
    data_new_release['new_release'] = list_manga
    return data_new_release

# RISING STARS
@app.route("/fictions/rising-stars", methods=["GET"])
def getRisingStars():
    data_rising_stars = dict()
    list_manga = list()
    link_rising_star = request.headers.get('link-page')
    session = requests.Session()
    # Link_home_page =  session.get("https://www.royalroad.com/fictions/rising-stars")
    Link_home_page =  session.get(link_rising_star)
    trending_manga = bs(Link_home_page.content,'html.parser')
    for manga in trending_manga.find_all('div',class_='fiction-list-item row'):
        manga_data = dict()
        manga_data['categories'] = list()
        manga_data['title'] = manga.find('a',class_='font-red-sunglo bold').text
        manga_data['link'] = manga.find('a',class_='font-red-sunglo bold').get('href')
        manga_data['descrition'] = manga.find('div',class_='margin-top-10 col-xs-12').text.replace("\n","")
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_data['categories'].append(category)
        manga_data['image'] = manga.find('img',class_="img-responsive").get('src')
        infor = list(manga.find_all('span'))
        for i in infor:
            if follower in i.text:
                manga_data['followers'] = int(i.text.replace(follower,'').replace(',','').strip())
        for i in infor:
            if page in i.text:
                manga_data['pages'] = int(i.text.replace(page,'').replace(',','').strip()) 
        for i in infor:
            if view in i.text:
                manga_data['views'] = int(i.text.replace(view,'').replace(',','').strip())
        for i in infor:
            if chapter in i.text:
                manga_data['chapter'] = int(i.text.replace(chapter,'').replace(',','').strip())
        for i in infor:
            if i.get('title'):
                manga_data['vote'] = float(i.get('title'))
        manga_data['time'] = manga.find('time').text 
        list_manga.append(manga_data)
    data_rising_stars['rising_stars'] = list_manga
    return data_rising_stars

# GET MANGA
@app.route("/fictions/manga", methods=["GET"])
def getManga():
    data = dict()
    categories = list()
    link_full = request.headers.get('link-full')
    session = requests.Session()
    Link_home_page =  session.get(link_full)
    manga_detail = bs(Link_home_page.content,'html.parser')
    data['title'] = manga_detail.find('title').text
    for category in manga_detail.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
        category_list = dict()
        category_list['name'] = category.text
        category_list['link'] = category.get('href')
        categories.append(category_list)
    data['categories'] = categories
    data['content'] = manga_detail.find('div',class_='hidden-content').text.replace("\n","")
    data['author'] = dict()
    data['author']['name'] = manga_detail.find('a',class_='font-red').text
    data['author']['link'] = manga_detail.find('a',class_='font-red').get('href')
    data['author']['achivements'] = list()
    for achivement in manga_detail.find_all('div',class_='col-xs-5ths'):
        achivement_data = dict()
        achivement_data['content'] = achivement.find('img').get('data-content').replace('\t','')
        achivement_data['image'] = achivement.find('img').get('src')
        data['author']['achivements'].append(achivement_data)
    data['chapers'] = list()
    for chapter in manga_detail.find_all('tr',class_='chapter-row'):
        chapter_detail = dict()
        chapter_detail['release-date'] = chapter.find('td',class_='text-right').find('time').get('datetime')
        chapter_detail['name'] = chapter.find('td').find('a').text.replace("\n","").strip()
        chapter_detail['link'] = chapter.find('td').find('a').get('href')
        data['chapers'].append(chapter_detail)
    data['manga_relate'] = list()
    return data
    
# GET CHAPTER
@app.route("/fictions/manga/chapter", methods=["GET"])
def getChapter():
    data = dict()
    link_chaper = request.headers.get('link-chapter')
    session = requests.Session()
    Link_home_page =  session.get(link_chaper)
    soupChapter = bs(Link_home_page.content,'html.parser')
    data['name'] = soupChapter.find('meta', property='og:title').get('content')
    data['chapter_url'] = soupChapter.find('meta',property='og:url').get('content')
    data['image'] = soupChapter.find('meta', property='og:image').get('content')
    data['content'] = soupChapter.find('div',class_='chapter-inner chapter-content').text.replace("\n","").strip()
    data['publish_date'] = soupChapter.find('time').text
    data['author'] = dict()
    data['author']['name'] = soupChapter.find('a',class_='font-blue-dark').text
    data['author']['link_profile'] = soupChapter.find('a',class_='font-blue-dark').get('href')
    data['author']['fiction'] = int(soupChapter.find('a',class_='margin-bottom-10 btn btn-sm btn-primary col-xs-12 col-sm-4 col-md-12').text.replace("\n","").strip().replace(fiction,''))
    data['author']['link_fiction'] = soupChapter.find('a',class_='margin-bottom-10 btn btn-sm btn-primary col-xs-12 col-sm-4 col-md-12').get('href')
    for auth_chapter in  soupChapter.find_all('a',class_='margin-bottom-10 btn btn-sm btn-primary col-xs-6 col-sm-4 col-md-12'):
        if(post in auth_chapter.text):
            data['author']['post'] = int(auth_chapter.text.replace(post,'').replace('\n','').strip())
            data['author']['link_post'] = auth_chapter.get('href')
        if(threads in auth_chapter.text):
            data['author']['threads'] = int(auth_chapter.text.replace(threads,'').replace('\n','').strip())
            data['author']['link_threads'] = auth_chapter.get('href')
    for infor in soupChapter.find_all('li'):
        if(infor.find('i',class_='fa fa-user')):
            data['author']['schedule'] = infor.text.replace('\n','').strip()
        if(infor.find('i',class_='fa fa-globe')):
            data['author']['auth_website'] = infor.find('a').get('href')
    for bio in soupChapter.find_all('p'):
        if(bio.find('i',class_='fa fa-info-circle')):
            data['author']['bio'] = bio.text.replace('\r','').replace('\n','').strip()
    data['author']['achievements'] = list()
    for achievement in soupChapter.find_all('img',class_='img-responsive popovers'):
        achieve_infor = dict()
        achieve_infor['image'] = achievement.get('src')
        achieve_infor['content'] = achievement.get('data-content').replace('\t','')
        data['author']['achievements'].append(achieve_infor)       
    
    return data
 
# GET CATEGORIES   
@app.route("/fictions/search/category", methods=["GET"])
def getCategory():
    category_data = dict()
    manga_list = list()
    link_category = request.headers.get('link-category')
    session = requests.Session()
    Link_home_page =  session.get(link_category)
    categorySoup = bs(Link_home_page.content,'html.parser')
    for manga in categorySoup.find_all('div',class_='row fiction-list-item'):
        manga_detail = dict()
        manga_detail['categories'] = list()
        manga_detail['title'] = manga.find('a',class_='font-red-sunglo bold').text
        for categories in manga.find_all('a',class_='label label-default label-sm bg-blue-dark fiction-tag'):
            category = dict()
            category['name'] = categories.text
            category['link'] = categories.get('href')
            manga_detail['categories'].append(category)
        manga_detail['image'] = manga.find('img').get('src')
        infor = list(manga.find_all('span'))
        for i in infor:
            if follower in i.text:
                manga_detail['followers'] = int(i.text.replace(follower,'').replace(',','').strip())
        for i in infor:
            if page in i.text:
                manga_detail['pages'] = int(i.text.replace(page,'').replace(',','').strip()) 
        for i in infor:
            if view in i.text:
                manga_detail['views'] = int(i.text.replace(view,'').replace(',','').strip())
        for i in infor:
            if chapter in i.text:
                manga_detail['chapter'] = int(i.text.replace(chapter,'').replace(',','').strip())
        for i in infor:
            if i.get('title'):
                manga_detail['vote'] = float(i.get('title'))
        manga_detail['time'] = manga.find('time').text
        manga_detail['content'] = manga.find('div',class_='margin-top-10 col-xs-12').text.replace('\n','').strip()
        manga_list.append(manga_detail)
    category_data['category_manga'] = manga_list
    return category_data

# GET AUTHOR 
@app.route("/profile/author", methods=["GET"])
def getAuthor():  
    author_data = dict()
    author_data['auth_activity'] = dict()
    author_data['auth_info'] = dict()
    author_data['person_infor'] = dict()
    link_auth = request.headers.get('link-auth')
    session = requests.Session()
    Link_home_page =  session.get(link_auth)
    authSoup = bs(Link_home_page.content,'html.parser')
    author_data['name'] = authSoup.find('div',class_='text-center username').find('h1').text.replace('\n','').strip()
    list_btn = list()
    for list_group in authSoup.find_all('a',class_='icon-btn'):
        list_btn.append(list_group.get('href'))
    author_data['link'] = list_btn[0]
    author_data['link_fiction'] = list_btn[1]
    author_data['reviews'] = list_btn[2]
    author_data['favorites'] = list_btn[3]
    author_data['threads'] = list_btn[4]
    author_data['posts'] = list_btn[5]
    author_data['achievements'] = list_btn[6]
    author_data['reputation'] = list_btn[7]
    favorites_list = list()
    for info in authSoup.find_all('tr'):
        if joined in info.text:
            author_data['person_infor']['joined'] = info.find('time').text
        if last_active in info.text:
            author_data['person_infor']['last_active'] = info.find('time').text
        if gender in info.text:
            author_data['person_infor']['gender'] = info.find('td').text.replace('\n','').strip()
        if location in info.text:
            author_data['person_infor']['location'] = info.find('td').text.replace('\n','').strip()
        if bio in info.text:
            author_data['person_infor']['bio'] = info.find('td').text.replace('\n','').replace('\r','').strip()
        if follows in info.text:
            author_data['auth_activity']['follows'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if ratings in info.text:
            author_data['auth_activity']['ratings'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if reviews in info.text:
            author_data['auth_activity']['reviews'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if comments in info.text:
            author_data['auth_activity']['comment'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if total_words in info.text:
            author_data['auth_info']['total_word'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if total_reviews_received in info.text:
            author_data['auth_info']['total_reviews_received'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if fictions in info.text:
            author_data['auth_info']['fictions'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if total_rating_received in info.text:
            author_data['auth_info']['total_rating_received'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
        if favorites in info.text:
            b = int(info.find('td').text.replace('\n','').replace(',','').strip())
            favorites_list.append(b)
        if follower in info.text:
            author_data['auth_info']['followers'] = int(info.find('td').text.replace('\n','').replace(',','').strip())
    # GET FAVORITES
    author_data['auth_activity']['favorites'] = favorites_list[0]
    author_data['auth_info']['favorites'] = favorites_list[1]
    print(favorites_list)
    return author_data

# GET AUTHOR FICTIONS
@app.route("/profile/author/fictions", methods=["GET"])
def getAuthFictions():
    data = dict()
    manga_list = list()
    link_fiction = request.headers.get('link-fiction')
    session = requests.Session()
    Link_home_page =  session.get(link_fiction)
    authSoup = bs(Link_home_page.content,'html.parser')
    for manga in authSoup.find_all('div',class_='col-md-12'):
        manga_item = dict()
        small_tag = list()
        manga_item['title'] = manga.find('h2').text.replace('\n','').strip()
        manga_item['image'] = manga.find('img').get('src')
        manga_item['link'] = manga.find('a',class_='btn btn-default btn-outline').get('href')
        manga_item['content'] = manga.find('div',class_='fiction-description').text.replace('\n','').strip()
        for small in manga.find_all('small',class_='font-white'):
            small_tag.append(small.text)
        manga_item['status'] = small_tag[0]
        manga_item['pages'] = small_tag[1]
        print(small_tag)
        manga_list.append(manga_item)
    data['author'] = authSoup.find('div',class_='text-center username').find('h1').text.replace('\n','').strip()
    data['fictions'] = manga_list
    return data

# GET AUTHOR REVIEWS
@app.route("/profile/author/reviews", methods=["GET"])
def getAuthReviews():
    data = dict()
    review_list = list()
    link_review = request.headers.get('link-review')
    session = requests.Session()
    Link_home_page =  session.get(link_review)
    authSoup = bs(Link_home_page.content,'html.parser')
    for review in authSoup.find_all('div',class_='row review'):
        review_item = dict()
        review_item['manga'] = dict()
        review_item['title'] = review.find('h4').text.replace('\n','').strip()
        review_item['manga']['name'] = review.find('span',class_='bold uppercase font-red-sunglo').find('a').text
        review_item['manga']['href'] = review.find('span',class_='bold uppercase font-red-sunglo').find('a').get('href')
        review_item['image'] = review.find('img').get('src')
        review_item['content'] = review.find('div',class_='review-content').text.replace('\n','').strip()
        review_item['publish_date'] = dict()
        review_item['publish_date']['link'] = review.find('span',class_='pull-right date bold uppercase font-red-sunglo small').find('a').get('href')
        review_item['publish_date']['time'] = review.find('span',class_='pull-right date bold uppercase font-red-sunglo small').find('time').text
        review_list.append(review_item)
    data['reviews'] = review_list
    data['author'] = authSoup.find('div',class_='text-center username').find('h1').text.replace('\n','').strip()
    return data
    
# GET AUTHOR FAVORITES
@app.route("/profile/author/favorites", methods=["GET"])
def getAuthFavorites():
    data = dict()
    manga_list = list()
    link_favorite = request.headers.get('link-favorite')
    session = requests.Session()
    Link_home_page =  session.get(link_favorite)
    authSoup = bs(Link_home_page.content,'html.parser')
    for manga in authSoup.find_all('div',class_='col-md-12'):
        manga_item = dict()
        small_tag = list()
        manga_item['title'] = manga.find('h2').text.replace('\n','').strip()
        manga_item['image'] = manga.find('img').get('src')
        manga_item['link'] = manga.find('a',class_='btn btn-default btn-outline').get('href')
        manga_item['content'] = manga.find('div',class_='fiction-description').text.replace('\n','').strip()
        for small in manga.find_all('small',class_='font-white'):
            small_tag.append(small.text)
        manga_item['published_by'] = small_tag[0]
        manga_item['status'] = small_tag[1]
        manga_item['pages'] = small_tag[2]
        manga_list.append(manga_item)
    data['author'] = authSoup.find('div',class_='text-center username').find('h1').text.replace('\n','').strip()
    data['favorites'] = manga_list
    return data

    
if __name__ == '__main__':
    # app.run(debug=True, )
    app.run(host='0.0.0.0',debug=True)