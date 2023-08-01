# from schemas.img_schemas import cut_change_schemas,change_img_schemas
from config.db import engine
from models.index import cut_change, change_img
from fastapi.responses import FileResponse
import os  # ,cv2, uuid, pixellib
import bcrypt

import jwt
from datetime import datetime, timedelta
from functools import wraps

# import matplotlib.pyplot as plt
from sqlalchemy import desc
from pixellib.tune_bg import alter_bg
from rembg import remove

# from random import randint
import random
import base64
import io
import PIL.Image
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import Depends, FastAPI, Header, Request, Body, File, UploadFile
import requests
import shutil
import random
import string
import json
from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from itsdangerous import URLSafeTimedSerializer

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS, cross_origin
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)


# ______SONPIPI______
from pickle import FALSE
from tkinter import TRUE
import mysql.connector
import smtplib
import hashlib
import requests
import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from getpass import getpass
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, url_for

app = Flask(__name__)
# apiFLASK = Api(app)


cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

IMAGEDIR = "images/"
IMAGEDIR_OUT = "images/out_put/"
YOUR_SECRET_KEY = "keysecret"

secret = URLSafeTimedSerializer("123456")


config = {
    "user": "root",
    "password": "18112002aD@",
    "host": "localhost",
    "port": 3306,
    "database": "fakelocation1",
}
# cred = firebase_admin.credentials.Certificate('fir-sigup-b773e-firebase-adminsdk-anunx-0416c5a276.json')
# cred = firebase_admin.credentials.Certificate('fir-sigup-b773e-firebase-adminsdk-anunx-f6abbb59a1.json')
cred = firebase_admin.credentials.Certificate(
    "fakelocation1-c0453-firebase-adminsdk-aug09-56c714bd51.json"
)

firebase_admin.initialize_app(cred)


