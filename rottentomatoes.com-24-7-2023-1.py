from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import mysql.connector
import sqlite3
import time
import re
from more_itertools import strip

app = Flask(__name__)


# LẤY PHÂN LOẠI TRANG flim
@app.route("/home", methods=["GET"])
def get_Home():
    # link_full = requests.headers.get("Link-Full")

    listJsonflim = dict()
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    listJsonflim["NEWS TV THIS WEEK"] = []
    for itemflimLastUpdate in soupflim_base.findAll("a", class_="news-tile"):
        for flimLastUpdate in itemflimLastUpdate("tile-dynamic", orientation="landscape"):
            ItemJsonflim = dict()

            # LẤY link
            ItemJsonflim["link"] = itemflimLastUpdate.get("href")
            # lay ten
            ItemJsonflim["name_flim"] = flimLastUpdate.find("div", slot="caption").text.strip()

            # LẤY POSTER
            ItemJsonflim["poster_flim"] = flimLastUpdate.img["src"]

            listJsonflim["NEWS TV THIS WEEK"].append(ItemJsonflim)
    json_data1 = json.dumps(listJsonflim["NEWS TV THIS WEEK"])

    try:
        conn = sqlite3.connect("./rottentomatoes2.db")
        c = conn.cursor()
        print("Connected to SQLite")
        sqlite_insert_with_param = """ 
                        INSERT INTO Home (attribute_name, attribute_value) VALUES (?, ?);"""
        values = ("NEWS TV THIS WEEK", json_data1)
        c.execute(sqlite_insert_with_param, values)
        conn.commit()
        c.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    for inew in soupflim_base.findAll("section", id="media-lists"):
        id2 = inew.find_all("section", class_="dynamic-poster-list")
        # for id3 in id2:
        #     i3= i.find_all("tiles-carousel-responsive-item")
        #     for i5 in i3:
        #         a=i5.find("a").get("href")
        #         print(a)
        for i in id2:
            h = i.find("h2").text
            listJsonflim[h] = []
            i3 = i.find_all("tiles-carousel-responsive-item")
            for i5 in i3:
                a = i5.find("a").get("href")
                print(a)
            i2 = i.find_all("tile-dynamic")
            for itemflimLastUpdate, i5 in zip(i2, i3):
                ItemJsonflim = dict()
                ItemJsonflim["poster_flim"] = itemflimLastUpdate.find("img").get("src")
                # a_element = itemflimLastUpdate.find("a")
                # if a_element:
                ItemJsonflim["link"] = a = i5.find("a").get("href")
                # else:
                #     ItemJsonflim["link"] = inew.find("tiles-carousel-responsive-item",slot="tile").find("a").get("href")
                ItemJsonflim["name"] = itemflimLastUpdate.find("span").text.strip()
                listJsonflim[h].append(ItemJsonflim)
            json_data = json.dumps(listJsonflim[h])

            try:
                conn = sqlite3.connect("./rottentomatoes2.db")
                c = conn.cursor()
                print("Connected to SQLite")
                sqlite_insert_with_param = """ 
                                INSERT INTO Home (attribute_name, attribute_value) VALUES (?,?);"""
                values = (h, json_data)
                c.execute(sqlite_insert_with_param, values)
                conn.commit()
                c.close()

            except sqlite3.Error as error:
                print("Failed to insert Python variable into sqlite table", error)

    return listJsonflim

    # NEW & UPCOMING MOVIES


@app.route("/popular", methods=["GET"])
def get_Popular():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):
            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:
                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                ItemPopularflim["time_update"] = P.find("span", class_="smaller").text.strip()
                listPopularflim.append(ItemPopularflim)

    return listPopularflim

    # MOST POPULAR TV ON RT


@app.route("/movies", methods=["GET"])
def get_movies():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):

            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:
                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                ItemPopularflim["time_update"] = P.find("span", class_="smaller").text.strip()
                listPopularflim.append(ItemPopularflim)

    return listPopularflim


#   NEW TV THIS WEEK

@app.route("/New", methods=["GET"])
def get_New():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com/browse/tv_series_browse/sort:newest")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):

            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:
                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                ItemPopularflim["time_update"] = P.find("span", class_="smaller").text.strip()
                listPopularflim.append(ItemPopularflim)

    return listPopularflim

    # POPULAR IN THEATERS


