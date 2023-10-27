
import mysql.connector
import datetime
import re
from typing import Union, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import binascii
import os
from postmarker.core import PostmarkClient
from datetime import datetime, timedelta
from datetime import timedelta
binascii.hexlify(os.urandom(24))
app = FastAPI()


config = {
                'user': 'sammy',
                'password': 'Thinkdiff123!!',
                'host': 'localhost',
                'port': 3306,
                'database': 'FutureLove4'
                # 'auth_plugin': 'mysql_native_password'
            }

sender = 'admin@datanomic.online'
postmark_api = 'afed6e53-a372-4319-b08f-b8eba39c4b40'
SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = 'fbhe3hf839vbiwvc9wh30fbweocboeuwefiwehfwf9bvsfw9'
# binascii.hexlify(os.urandom(24))

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

async def send_mail(email, link):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject='FutureLove Account Register - Generate Images With AI',
        HtmlBody=f'Hi FutureLove User, \n You recently requested to open your FutureLove account. Use the button below to confirmation. This active link only valid for the next 24 hours. \n Active account \n For security, this request was received from a operating_system_Value device using browser_name_Value. If you did not request open account, please ignore this email or contact support if you have questions. \n Thanks, \n The product_name_Value Team \n If you’re having trouble with the button above, copy and paste the URL below into your web browser. action_url_Value {link}'
    )

async def send_mail_reset(email, password_new):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject='FutureLove Account Register - Generate Images With AI',
        HtmlBody=f'Your new password is: {password_new}'
    )

async def send_mail_notifi(email, message):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject='FutureLove Account Register - Generate Images With AI',
        HtmlBody= message
    )

async def send_mail_del_account(email, message):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject='FutureLove Account Register - Generate Images With AI',
        HtmlBody= message
    )


def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 30  # Expired after 3 days
    )
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt

def verify_password(username, password):
        thong_tin = {}
        try:
            connection= mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor(buffered=True)
                query = "SELECT * FROM user WHERE user_name = %s OR email = %s"
                values = (username, username)
                cursor.execute(query, values)
                user = cursor.fetchall()

                if user[0][5] == password:
                    thong_tin["id_user"] = user[0][0]
                    thong_tin["link_avatar"] = user[0][1]
                    thong_tin["user_name"] = user[0][2]
                    thong_tin["ip_register"] = user[0][3]
                    thong_tin["device_register"] = user[0][4]
                    thong_tin["email"] = user[0][6]
                    thong_tin["count_sukien"] = int(user[0][7])
                    thong_tin["count_comment"] = int(user[0][8])
                    thong_tin["count_view"] = int(user[0][9])
                    # thong_tin["cover_pic"] = user[0][10]
                    return thong_tin
                else:
                    return thong_tin
        except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
        finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")

abc = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ1MDM0MzksInVzZXJuYW1lIjoiMjAwMjEzODhAdm51LmVkdS52biJ9.BoQtteOqGdTPhvapWQg3YZAAzzom1DPAQusVLsWcoTk'

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        print(payload)
        expiration_time = payload.get('exp')
        current_time = datetime.now().timestamp()
        if expiration_time < current_time:
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )




async def save_user_to_mysql(user_name , password, email,link_avatar,ip_register,device_register ):
        try:
            connection= mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor(buffered=True)
                mycursor.execute(f"SELECT MAX(id_user) from user")
                max_id_user = mycursor.fetchone()[0]
                id_user = max_id_user + 1
                count_sk = 0
                count_view = 0
                count_comment = 0
                sql = f"INSERT INTO user (id_user , user_name , password, email ,link_avatar , ip_register , device_register, count_sukien, count_comment, count_view) VALUES ( {id_user} , %s, %s, %s, %s, %s , %s, {count_sk}, {count_view}, {count_comment} )"
                val = (user_name, password, email, link_avatar, ip_register, device_register)
                mycursor.execute(sql, val)
                connection.commit()
        except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
        finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")