@app.route("/register", methods=["POST"])
def register():
    from_address = "nguyentienmanh181102@gmail.com"
    password_mail = "avsmfkqcjouesezo"

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")
    user_name = data.get("user_name")
    link_avatar = data.get("link_avatar")
    ip_register = data.get("ip_register")
    device_register = data.get("device_register")

    if email is None and password is None and user_name is None:
        return jsonify(message="Please enter your email and password and user name!")
    elif email is None:
        return jsonify(message="Please enter your email!")
    elif password is None:
        return jsonify(message="Please enter your password!")
    elif email is None and password is None:
        return jsonify(message="Please enter your email and password!")
    elif user_name is None:
        return jsonify(message="Please enter your user name!")
    elif password is None and user_name is None:
        return jsonify(message="Please enter your password and user name!")
    elif email is None and user_name is None:
        return jsonify(message="Please enter your email and user name!")

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", [email])
    account = cursor.fetchone()
    print(account)
    cursor.close()
    if account:
        return jsonify(message="Account already exists!")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(message="Invalid email address!")
    elif not password or not email:
        return jsonify(message="Incorrect email/password!")
    elif len(password) < 8:
        return jsonify(message="Password must be at least 8 characters.")
    else:
        data = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "user_name": user_name,
            "link_avatar": link_avatar,
            "ip_register": ip_register,
            "device_register": device_register,
        }
        token = secret.dumps(data, salt="d5e6d7g8h9w6rq5w6r7z8x7z8x9c")
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = email
        msg["Subject"] = "Social Thinkdiff Company"
        link = url_for("register_confirm", token=token, _external=True)
        body = (
            """
    Thank You
    We appreciate your interest in connecting with us at, you can find related resources mentioned during the presentation on the session resources page.
    Devsenior Thinkdiff Company
    """
            + link
        )
        # mail.send(msg)
        msg.attach(MIMEText(body.format(email), "html"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_address, password_mail)
            server.sendmail(from_address, email, msg.as_string())
        return jsonify(
            message="Please check your email or spam", account={"email": email}
        )


@app.route("/register/confirm/<token>")
def register_confirm(token):
    try:
        print("halllo")
        confirmed_email = secret.loads(token, salt="d5e6d7g8h9w6rq5w6r7z8x7z8x9c")
        print(confirmed_email["email"])
        connection = mysql.connector.connect(**config)
        print("test1")
        cursor = connection.cursor()
        print("test2")
        cursor.execute(
            "SELECT * FROM user WHERE email = %s", [confirmed_email["email"]]
        )
        print("test")
        account = cursor.fetchone()
        cursor.close()
        print(account)
        print("helo")
        if account:
            return jsonify(message="Your account was already confirm")
        else:
            save_user_to_mysql(
                confirmed_email["email"],
                confirmed_email["password"],
                confirmed_email["full_name"],
                confirmed_email["user_name"],
                confirmed_email["link_avatar"],
                confirmed_email["ip_register"],
                confirmed_email["device_register"],
            )
    except Exception:
        return {"message": "Your link was expired. Try again"}

    return {"message": "Confirm successfully. Try to login"}


def save_user_to_mysql(
    email, password, full_name, user_name, link_avatar, ip_register, device_register
):
    connection = mysql.connector.connect(**config)
    mycursor = connection.cursor()

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Thực hiện các thao tác trên cơ sở dữ liệu
    # Ví dụ: Thêm thông tin người dùng vào bảng "user"
    sql = "INSERT INTO user (   email, password, full_name, user_name, link_avatar, ip_register, device_register) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
    val = (
        email,
        hashed_password,
        full_name,
        user_name,
        link_avatar,
        ip_register,
        device_register,
    )
    mycursor.execute(sql, val)
    connection.commit()
    connection.close()


@app.route("/login", methods=["POST"])
def loginAccount():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    try:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()

        # Kiểm tra thông tin email trong cơ sở dữ liệu
        sql = "SELECT * FROM user WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        user_info = mycursor.fetchone()

        if user_info:
            # Verify the password using bcrypt
            hashed_password = user_info[2]  # The hashed password stored in the database
            if bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            ):
                user = {
                    "id_user": user_info[0],
                    "email": user_info[1],
                    "full_name": user_info[3],
                    "user_name": user_info[4],
                    "link_avatar": user_info[5],
                    "ip_register": user_info[6],
                    "device_register": user_info[7],
                }

                token_payload = {
                    "user_id": user["id_user"],
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(days=1),  # Thời gian hết hạn của token
                }
                token = jwt.encode(token_payload, YOUR_SECRET_KEY, algorithm="HS256")

                return {"ketqua": "Đăng nhập thành công!", "user": user, "token": token}
            else:
                return {"ketqua": "Email hoặc mật khẩu không đúng."}
        else:
            return {"ketqua": "Email hoặc mật khẩu không đúng."}

    except Exception as e:
        return {"ketqua": "Lỗi khi kết nối đến cơ sở dữ liệu."}


def authenticate_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
                token_payload = jwt.decode(token, YOUR_SECRET_KEY, algorithms=["HS256"])
                request.user_id = token_payload["user_id"]  # Thêm user_id vào request
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"ketqua": "Token đã hết hạn, vui lòng đăng nhập lại."}
            except jwt.InvalidTokenError:
                return {"ketqua": "Token không hợp lệ, vui lòng đăng nhập lại."}
        else:
            return {"ketqua": "Vui lòng cung cấp token trong tiêu đề Authorization."}

    return wrapper


