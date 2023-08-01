from operator import or_
from urllib.parse import urlparse
from flask import Flask, jsonify, make_response, request, url_for
import requests
import json
import mysql.connector
import time
from flask_mail import *
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import JWTManager
from bs4 import BeautifulSoup
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "ant3062003@gmail.com"
app.config["MAIL_PASSWORD"] = "tckkgibesnyxmppd"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["JWT_SECRET_KEY"] = "devsenior"
app.config["SECURITY_PASSWORD_SALT"] = "my_salt_value"
app.config["SECRET_KEY"]="manhdz"
jwt = JWTManager(app)
mail = Mail(app)
# config = {
#                 'user': 'root',
#                 'password': 'mcso@123#@!',
#                 'host': '14.225.7.221',
#                 'port': 81,
#                 'database': 'huydong'
#                 }
config = {
    "user": "root",
    "password": "18112002aD@",
    "host": "localhost",
    "port": 3306,
    "database": "manga",
}
#### API dki user
# kiem tra email dangki
s = URLSafeTimedSerializer("mysecretkey")


@app.route("/register", methods=["POST"])
def Create_account1():
    email = request.form.get("email")
    account_name = request.form.get("account_name")
    name_user = request.form.get("name_user")
    password = request.form.get("password")
    connection = mysql.connector.connect(**config)
    try:
        # connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM Create_account1 where email=%s", (email,)
            )
            user = cursor.fetchall()
            if not user:
                token = s.dumps(
                    {
                        "email": email,
                        "account_name": account_name,
                        "name_user": name_user,
                        "password": password,
                    },
                    salt=app.config["SECURITY_PASSWORD_SALT"],
                )
                msg = Message(
                    "Xác nhận tài khoản",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[email],
                )
                link = url_for(
                    "confirm_email", token=token, _external=True
                )  # link đến route 'confirm_email'
                msg.body = "Your confirmation link is " + link
                mail.send(msg)
                message = {"status": 200, "message": "Please check your email or spam"}

            else:
                message = {"status": 400, "message": "Account or email already exists"}

            cursor.close()

    except Exception as e:
        print("Error while connecting to MySQL", e)
        message = {"status": 500, "message": "Error connecting to the database"}

    finally:
        if connection.is_connected():
            connection.close()

    return jsonify(message)


@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        data = s.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=300
        )  # max_age = 1 day
        email = data["email"]
        account_name = data["account_name"]
        name_user = data["name_user"]
        password = data["password"]

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                cursor = connection.cursor()

                cursor.execute(
                    "SELECT * FROM Create_account1 where email=%s", (email,)
                )
                user = cursor.fetchall()
                if not user:
                    hashed_password = bcrypt.hashpw(
                        password.encode("utf-8"), bcrypt.gensalt()
                    )
                    cursor.execute(
                        "INSERT INTO Create_account1 (name_account, name_user, password, email) VALUES (%s,%s,%s,%s)",
                        (account_name, name_user, hashed_password, email),
                    )
                    connection.commit()
                    cursor.close()
                    message = {
                        "status": 200,
                        "message": "Account created and email confirmed. Please check your email or spam.",
                    }
                else:
                    message = {
                        "status": 400,
                        "message": "Account or email already exists",
                    }
        except Exception as e:
            print("Error while connecting to MySQL", e)
            message = {
                "status": 500,
                "message": "Error while adding account to the database",
            }

    except SignatureExpired:
        message = {
            "status": 400,
            "message": "The confirmation link is invalid or has expired.",
        }

    return jsonify(message)

    ####   API Đăng nhập tài khoản


# def get_check(password, hashed_password):
#     return bcrypt.checkpw(
#         password_user.encode("utf-8"), hashed_password.encode("utf-8")
#     )