@app.route("/TV", methods=["GET"])
def get_TV():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):

            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:

                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                # ItemPopularflim["time_update"] = P.find("span",class_= "smaller").text.strip()
                element = P.find("span", class_="smaller")
                if element:
                    ItemPopularflim["time_update"] = element.text.strip()
                else:
                    ItemPopularflim["time_update"] = None
                listPopularflim.append(ItemPopularflim)

    return listPopularflim

    #   POPULAR IN THEATERS


@app.route("/Best", methods=["GET"])
def get_Best():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):

            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:
                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                ItemPopularflim["time_update"] = P.find("span", class_="smaller").text.strip()
                listPopularflim.append(ItemPopularflim)

    return listPopularflim


#   LATEST CERTIFIED FRESH MOVIES

@app.route("/Fresh", methods=["GET"])
def get_Fresh():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get("https://www.rottentomatoes.com/browse/movies_at_home/critics:certified_fresh")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):

            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:
                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                ItemPopularflim["time_update"] = P.find("span", class_="smaller").text.strip()
                listPopularflim.append(ItemPopularflim)

    return listPopularflim


#   LATEST CERTIFIED FRESH MOVIES

@app.route("/h", methods=["GET"])
def get_h():
    # link_full = request.headers.get("Link-Full")
    listPopularflim = []
    session = requests.Session()
    rflim_base = session.get(
        "https://www.rottentomatoes.com/browse/movies_in_theaters/critics:certified_fresh,fresh~sort:newest")
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    index = 0

    for Popularflim in soupflim_base.findAll("div", class_="discovery-grids-container"):
        for Popular in Popularflim.findAll("div", class_="js-tile-link"):
            po = Popular.find_all("tile-dynamic", skeleton="panel")

            for P in po:
                ItemPopularflim = dict()

                # LẤY LINK

                ItemPopularflim["link"] = P.a["href"]

                ItemPopularflim["poster"] = P.find("img").get("src")

                ItemPopularflim["name_flim"] = P.find("img").get("alt")

                # LÁY THỜI GIAN CẬP NHẬT

                ItemPopularflim["time_update"] = P.find("span", class_="smaller").text.strip()
                listPopularflim.append(ItemPopularflim)

    return listPopularflim


# @app.route("/search/<string:text_search>", methods=["GET"])
# def get_Search(text_search):
@app.route("/search", methods=["GET"])
def get_Search():
    text_search = request.headers.get("text-search")
    textLinkSearch = text_search.strip().replace(" ", "%20")
    listJsonflim = dict()
    session = requests.Session()
    linksearch = "https://www.rottentomatoes.com/search?search=" + textLinkSearch
    rflim_base = session.get(linksearch)
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    listJsonflim["movie"] = []
    listJsonflim["franchise"] = []
    listJsonflim["tvSeries"] = []
    listJsonflim["celebrity"] = []
    for typeSearch in soupflim_base.findAll("search-page-result", type="franchise"):
        item = typeSearch.find_all("search-page-item-row")
        for flimLastUpdate in item:
            ItemJsonflim1 = dict()

            ItemJsonflim1["link"] = "https://www.rottentomatoes.com" + flimLastUpdate.find("a").get("href")
            # LẤY POSTER
            ItemJsonflim1["poster_flim"] = "http" + flimLastUpdate.find("a").img["src"].split("http")[-1]
            # lay ten
            ItemJsonflim1["name_flim"] = flimLastUpdate.find("a").img["alt"]
            listJsonflim["franchise"].append(ItemJsonflim1)

            #
    for typeSearch in soupflim_base.findAll("search-page-result", type="movie"):
        item = typeSearch.find_all("search-page-media-row")
        for flimLastUpdate in item:
            ItemJsonflim2 = dict()

            ItemJsonflim2["link"] = flimLastUpdate.find("a").get("href")
            # LẤY POSTER
            ItemJsonflim2["poster_flim"] = "http" + flimLastUpdate.find("a").img["src"].split("http")[-1]
            # lay ten
            ItemJsonflim2["name_flim"] = flimLastUpdate.find("a").img["alt"]
            listJsonflim["movie"].append(ItemJsonflim2)

    # 
    for typeSearch in soupflim_base.findAll("search-page-result", type="tvSeries"):
        item = typeSearch.find_all("search-page-media-row")
        for flimLastUpdate in item:
            ItemJsonflim3 = dict()

            ItemJsonflim3["link"] = flimLastUpdate.find("a").get("href")
            # LẤY POSTER
            ItemJsonflim3["poster_flim"] = "http" + flimLastUpdate.find("a").img["src"].split("http")[-1]
            # lay ten
            ItemJsonflim3["name_flim"] = flimLastUpdate.find("a").img["alt"]
            listJsonflim["tvSeries"].append(ItemJsonflim3)
    # 
    for typeSearch in soupflim_base.findAll("search-page-result", type="celebrity"):
        item = typeSearch.find_all("search-page-item-row")
        for flimLastUpdate in item:
            ItemJsonflim4 = dict()

            ItemJsonflim4["link"] = "https://www.rottentomatoes.com" + flimLastUpdate.find("a").get("href")
            # LẤY POSTER
            ItemJsonflim4["poster_flim"] = "http" + flimLastUpdate.find("a").img["src"].split("http")[-1]
            # lay ten
            ItemJsonflim4["name_flim"] = flimLastUpdate.find("a").img["alt"]
            listJsonflim["celebrity"].append(ItemJsonflim4)

    return listJsonflim