@app.route("/resetpass", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    user_name = data.get("user_name")

    try:
        # Kiểm tra xem email và user_name có tồn tại trong cơ sở dữ liệu không
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()
        mycursor.execute(
            "SELECT * FROM user WHERE email = %s AND user_name = %s", (email, user_name)
        )
        account = mycursor.fetchone()
        mycursor.close()
        connection.close()

        if not account:
            return {"ketqua": "Email hoặc user_name không tồn tại trong hệ thống."}

        # Tạo mật khẩu mới ngẫu nhiên
        new_password = generate_random_password()

        # Cập nhật mật khẩu mới vào cơ sở dữ liệu
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()
        mycursor.execute(
            "UPDATE user SET password = %s WHERE email = %s AND user_name = %s",
            (new_password, email, user_name),
        )
        connection.commit()
        mycursor.close()
        connection.close()

        # Gửi email chứa mật khẩu mới đến người dùng
        send_email(email, new_password)

        return {
            "ketqua": "Đã gửi yêu cầu đặt lại mật khẩu. Vui lòng kiểm tra email để tạo mật khẩu mới."
        }

    except Exception as e:
        return {"ketqua": "Đã xảy ra lỗi khi thực hiện yêu cầu đặt lại mật khẩu."}


def generate_random_password():
    # Tạo mật khẩu ngẫu nhiên có 8 ký tự bằng cách sử dụng thư viện random
    letters = string.ascii_letters + string.digits + string.punctuation
    new_password = "".join(random.choice(letters) for i in range(8))
    return new_password


# gưi mail reset
def send_email(email, new_password):
    from_address = "nguyentienmanh181102@gmail.com"  # Thay bằng địa chỉ email của bạn
    password = "avsmfkqcjouesezo"  # Thay bằng mật khẩu email của bạn

    to_address = email
    subject = "Reset mật khẩu"

    # Nội dung email
    body = f"""
    Xin chào,

    Mật khẩu mới của bạn là: {new_password}

    Hãy sử dụng mật khẩu này để đăng nhập vào tài khoản của bạn.

    Trân trọng,
    Đội ngũ của chúng tôi
    """

    # Tạo đối tượng MIMEText
    msg = MIMEText(body, "plain")
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject

    # Kết nối đến máy chủ email và gửi email
    try:
        server = smtplib.SMTP(
            "smtp.gmail.com", 587
        )  # Thay bằng thông tin máy chủ email của bạn
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()

        return {"ketqua": "Đã gửi email chứa mật khẩu mới đến địa chỉ email của bạn."}
    except Exception as e:
        return {"ketqua": "Lỗi khi gửi email. Vui lòng thử lại sau."}


# đổi password
@app.route("/profile/change_password", methods=["POST"])
@authenticate_user
def change_password():
    id_user = request.user_id
    data = request.get_json()
    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    try:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()

        # Kiểm tra xem email và mật khẩu cũ có tồn tại trong cơ sở dữ liệu không
        sql = "SELECT * FROM user WHERE id_user = %s AND email = %s AND password = %s"
        val = (id_user, email, old_password)
        mycursor.execute(sql, val)
        user_info = mycursor.fetchone()
        if user_info:
            # Cập nhật mật khẩu mới vào cơ sở dữ liệu
            sql = "UPDATE user SET password = %s WHERE email = %s"
            val = (new_password, email)
            mycursor.execute(sql, val)
            connection.commit()
            mycursor.close()
            connection.close()
            return {"ketqua": "Đổi mật khẩu thành công!"}
        else:
            return {"ketqua": "Email hoặc mật khẩu cũ không đúng."}

    except Exception as e:
        return {"ketqua": "Đã xảy ra lỗi khi đổi mật khẩu."}


@app.route("/profile/<int:id_user>", methods=["GET"])
@authenticate_user
def get_user_profile(id_user):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn tất cả thông tin của các bản ghi trong bảng change_background
        query_change_background = "SELECT * FROM fakelocation_image WHERE id_user = %s ORDER BY created_at DESC"
        cursor.execute(query_change_background, (id_user,))
        change_background_records = cursor.fetchall()

        # Tạo danh sách các change_background đã tạo
        change_background_list = []
        for record in change_background_records:
            change_background_info = {
                "id_image": record[0],
                "imagegoc": record[1],
                "imagebackground": record[2],
                "linkImage": record[3],
                "categories": record[4],
                "location": record[5],
                "device_post_image": record[6],
                "ip_location_post": record[7],
                "id_user": record[8],
                "user_name": record[9],
                "created_at": record[10],
            }
            change_background_list.append(change_background_info)

        cursor.close()
        connection.close()
        return {"change_backgrounds": change_background_list}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


@app.route("/profile/change_avatar", methods=["PUT"])
@authenticate_user
def change_avatar():
    # Lấy thông tin từ request và thực hiện thay đổi link_avatar
    id_user = request.user_id  # Truy xuất user_id từ request
    data = request.get_json()
    link_avatar = data.get("link_avatar")

    # Kiểm tra user_id của token và thực hiện thay đổi link_avatar
    # ...
    try:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()

        # Update the link_avatar for the user with the given id_user
        sql = "UPDATE user SET link_avatar = %s WHERE id_user = %s"
        val = (link_avatar, id_user)
        mycursor.execute(sql, val)
        connection.commit()
        mycursor.close()
        connection.close()

        return {"ketqua": "Avatar updated successfully!"}
    except Exception as e:
        return {"ketqua": "Lỗi khi kết nối đến cơ sở dữ liệu."}


# tạo sự fakelocation
@app.route("/change_background", methods=["POST"])
@authenticate_user
def change_background():
    try:
        # imagegoc = request.headers.get("imagegoc")
        # imagebackground = request.headers.get("imagebackground")
        id_user = request.user_id

        data = request.get_json()  # Lấy dữ liệu JSON từ phần thân của yêu cầu

        imagegoc = data.get("imagegoc")
        imagebackground = data.get("imagebackground")
        categories = data.get("categories")
        location = data.get("location")
        device_post_image = data.get("device_post_image")
        ip_location_post = data.get("ip_location_post")

        print(imagegoc)
        print(imagebackground)
        linkSave1 = "linkgoc_" + get_random_string(8) + ".jpg"
        linkBackground = "link_background_" + get_random_string(8) + ".jpg"
        output_path = "ketqua_" + get_random_string(8) + ".jpg"
        print(linkSave1)
        print(linkBackground)
        download_image(imagegoc, linkSave1)
        download_image(imagebackground, linkBackground)
        change_bg = alter_bg(model_type="pb")
        change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
        change_bg.change_bg_img(
            f_image_path=linkSave1,
            b_image_path=linkBackground,
            output_image_name=output_path,
        )
        api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
        direct_link = upload_image_to_imgbb(output_path, api_key)
        os.remove(linkSave1)
        os.remove(linkBackground)
        os.remove(output_path)

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn thông tin người dùng từ bảng user dựa trên id_user
        query_user = "SELECT user_name FROM user WHERE id_user = %s"
        cursor.execute(query_user, (id_user,))
        user_info = cursor.fetchone()

        if user_info is None:
            return {"error": "User not found"}, 404

        user_name = user_info[0]

        query = "INSERT INTO fakelocation_image (imagegoc,imagebackground, linkImage,categories, location, device_post_image, ip_location_post, id_user, user_name) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            imagegoc,
            imagebackground,
            direct_link,
            categories,
            location,
            device_post_image,
            ip_location_post,
            id_user,
            user_name,
        )
        cursor.execute(query, values)

        # Lưu thay đổi vào cơ sở dữ liệu
        connection.commit()

        # Đóng kết nối
        cursor.close()
        connection.close()
        return {"linkreturn": direct_link}
    except Exception as e:
        return {"error": str(e)}, 500