# @app.route("/login", methods=["POST"])
# def login():
#     email = request.form.get("email")
#     password = request.form.get("password")
#     connection = mysql.connector.connect(**config)
#     try:
#         if connection.is_connected():
#             cursor = connection.cursor()
#             cursor.execute(
#                 "SELECT * FROM Create_account1 WHERE email=%s", (email,)
#             )
#             user = cursor.fetchone()
#             if user:
#                 hashed_password = user[4]  # Assuming password is stored in the 4th column
#                 if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
#                     # Generate a token
#                     token_data = {"email": email}
#                     token = jwt.encode(token_data, app.config["SECRET_KEY"], algorithm="HS256")
#                     return jsonify({"status": 200, "message": "Login successful", "token": token})
#                 else:
#                     return jsonify({"status": 401, "message": "Invalid email or password"})
#             else:
#                 return jsonify({"status": 401, "message": "Invalid email or password"})
#
#     except Exception as e:
#         print("Error while connecting to MySQL", e)
#         return jsonify({"status": 500, "message": "Error connecting to the database"})
#
#     finally:
#         if connection.is_connected():
#             connection.close()
#
#     return jsonify({"status": 500, "message": "Unknown error"})

@app.route("/login", methods=["POST"])
def loginAccount():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    try:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()

        # Kiểm tra thông tin email trong cơ sở dữ liệu
        sql = "SELECT * FROM create_account1 WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        user_info = mycursor.fetchone()

        if user_info:
            # Verify the password using bcrypt
            hashed_password = user_info[4]  # The hashed password stored in the database
            if bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            ):
                user = {
                    "id_user": user_info[0],
                    "email": user_info[1],
                    "name_account": user_info[2],
                    "name_user": user_info[3],
                    "password": user_info[4]
                }

                return {"ketqua": "Đăng nhập thành công!", "user": user}
            else:
                return {"ketqua": "Email hoặc mật khẩu không đúng."}
        else:
            return {"ketqua": "Email hoặc mật khẩu không đúng."}

    except Exception as e:
        return {"ketqua": "Lỗi khi kết nối đến cơ sở dữ liệu."}


####   API lay lai mat khau
@app.route("/forgot_pass", methods=["GET"])
def get_forgotpass():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                "SELECT password FROM Create_account1 WHERE email = %s", (email,)
            )
            result = cursor.fetchone()
            if result[4] is not None:
                token = s.dumps(
                    {"email": email, "password": password},
                    salt=app.config["SECURITY_PASSWORD_SALT"],
                )
                msg = Message(
                    "Xác nhận tài khoản",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[email],
                )
                link = url_for(
                    "confirm_account", token=token, _external=True
                )  # link đến route 'confirm_email'
                msg.body = "Your confirmation link is " + link
                mail.send(msg)
                data = {"status": 200, "message": "Please check your email or spam"}
            else:
                data = "Email không tồn tại"
        else:
            data = "Không thể kết nối đến cơ sở dữ liệu."
    except Exception as e:
        print("Error while connecting to MySQL", e)
        data = "Lỗi khi kết nối đến cơ sở dữ liệu."
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return jsonify({"message": data})


@app.route("/confirm_account/<token>")
def confirm_account(token):
    try:
        data = s.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=300)
        email = data["email"]
        password = data["password"]
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE Create_account1 SET password=%s WHERE email=%s",
                    (hashed_password, email),
                )
                connection.commit()
                message = {"status": 200, "message": "Password reset successful"}
            else:
                message = {"status": 500, "message": "Lỗi kết nối đến cơ sở dữ liệu"}
        except Exception as e:
            print("Error while connecting to MySQL", e)
            message = {
                "status": 500,
                "message": "Lỗi khi thêm tài khoản vào cơ sở dữ liệu",
            }

    except SignatureExpired:
        message = {
            "status": 400,
            "message": "Liên kết xác nhận không hợp lệ hoặc đã hết hạn.",
        }

    return jsonify(message)