@app.route("/detail", methods=["GET"])
def get_Detail():
    linkDetail = request.headers.get("link-detail")
    # print(linkDetail)
    detailFullFilm = dict()
    session = requests.Session()
    rflim_base = session.get(linkDetail)
    soupflim_base = BeautifulSoup(rflim_base.content, "html.parser")
    for meta in soupflim_base.findAll("meta"):
        if meta.get("property") == "og:title":
            detailFullFilm["title"] = meta.get("content")
        if meta.get("property") == "og:description":
            detailFullFilm["description"] = meta.get("content")
        if meta.get("property") == "og:image":
            detailFullFilm["image"] = meta.get("content")
            break
    detailFullFilm["listimages"] = []
    for div in soupflim_base.findAll("div", class_="PhotosCarousel__item"):
        for img in div.findAll("img"):
            itemImage = dict()
            itemImage["image"] = img.get("src")
            detailFullFilm["listimages"].append(itemImage)
            break
    detailFullFilm["crewcasting"] = []
    for div in soupflim_base.findAll("div", class_="cast-and-crew-item"):
        castItem = dict()
        for ahref in div.findAll("a"):
            castItem["link"] = ahref.get("href")
        for img in div.findAll("img"):
            castItem["name"] = img.get("alt")
            castItem["image"] = img.get("src")
            detailFullFilm["crewcasting"].append(castItem)
            break
    detailFullFilm["review"] = []
    for div in soupflim_base.findAll("review-speech-balloon"):
        reviewList = dict()
        reviewList["reviewquote"] = div.get("reviewquote")
        reviewList["createdate"] = div.get("createdate")
        reviewList["criticimageurl"] = div.get("criticimageurl")
        detailFullFilm["review"].append(reviewList)

    return detailFullFilm


# Get New and Features
@app.route("/NewAndFeatures", methods=["GET"])
def get_NewAndFeatures():
    listNewAndFeatures = []
    session = requests.Session()
    new_base = session.get("https://www.rottentomatoes.com")
    soup_new_base = BeautifulSoup(new_base.content, "html.parser")
    for news in soup_new_base.findAll("div", class_="spotlight__scroll-wrap"):
        for new in news.findAll("li", class_="spotlight-item"):
            ItemNew = dict()
            # lay link
            link = new.a["href"]
            if link is not None:
                ItemNew["link"] = link
            else:
                ItemNew["link"] = ""
            poster = new.find("a").img["src"]
            if poster is not None:
                ItemNew["poster"] = "http" + poster.split("http")[-1]
            else:
                ItemNew["poster"] = ""
            title = new.find("h3")
            if title is not None:
                ItemNew["title"] = new.find("h3").text.strip()
            else:
                ItemNew["title"] = ""
            text = new.find("p")
            if text is not None:
                ItemNew["text"] = text.text.strip()
            else:
                ItemNew["text"] = ""
            listNewAndFeatures.append(ItemNew)
    return listNewAndFeatures