# tìm kiếm sự kiện theo location
@app.route("/events_by_location", methods=["GET"])
def events_by_location():
    try:
        data = request.get_json()
        search_query = data.get("location")

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn danh sách sự kiện dựa trên vị trí
        query = "SELECT * FROM fakelocation_image WHERE location LIKE %s"
        cursor.execute(query, ("%" + search_query + "%",))
        events = cursor.fetchall()

        # Đóng kết nối
        cursor.close()
        connection.close()

        if not events:
            return {"message": "No events found for the given location"}, 404

        # Format dữ liệu và trả về kết quả
        formatted_events = []
        for event in events:
            formatted_event = {
                "id": event[0],
                "imagegoc": event[1],
                "imagebackground": event[2],
                "direct_link": event[3],
                "categories": event[4],
                "location": event[5],
                "device_post_image": event[6],
                "ip_location_post": event[7],
                "id_user": event[8],
                "user_name": event[9],
            }
            formatted_events.append(formatted_event)

        return {"events": formatted_events}
    except Exception as e:
        return {"error": str(e)}, 500


# get location được nhiều người chọn nhất
@app.route("/most_chosen_location", methods=["GET"])
def most_chosen_location():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Query to get the most chosen locations and their counts in descending order
        query_most_chosen_location = (
            "SELECT location, COUNT(location) AS location_count, "
            "MAX(categories) AS categories, MAX(imagebackground) AS imagebackground "
            "FROM fakelocation_image "
            "GROUP BY location "
            "ORDER BY location_count DESC"
        )

        cursor.execute(query_most_chosen_location)
        results = cursor.fetchall()

        if not results:
            return {"error": "No data found"}, 404

        # Create a list to store the results
        most_chosen_locations = []
        for location, location_count, categories, imagebackground in results:
            location_info = {
                "location": location,
                "location_count": location_count,
                "categories": categories,
                "imagebackground": imagebackground,
            }
            most_chosen_locations.append(location_info)

        cursor.close()
        connection.close()
        return {"most_chosen_locations": most_chosen_locations}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