@app.route("/search", methods=["GET"])
def searchManga():
    listJsonManga = {}
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonManga["latest_uptate"] = "READ MANGA ONLINE - LATEST UPDATES"
    chapter = soupManga_base.find("div", class_="content-homepage-item-right")
    link_full = []

    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all(
        "div", class_="search-story-item"
    ):
        item = {}
        item2 = {}
        item["title"] = itemMangaLastUpdate.find("a", class_="item-img").text
        item["link"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.a["href"]
        item["poster"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.img["src"]
        item["authod"] = itemMangaLastUpdate.find(
            "span", class_="text-nowrap item-author"
        ).text
        index2 = 0
        link_full2 = []
        for chap in itemMangaLastUpdate.find_all(
            "a", class_="item-chapter a-h text-nowrap"
        ):
            item2 = "https://ww5.manganelo.tv" + chap.get("href")
            link_full2.append(item2)
            item["chapter_home"] = link_full2
        indexRun = indexRun + 1
        link_full.append(item)
    listJsonManga["manga_link"] = link_full
    return listJsonManga


@app.route("/categorieslist", methods=["GET"])
def categorieslist():
    listJsonManga = {}
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonManga["latest_uptate"] = "READ MANGA ONLINE - LATEST UPDATES"
    chapter = soupManga_base.find("div", class_="content-homepage-item-right")
    link_full = []

    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all(
        "div", class_="content-genres-item"
    ):
        item = {}
        item2 = {}
        item["title"] = itemMangaLastUpdate.find("a", class_="genres-item-img").get(
            "title"
        )
        item["link"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.a["href"]
        item["poster"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.img["src"]
        item["author_home"] = itemMangaLastUpdate.find(
            "span", class_="genres-item-author"
        ).text
        index2 = 0
        link_full2 = []
        for chap in itemMangaLastUpdate.find_all("a"):
            itemChapter = {}
            itemChapter["link"] = "https://ww5.manganelo.tv" + chap.get("href")
            itemChapter["title"] = chap.get("title")
            link_full2.append(itemChapter)
            item["chapter_home"] = link_full2
        indexRun = indexRun + 1
        link_full.append(item)
    listJsonManga["manga_link"] = link_full
    return listJsonManga


# Lấy category ở home
# Lấy link chapter
@app.route("/homenelo", methods=["GET"])
def get_Home():
    listJsonManga = {}
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonManga["latest_uptate"] = "READ MANGA ONLINE - LATEST UPDATES"
    chapter = soupManga_base.find("div", class_="content-homepage-item-right")
    link_full = []

    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all(
        "div", class_="content-homepage-item"
    ):
        item = {}
        item2 = {}
        item["title"] = itemMangaLastUpdate.find(
            "a", class_="tooltip a-h text-nowrap"
        ).text
        item["link"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.a["href"]
        item["poster"] = (
            "https://ww5.manganelo.tv" + itemMangaLastUpdate.img["data-src"]
        )
        item["author_home"] = (
            itemMangaLastUpdate.find("span", class_="text-nowrap item-author")
            .text.replace("\r", "")
            .replace("\n", " ")
            .replace(" ", "")
        )
        index2 = 0
        link_full2 = []
        for chap in itemMangaLastUpdate.find_all("p", class_="a-h item-chapter"):
            itemChapter = {}
            item2 = chap.text.replace("\r", "-").replace("\n", " ")
            itemChapter["title"] = item2
            itemChapter["link"] = chap.a["href"]
            link_full2.append(itemChapter)
        item["chapter_home"] = link_full2
        indexRun = indexRun + 1
        link_full.append(item)
    listJsonManga["manga_link"] = link_full
    return listJsonManga


# Lấy category ở home
@app.route("/category_home", methods=["GET"])
def get_category():
    listJsonMang = {}
    item = []
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonMang["genres"] = "MANGA BY GENRES"
    soup = soupManga_base.find("div", class_="panel-category")
    category = soup.find_all("p", class_="pn-category-row")
    list_cate = []
    for item in category:
        text_cate = item.text.replace("\r", "").replace("\n", " ")
        list_cate.append(str(text_cate))
    listJsonMang["category_home"] = list_cate
    return listJsonMang


# lấy thông tin của manga
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, "html.parser")
    detail = {}
    data1 = soup.find("table", class_="variations-tableInfo")
    lis = []

    def ac():
        name_imgs = data1.find_all("tr")
        lis = []
        for i in name_imgs[3]:
            text_a = (
                i.text.replace("\r", "")
                .replace("\n", "")
                .replace(" - ", ",")
                .replace(" ", "")
            )
            lis.append(str(text_a))
        del lis[0:3]
        return lis[:-1]

    # LẤY POSTER
    detail["poster_manga"] = "https://ww5.manganelo.tv" + soup.find(
        "div", class_="story-info-left"
    ).find("img", class_="img-loading").get("src")
    df = soup.find_all("h1")
    # LẤY TIÊU ĐỀ
    for i in df:
        detail["title_manga"] = i.text
    # LẤY AUTHOR
    list_au = []
    for au in data1.find_all("td", class_="table-value"):
        text_au = au.text.replace("\r", "").replace("\n", " ")
        list_au.append(text_au)
    detail["author"] = list_au[1]
    # LẤY DESCRIPTIONS
    des = soup.find("div", class_="story-info-right").findAll("h2")
    for ii in des:
        detail["descriptions"] = (
            ii.text.replace("\r", "").replace("\n", "").replace(" ", "")
        )
    # Lấy status
    status = soup.find("div", class_="story-info-right").find_all("tr")
    for st in status[2].find("td", class_="table-value"):
        detail["status"] = st.text.strip()
    # Lấy thể loại
    for li in data1.find_all("tr"):
        detail["categories"] = ac()
    detail["last_update"] = "27/12/2014"
    # Lấy lượt xem
    view = soup.find("div", class_="story-info-right-extent").find_all("p")
    for st in view[1].find("span", class_="stre-value"):
        detail["View"] = st.text.strip()
    # lấy xếp hạng
    list_xh = []
    for xh in view:
        text = xh.text.replace("\r", "").replace("\n", "")
        list_xh.append(text)
    detail["Rating"] = list_xh[3]
    # LẤY IMG BOOKMARK
    view2 = soup.find("div", class_="story-info-right-extent").find(
        "p", class_="info-bookmark"
    )
    detail["infor_bookmark"] = "https://ww5.manganelo.tv/" + view2.find("img").get(
        "src"
    )
    # LẤY NỘI DUNG
    list_nd = []
    nd = soup.find("div", class_="panel-story-info-description")
    for text1 in nd:
        text_nd = text1.text.replace("\r", "").replace("\n", "")
        list_nd.append(text_nd)
    detail["Description"] = list_nd[2]
    return detail


# Lấy  link chapter
@app.route("/chapter", methods=["GET"])
def get_Chapter():
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, "html.parser")
    item = {}
    data1 = soup.find("table", class_="variations-tableInfo")
    data_link = (
        soup.find("div", class_="panel-story-chapter-list")
        .find("ul", class_="row-content-chapter")
        .find_all("li", class_="a-h")
    )
    link_all = []
    for link in data_link:
        link_all.append(link.find("a").get("href"))
        reversed_link_all = list(reversed(link_all))

    def get_link_img(url_link):
        link_imgs = []
        request = requests.get("https://ww5.manganelo.tv/" + str(url_link))
        soup = BeautifulSoup(request.text, "html.parser")
        data_img = soup.find("div", class_="container-chapter-reader").find_all(
            "img", class_="img-loading"
        )
        for item in data_img:
            link_imgs.append(item.get("data-src"))
        return link_imgs

    def get_name_img(url_name):
        request = requests.get("https://ww5.manganelo.tv/" + str(url_name))
        soup = BeautifulSoup(request.text, "html.parser")
        name_imgs = soup.find("div", class_="panel-chapter-info-top").find("h1").text
        return name_imgs

    link_all_img = []
    for link_img in range(0, len(reversed_link_all)):
        item_img = {}
        a = "page_list" + str(link_img + 1)
        item_img["chapter_id"] = link_img + 1
        item_img["chapter_name"] = get_name_img(reversed_link_all[link_img])
        item_img[a] = get_link_img(reversed_link_all[link_img])
        link_all_img.append(item_img)
    item["chapters"] = link_all_img
    return item


# # API lưu thông tin bộ truyện yêu thích của người dùng
@app.route("/api/favorite/<string:iduser>", methods=["POST"])
def add_favorite(iduser):
    id_like = request.form.get("like_id")
    # id_user =request.form.get('user_id')
    link = request.form.get("link")
    saved_at = request.form.get("saved_at")
    like_ip = request.form.get("like_ip")
    name_device_like = request.form.get("name_device")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            # curs.execute("INSERT INTO mangaFavorite (idLike,idUser, Link_Manga_like, dateTimeLike,ip_like,name_device) VALUES (%s, %s,%s, %s,%s,%s)", (id_like,id_user, link, saved_at, like_ip, name_device_like))
            curs.execute(
                "INSERT INTO mangaFavorite (idUser, Link_Manga_like, dateTimeLike,ip_like,name_device) VALUES (%s,%s, %s,%s,%s)",
                (iduser, link, saved_at, like_ip, name_device_like),
            )
            data = "Favorite added successfully!"
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API get ⇒ list favirote của 1 user


@app.route("/api/favirote/<string:iduser>", methods=["GET"])
def get_id(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * from mangaFavorite where idUser=%s", (iduser,))
            data = creatcur.fetchall()
            connection.commit()
            creatcur.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API get ⇒ lấy 200 recent mới nhất của cả hệ thống user


@app.route("/api/last_200_recent", methods=["GET"])
def get_200_recent():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute(
                "SELECT * FROM mangaFavorite ORDER BY idLike DESC LIMIT 200"
            )
            data = creatcur.fetchall()
            connection.commit()
            creatcur.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API thêm recent của 1 user
@app.route("/api/recent/<string:iduser>", methods=["POST"])
def add_recent(iduser):
    link_chapter = request.form.get("link_chapter")
    link_manga = request.form.get("link_manga")
    datetime = request.form.get("datetime")
    ip_readed = request.form.get("ip_readed")
    name_device_readed = request.form.get("name_device")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO recent_chapter_readed (link_detail_chapter, id_user, link_detail_manga, datetime, ip_readed, name_device_readed) VALUES (%s,%s,%s, %s,%s,%s)",
                (
                    link_chapter,
                    iduser,
                    link_manga,
                    datetime,
                    ip_readed,
                    name_device_readed,
                ),
            )
            data = "Favorite added successfully!"
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API lấy toàn bộ recent của 1 user


@app.route("/api/recent/<string:iduser>", methods=["GET"])
def get_recent(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute(
                "SELECT * from recent_chapter_readed where id_user=%s", (iduser,)
            )
            data = creatcur.fetchall()
            connection.commit()
            creatcur.close()
            connection.close()
            data = "Favorite added successfully!"
    except:
        data = "error"
    return jsonify(data)


# API thêm avatar của 1 user
@app.route("/api/avatar/<string:iduser>", methods=["POST"])
def add_avatar(iduser):
    link_avatar = request.form.get("link_avatar")
    password = request.form.get("password")
    TimeOnline = request.form.get("TimeOnline")
    ip_register = request.form.get("ip_register")
    device_name_register = request.form.get("name_device")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO users (link_avatar, id_user, password, TimeOnline, ip_register, device_name_register) VALUES (%s,%s,%s, %s,%s,%s)",
                (
                    link_avatar,
                    iduser,
                    password,
                    TimeOnline,
                    ip_register,
                    device_name_register,
                ),
            )
            connection.commit()
            curs.close()
            connection.close()
            data = "Favorite added successfully!"
    except:
        data = "error"
    return jsonify(data)


# API post thêm comment vào profile của 1 user
@app.route("/api/profile/comment/<string:iduser>", methods=["POST"])
def add_comment(iduser):
    Id_User_Comment = request.form.get("Id_User_Comment")
    NoiDungComment = request.form.get("NoiDungComment")
    link_image_attach = request.form.get("link_image_attach")
    dateTimeComment = request.form.get("dateTimeComment")
    nameDevice_Comment = request.form.get("name_device")
    IPComment = request.form.get("IPComment")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO comment_user (Id_User_Comment, Id_User_Bi_Comment, NoiDungComment, link_image_attach, dateTimeComment, nameDevice_Comment,IPComment) VALUES (%s,%s,%s, %s,%s,%s, %s)",
                (
                    Id_User_Comment,
                    iduser,
                    NoiDungComment,
                    link_image_attach,
                    dateTimeComment,
                    nameDevice_Comment,
                    IPComment,
                ),
            )
            connection.commit()
            curs.close()
            connection.close()
            data = "Favorite added successfully!"
    except:
        data = "error"
    return jsonify(data)


# API post lấy toàn bộ comment trên 1 user
@app.route("/api/profile/comment/<string:iduser>", methods=["GET"])
def get_comment(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute(
                "SELECT * from comment_user where id_User_Bi_Comment=%s", (iduser,)
            )
            data = creatcur.fetchall()
            connection.commit()
            creatcur.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API get ⇒ lấy 200 recent mới nhất của cả hệ thống user
@app.route("/api/200_comment", methods=["GET"])
def get_200_comment():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute(
                "SELECT * FROM comment_user ORDER BY idComment DESC LIMIT 200"
            )
            data = creatcur.fetchall()
            connection.commit()
            creatcur.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API post thêm thời gian đang hoạt động lên 1 trường trên database, cứ 1 phút gọi 1 lần
@app.route("/api/online/<string:iduser>", methods=["POST"])
def add_timeonline(iduser):
    link_avatar = request.form.get("link_avatar")
    ip_register = request.form.get("ip_register")
    device_name_register = request.form.get("device_name_register")
    password = request.form.get("password")
    TimeOnline = request.form.get("TimeOnline")
    # id_user = request.form.get('id_user')
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcurs = connection.cursor()
            creatcurs.execute("SELECT id_user FROM users where id_user=%s", (iduser,))
            users = creatcurs.fetchone()
            if users is not None:
                curs = connection.cursor()
                curs.execute(
                    "UPDATE users SET link_avatar = %s, password = %s, TimeOnline = %s, ip_register = %s, device_name_register = %s WHERE id_user = %s",
                    (
                        link_avatar,
                        password,
                        TimeOnline,
                        ip_register,
                        device_name_register,
                        iduser,
                    ),
                )
                connection.commit()
                curs.close()
                connection.close()
            else:
                curs = connection.cursor()
                curs.execute(
                    "INSERT INTO users (link_avatar, id_user, password, TimeOnline, ip_register, device_name_register) VALUES (%s,%s,%s, %s,%s,%s)",
                    (
                        link_avatar,
                        iduser,
                        password,
                        TimeOnline,
                        ip_register,
                        device_name_register,
                    ),
                )
                connection.commit()
                curs.close()
                connection.close()
        data = "Favorite added successfully!"
    except:
        data = "error"
    return jsonify(data)


def goi_timeonline(iduser):
    # t = threading.Thread(target=update_timeonline, args=[iduser])
    # t.start()
    while True:
        add_timeonline(iduser)
        time.sleep(60)


# API kiểm tra user hiện tại có đang online không ?
@app.route("/api/check_online/<string:iduser>", methods=["GET"])
def get_TimeOnline(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("SELECT TimeOnline FROM users where id_user=%s", (iduser,))
            query = curs.fetchone()
            connection.commit()
            curs.close()
            connection.close()
            if int(query[0]) > 0:
                data = "online"
            else:
                data = "offline"
    except:
        data = "error"
    return jsonify(data)


# API ấy toàn bộ các user đang online trên hệ thống
@app.route("/get/api/list_online", methods=["GET"])
def get_Online():
    a = "0"
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("SELECT * FROM users where TimeOnline>%s", (a,))
            data = curs.fetchall()
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API post comment vào 1 chapter
@app.route("/api/comment/chapter", methods=["POST"])
def add_comment_chapter():
    idUser = request.form.get("idUser")
    link_chapter = request.form.get("link_chapter")
    link_manga = request.form.get("link_manga")
    ip_comment = request.form.get("ip_comment")
    device_comment = request.form.get("device_comment")
    noidungComment = request.form.get("noidungComment")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO comment_chapter (idUser, noidungComment, link_chapter, link_manga, ip_comment, device_comment) VALUES (%s,%s,%s, %s,%s,%s)",
                (
                    idUser,
                    noidungComment,
                    link_chapter,
                    link_manga,
                    ip_comment,
                    device_comment,
                ),
            )
            connection.commit()
            curs.close()
            connection.close()
            data = "Favorite added successfully!"
    except:
        data = "error"
    return jsonify(data)


# API lấy toàn bộ comment của 1 user vào các bộ truyện manga
@app.route("/api/comment/<string:iduser>", methods=["GET"])
def get_user_comment(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "SELECT noidungComment,idComment FROM comment_chapter where idUser=%s",
                (iduser,),
            )
            data = curs.fetchall()
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API get ⇒ lấy 200 comment mới nhất của cả hệ thống user
@app.route("/api/last_200_comment", methods=["GET"])
def get_last_200_comment():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute(
                "SELECT * FROM comment_chapter ORDER BY idComment DESC LIMIT 200"
            )
            data = creatcur.fetchall()
            connection.commit()
            creatcur.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API dki user

s = URLSafeTimedSerializer("mysecretkey")


# @app.route("/register", methods=["POST"])
# def create_account():
#     email = request.form.get("email")
#     try:
#         connection = mysql.connector.connect(**config)
#         if connection.is_connected():
#             cursor = connection.cursor()
#
#             cursor.execute("SELECT * FROM Create_account where email=%s", (email,))
#             user = cursor.fetchall()
#             if not user:
#                 token = s.dumps(
#                     {"email": email}, salt=app.config["SECURITY_PASSWORD_SALT"]
#                 )
#                 msg = Message(
#                     "Xác nhận tài khoản",
#                     sender=app.config["MAIL_USERNAME"],
#                     recipients=[email],
#                 )
#                 link = url_for(
#                     "confirm_email", token=token, _external=True
#                 )  # link đến route 'confirm'
#                 msg.body = "Your confirmation link is " + link
#                 mail.send(msg)
#                 message = {"status": 200, "message": "Please check your email or spam"}
#                 connection.commit()
#
#             else:
#                 message = {"status": 400, "message": "Account or gmail already exists"}
#
#             cursor.close()
#
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#         message = {"status": 500, "message": "error connected database"}
#
#     finally:
#         if connection.is_connected():
#             connection.close()
#
#     return jsonify(message)


# kiểm tra xác nhận email
# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=86400) # max_age = 1 day
#         # update status of user's account in the database
#         message = 'Your email has been confirmed. Thanks for registering!'
#     except SignatureExpired:
#         message = 'The confirmation link is invalid or has expired.'
#     return message


# thêm tài khoản vào database
# @app.route("/add_account", methods=["POST"])
# def get_account():
#     email = request.form.get("email")
#     account_name = request.form.get("account_name")
#     name_user = request.form.get("name_user")
#     password = request.form.get("password")
#     try:
#         connection = mysql.connector.connect(**config)
#         if connection.is_connected():
#             curs = connection.cursor()
#             curs.execute(
#                 "INSERT INTO Create_account (name_account, name_user, password, email) VALUES (%s,%s,%s,%s)",
#                 (account_name, name_user, password, email),
#             )
#             connection.commit()
#             curs.close()
#             connection.close()
#             data = "Favorite added successfully!"
#     except:
#         data = "error"
#     return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1983)