# @app.route("/celebrity/<string:name_actor>", methods=["GET"])
# def get_celebrity(name_actor):
@app.route("/celebrity", methods=["GET"])
def get_celebrity():
    link_actor = request.headers.get("link-celebrity")
    session = requests.Session()

    try:
        actor_base = session.get(link_actor)
    except:
        print("Could not find link actor")
        return [" Not find actor"]

    soup_actor_base = BeautifulSoup(actor_base.content, "html.parser")
    if soup_actor_base is None:
        return [" Not find actor"]
    info_actor = soup_actor_base.find("div", class_="celebrity-bio")
    if info_actor is not None:
        item_actor = dict()
        name = info_actor.find("h1")
        if name is not None:
            item_actor["name"] = name.text.strip()
            print(item_actor["name"])
        else:
            item_actor["name"] = ""
        poster_actor = info_actor.find('img', {'class': 'celebrity-bio__hero-img'})['src']
        if poster_actor is not None:
            item_actor["poster_actor"] = "http" + poster_actor.split("http")[-1]
        else:
            item_actor["poster_actor"] = ""
        try:
            item_actor["summary"] = info_actor.find("p", class_="celebrity-bio__summary").text.strip()
        except:
            item_actor["summary"] = ""
        item_actor_base = info_actor.findAll("p", class_="celebrity-bio__item")

        for id, item in enumerate(item_actor_base):
            if id == 0:
                try:
                    item_actor["highest_rated_%"] = item.find("span", class_="label").text.strip().split("\n")[0]
                    item_actor["highest_rated"] = item.find("a", class_="celebrity-bio__link").text.strip()
                    item_actor["highest_rated_link"] = "https://www.rottentomatoes.com" + item.a["href"]
                except:
                    item_actor["highest_rated_%"] = ""
                    item_actor["highest_rated"] = "Not Available"
                    item_actor["highest_rated_link"] = ""
            elif id == 1:
                try:
                    item_actor["lowest_rated_%"] = item.find("span", class_="label").text.strip().split("\n")[0]
                    item_actor["lowest_rated"] = item.find("a", class_="celebrity-bio__link").text.strip()
                    item_actor["lowest_rated_link"] = "https://www.rottentomatoes.com" + item.a["href"]
                except:
                    item_actor["lowest_rated_%"] = ""
                    item_actor["lowest_rated"] = "Not Available"
                    item_actor["lowest_rated_link"] = ""
            elif id == 2:
                try:
                    item_actor["birthday"] = item.text.replace("Birthday:\n", "").strip()
                except:
                    item_actor["birthday"] = "Not Available"
            elif id == 3:
                try:
                    item_actor["birthplace"] = item.text.replace("Birthplace:\n", "").strip()
                except:
                    item_actor["birthplace"] = "Not Available"
            else:
                print("Invalid information actor")
        return [item_actor]
    else:
        return [" Not find actor"]