@app.route("/_chosen_location", methods=["GET"])
def _chosen_location():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Query to get the most chosen locations and their counts in descending order
        query_most_chosen_location = (
            "SELECT location, "
            "SUBSTRING_INDEX(location, ',', -1) AS city, "
            "TRIM(SUBSTRING_INDEX(location, ',', 1)) AS country, "
            "COUNT(location) AS location_count, "
            "MAX(categories) AS categories, "
            "MAX(imagebackground) AS imagebackground "
            "FROM fakelocation_image "
            "GROUP BY location "
            "ORDER BY country, city, location_count DESC"
        )

        cursor.execute(query_most_chosen_location)
        results = cursor.fetchall()

        if not results:
            return {"error": "No data found"}, 404

        # Create a list to store the results
        most_chosen_locations = []
        for (
            location,
            city,
            country,
            location_count,
            categories,
            imagebackground,
        ) in results:
            location_info = {
                "location": location,
                "city": city,
                "country": country,
                "location_count": location_count,
                "categories": categories,
                "imagebackground": imagebackground,
            }
            most_chosen_locations.append(location_info)

        cursor.close()
        connection.close()
        return {"most_chosen_locations": most_chosen_locations}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# list ảnh theo các categories tương ứng với location
@app.route("/get_images_by_location_and_categories", methods=["GET"])
def get_images_by_location_and_categories():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Query to get the list of images grouped by locations and categories
        query_images_by_location_and_categories = (
            "SELECT location, "
            "SUBSTRING_INDEX(location, ',', -1) AS city, "
            "TRIM(SUBSTRING_INDEX(location, ',', 1)) AS country, "
            "categories, "
            "imagebackground "
            "FROM fakelocation_image "
            "ORDER BY country, city, categories"
        )

        cursor.execute(query_images_by_location_and_categories)
        images_info = cursor.fetchall()

        if not images_info:
            return jsonify({"error": "No images found"}), 404

        # Create a dictionary to store the images grouped by location and categories
        images_by_location_and_categories = {}
        for location, city, country, categories, imagebackground in images_info:
            key = f"{country} - {city}"
            if key not in images_by_location_and_categories:
                images_by_location_and_categories[key] = []
            image_info = {
                "location": location,
                "categories": categories,
                "imagebackground": imagebackground,
            }
            images_by_location_and_categories[key].append(image_info)

        cursor.close()
        connection.close()

        return jsonify(images_by_location_and_categories), 200
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# xem chi tiet fakelocation
@app.route("/change_background/<int:id_image>", methods=["GET"])
def get_change_background_by_id(id_image):
    return get_change_background(id_image)


def get_change_background(id_image):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn thông tin sự kiện dựa trên id_image
        query_change_background = "SELECT * FROM fakelocation_image WHERE id_image = %s"
        cursor.execute(query_change_background, (id_image,))
        change_background_info = cursor.fetchone()

        # Kiểm tra xem sự kiện có tồn tại hay không
        if not change_background_info:
            return {"error": "Change background not found"}, 404

        # Chuyển đổi kết quả từ tuple sang dictionary
        change_background_info_dict = {
            "id_image": change_background_info[0],
            "imagegoc": change_background_info[1],
            "imagebackground": change_background_info[2],
            "linkImage": change_background_info[3],
            "categories": change_background_info[4],
            "location": change_background_info[5],
            "device_post_image": change_background_info[6],
            "ip_location_post": change_background_info[7],
            "id_user": change_background_info[8],
            "user_name": change_background_info[9],
            "created_at": change_background_info[10],
        }

        cursor.close()
        connection.close()
        return change_background_info_dict
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# get tat ca các fakelocation
@app.route("/list_change_background", methods=["GET"])
def list_change_background():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn tất cả thông tin của các bản ghi trong bảng change_background
        query_change_background = (
            "SELECT * FROM fakelocation_image ORDER BY created_at DESC"
        )
        cursor.execute(query_change_background)
        change_background_records = cursor.fetchall()

        # Tạo danh sách các change_background đã tạo
        change_background_list = []
        for record in change_background_records:
            change_background_info = {
                "id_image": record[0],
                "imagegoc": record[1],
                "imagebackground": record[2],
                "linkImage": record[3],
                "categories": record[4],
                "location": record[5],
                "device_post_image": record[6],
                "ip_location_post": record[7],
                "id_user": record[8],
                "user_name": record[9],
                "created_at": record[10],
            }
            change_background_list.append(change_background_info)

        cursor.close()
        connection.close()
        return {"change_backgrounds": change_background_list}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# GET THEO so luong cmt
@app.route("/list_change_background_sorted_by_comment", methods=["GET"])
def list_change_background_sorted_by_comment():
    return jsonify(get_all_change_backgrounds_sorted_by_comment_count())


def get_all_change_backgrounds_sorted_by_comment_count():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn tất cả thông tin của các bản ghi trong bảng change_background
        query_change_background = (
            "SELECT f.*, COUNT(c.id_comment) AS comment_count FROM fakelocation_image AS f "
            "LEFT JOIN comment_image AS c ON f.id_image = c.id_image "
            "GROUP BY f.id_image "
            "ORDER BY comment_count DESC"
        )
        cursor.execute(query_change_background)
        change_background_records = cursor.fetchall()

        # Tạo danh sách các change_background đã tạo
        change_background_list = []
        for record in change_background_records:
            change_background_info = {
                "id_image": record[0],
                "imagegoc": record[1],
                "imagebackground": record[2],
                "linkImage": record[3],
                "categories": record[4],
                "location": record[5],
                "device_post_image": record[6],
                "ip_location_post": record[7],
                "id_user": record[8],
                "user_name": record[9],
                "created_at": record[10],
                "comment_count": record[11],  # Số lượng comment
            }
            change_background_list.append(change_background_info)

        cursor.close()
        connection.close()
        return change_background_list
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


@app.route("/delete_image/<int:id_image>", methods=["DELETE"])
@authenticate_user
def delete_image(id_image):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Kiểm tra xem sự kiện có tồn tại không trước khi xóa
        query_check_event = "SELECT id_user FROM fakelocation_image WHERE id_image = %s"
        cursor.execute(query_check_event, (id_image,))
        event_owner = cursor.fetchone()

        if event_owner is None:
            return {"error": "image not found"}, 404

        # Kiểm tra quyền truy cập của người dùng (chỉ người dùng sở hữu sự kiện mới có thể xóa)
        user_id = request.user_id
        if user_id != event_owner[0]:
            return {"error": "Unauthorized to delete this event"}, 401

        # Thực hiện xóa sự kiện
        query_delete_event = "DELETE FROM fakelocation_image WHERE id_image = %s"
        cursor.execute(query_delete_event, (id_image,))
        connection.commit()

        # Đóng kết nối
        cursor.close()
        connection.close()

        return {"message": "image_change deleted successfully"}

    except Exception as e:
        return {"error": str(e)}, 500


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
        # print(response.raw ,"****")
    del response


def upload_image_to_imgbb(image_path, api_key):
    # Tải dữ liệu ảnh
    with open(image_path, "rb") as file:
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }
    # Gửi yêu cầu POST tải lên ảnh đến API của ImgBB
    response = requests.post("https://api.imgbb.com/1/upload", payload)
    # Trích xuất đường dẫn trực tiếp đến ảnh từ JSON response
    json_data = json.loads(response.text)
    direct_link = json_data["data"]["url"]
    # Trả về đường dẫn trực tiếp đến ảnh
    return direct_link