@app.route("/franchise", methods=["GET"])
def get_franchise():
    link_film = request.headers.get("link-film")
    session = requests.Session()
    try:
        film_base = session.get(link_film)
    except:
        print("Could not find link film")
        return ["Not find film"]
    soup_film_base = BeautifulSoup(film_base.content, "html.parser")
    list_info_film_base = dict()
    Item_film = dict()
    name_film = soup_film_base.find("h1", class_="franchise-title__h1")
    if name_film is not None:
        Item_film["name_film"] = name_film.text.strip()
    else:
        Item_film["name_film"] = ""
    banner_film = soup_film_base.find("img", class_="franchise-hero__banner")["srcset"]
    if banner_film is not None:
        Item_film["banner_film"] = banner_film.split(" ")[-2]
    else:
        Item_film["banner_film"] = ""
    summary_film = soup_film_base.find("div", class_="franchise-hero__summary")
    if summary_film is not None:
        Item_film["summary_film"] = summary_film.text.strip().split("\n")[0]
    else:
        Item_film["summary_film"] = ""
    highest_rated_tv_show = soup_film_base.find("div", class_="franchise-hero__rating-header")
    if highest_rated_tv_show is not None:
        Item_film["highest_rated_tv_show"] = highest_rated_tv_show.text.strip()
    else:
        Item_film["highest_rated_tv_show"] = ""

    highest_rated_tv_show_percent = soup_film_base.find("div", class_="franchise-hero__icon-wrap")
    if highest_rated_tv_show_percent is not None:
        Item_film["highest_rated_tv_show_percent"] = highest_rated_tv_show_percent.text.strip()
    else:
        Item_film["highest_rated_tv_show_percent"] = ""
    show_title = soup_film_base.find("a", class_="franchise-hero__rating-link")
    if show_title is not None:
        Item_film["show_title"] = show_title.text.strip()
    else:
        Item_film["show_title"] = ""
    link_show_title = soup_film_base.find("a", class_="franchise-hero__rating-link")["href"]
    if link_show_title is not None:
        Item_film["link_show_title"] = "https://www.rottentomatoes.com" + link_show_title.strip()
    else:
        Item_film["link_show_title"] = ""

    list_info_film_base["header"] = [Item_film]
    Item_film_fearures = dict()
    list_features_base = soup_film_base.find("section", id="franchise-features")
    header_features = list_features_base.find("h2")
    if header_features is not None:
        Item_film_fearures["header_features"] = header_features.text.strip()
    else:
        Item_film_fearures["header_features"] = ""
    poster_features = list_features_base.find("img")["srcset"]
    if poster_features is not None:
        Item_film_fearures["poster_features"] = poster_features.strip()
    else:
        Item_film_fearures["poster_features"] = ""
    title_features = list_features_base.find("p", class_="franchise-feature__title")
    if title_features is not None:
        Item_film_fearures["title_features"] = title_features.text.strip()
    else:
        Item_film_fearures["title_features"] = ""

    list_info_film_base["features"] = [Item_film_fearures]

    list_photos_base = soup_film_base.find("section", id="photos-module")

    list_item_img_photos = []
    for item in list_photos_base.findAll("tiles-carousel-responsive-item"):
        if item is not None:
            list_item_img_photos.append(item.find("img")["src"])
        else:
            print("item none\n")

    list_info_film_base["list_img_photos"] = list_item_img_photos

    list_tv_shows = []
    list_tv_show_base = soup_film_base.find("ul", class_="franchise-media-list js-franchise-media-list")
    list_item_tv_show_base = list_tv_show_base.findAll("li", class_="franchise-media-list__item")
    for item_tv_show in list_item_tv_show_base:
        list_item_tv_show = dict()
        list_item_tv_show["poster_film"] = item_tv_show.find("img")["src"]
        highest_film_percent = item_tv_show.find("strong", {'data-qa': 'franchise-media-list__tomatometer'})
        if highest_film_percent is not None:
            list_item_tv_show["highest_film_percent"] = highest_film_percent.text.strip()
        else:
            list_item_tv_show["highest_film_percent"] = ""
        score_film_percent = item_tv_show.find("div", class_='franchise-media-list__audiences')
        if score_film_percent is not None:
            list_item_tv_show["score_film_percent"] = score_film_percent.text.strip()
        else:
            list_item_tv_show["score_film_percent"] = ""
        header_film = item_tv_show.find("h3", class_='franchise-media-list__h3')
        if header_film is not None:
            list_item_tv_show["header_film"] = header_film.text.strip
        else:
            list_item_tv_show["header_film"] = ""
        link_film = item_tv_show.find("a")["href"]
        if link_film is not None:
            list_item_tv_show["link_film"] = "https://www.rottentomatoes.com" + link_film.strip()
        else:
            list_item_tv_show["link_film"] = ""
        starting = item_tv_show.find("div", {"data-qa": "franchise-media-cast"})
        if starting is not None:
            list_item_tv_show["starting"] = re.sub('\s{2,}', ' ', starting.text.strip())
        else:
            list_item_tv_show["starting"] = ""
        executive_producer = item_tv_show.find("div", {"data-qa": "franchise-media-producer"})
        if executive_producer is not None:
            list_item_tv_show["executive_producer"] = re.sub('\s{2,}', ' ', executive_producer.text.strip())
        else:
            list_item_tv_show["executive_producer"] = ""
        list_tv_shows.append(list_item_tv_show)
    list_info_film_base["tv_shows"] = list_tv_shows

    list_news_base = soup_film_base.find("div", class_="content_body")
    list_news = []
    for news in list_news_base.findAll("a"):
        list_item_news = dict()
        title = news.find("div", class_="franchise-news__title")
        if title is not None:
            list_item_news["header_news"] = title.text.strip()
        else:
            list_item_news["header_news"] = ""
            continue
        link_news = news["href"]
        if link_news is not None:
            list_item_news["link_news"] = link_news.strip()
        else:
            list_item_news["link_news"] = ""
        photo = news.find("img", class_="franchise-news__photo")
        if photo is not None:
            list_item_news["photo_news"] = photo["src"].strip()
        else:
            list_item_news["photo_news"] = None
        list_news.append(list_item_news)
    list_info_film_base["news"] = list_news
    result = json.dumps(list_info_film_base, default=handle_non_serializable)

    return result


def handle_non_serializable(obj):
    if callable(obj):
        return str(obj)
    else:
        raise TypeError('Object is not JSON serializable')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3099)