@app.route("/post_comments", methods=["POST"])
@authenticate_user
def post_comments():
    try:
        id_user = request.user_id
        data = request.get_json()
        device_comment = data.get("device_comment")
        ip_comment = data.get("ip_comment")
        noidung_comment = data.get("noidung_comment")
        linkImage = data.get("linkImage")
        id_image = data.get("id_image")

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn thông tin người dùng từ bảng user dựa trên id_user
        query_user = "SELECT user_name FROM user WHERE id_user = %s"
        cursor.execute(query_user, (id_user,))
        user_info = cursor.fetchone()

        if user_info is None:
            return {"error": "User not found"}, 404

        user_name = user_info[0]

        insert_comment_query = "INSERT INTO comment_image (id_user, linkImage, ip_comment, device_comment, noidung_comment, id_image, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (
            id_user,
            linkImage,
            ip_comment,
            device_comment,
            noidung_comment,
            id_image,
            user_name,
        )
        cursor.execute(insert_comment_query, values)
        connection.commit()

        # Get the ID of the inserted comment
        comment_id = cursor.lastrowid

        # Retrieve the inserted comment details
        query_comment = "SELECT * FROM comment_image WHERE id_comment = %s"
        cursor.execute(query_comment, (comment_id,))
        comment_info = cursor.fetchone()

        comment = {
            "id_comment": comment_info[0],
            "id_user": comment_info[1],
            "linkImage": comment_info[2],
            "ip_comment": comment_info[3],
            "noidung_comment": comment_info[4],
            "id_image": comment_info[5],
            "user_name": comment_info[6],
            "device_comment": comment_info[7],
            "created_at": comment_info[8],
        }

        cursor.close()
        connection.close()
        return {"message": "cmt thành công", "comment": comment}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# lây all comment theo id_image
@app.route("/comments/<int:id_image>", methods=["GET"])
def get_comments_by_image_id(id_image):
    return jsonify(get_comments_by_image(id_image))


def get_comments_by_image(id_image):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn tất cả các comment dựa trên id_image
        query_comments = "SELECT * FROM comment_image WHERE id_image = %s"
        cursor.execute(query_comments, (id_image,))
        comments_records = cursor.fetchall()

        # Tạo danh sách các comment
        comments_list = []
        for record in comments_records:
            comment_info = {
                "id_comment": record[0],
                "id_user": record[1],
                "linkImage": record[2],
                "ip_comment": record[3],
                "noidung_comment": record[4],
                "id_image": record[5],
                "user_name": record[6],
                "device_comment": record[7],
                "create_at": record[8],
            }
            comments_list.append(comment_info)

        cursor.close()
        connection.close()
        return comments_list
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


@app.route("/delete_comment/<int:comment_id>", methods=["DELETE"])
@authenticate_user
def delete_comment(comment_id):
    try:
        id_user = request.user_id

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Kiểm tra xem comment có tồn tại và thuộc về người dùng hiện tại hay không
        query_comment = "SELECT id_user FROM comment_image WHERE id_comment = %s"
        cursor.execute(query_comment, (comment_id,))
        comment_info = cursor.fetchone()

        if comment_info is None:
            return {"error": "Comment not found"}, 404

        if comment_info[0] != id_user:
            return {"error": "You are not authorized to delete this comment"}, 403

        # Xóa comment
        delete_comment_query = "DELETE FROM comment_image WHERE id_comment = %s"
        cursor.execute(delete_comment_query, (comment_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return {"message": "Comment deleted successfully"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


@app.route("/list_new_users", methods=["GET"])
def list_new_users():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Truy vấn tất cả thông tin của người dùng mới đăng ký từ bảng user
        query_new_users = "SELECT * FROM user ORDER BY created_at DESC"
        cursor.execute(query_new_users)
        new_users = cursor.fetchall()

        # Tạo danh sách các người dùng mới đăng ký
        users_list = []
        for user in new_users:
            user_info = {
                "id_user": user[0],
                "email": user[1],
                "full_name": user[3],
                "user_name": user[4],
                "link_avatar": user[5],
                "ip_register": user[6],
                "device_register": user[7],
                "created_at": user[8],
            }
            users_list.append(user_info)

        cursor.close()
        connection.close()
        return {"new_users": users_list}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
