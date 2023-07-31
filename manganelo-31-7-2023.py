from operator import or_
from urllib.parse import urlparse
from flask import Flask, jsonify, make_response, request, url_for
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
from flask_cors import CORS
import bcrypt
app = Flask(__name__)
CORS(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="ant3062003@gmail.com"
app.config['MAIL_PASSWORD']="tckkgibesnyxmppd"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['JWT_SECRET_KEY'] = 'devsenior'
app.config['SECURITY_PASSWORD_SALT'] = 'my_salt_value' 
jwt=JWTManager(app)
mail = Mail(app)
config = {
                'user': 'root',
                'password': 'mcso@123#@!',
                'host': '14.225.7.221',
                'port': 81,
                'database': 'huydong'
                }
# config = {
#                 'user': 'phpmyadmin',
#                 'password': 'password',
#                 'host': 'localhost',
#                 'port': 3306,
#                 'database': 'manga'
# }
#### API dki user
# kiem tra email dangki
s = URLSafeTimedSerializer('mysecretkey')
@app.route("/register", methods=["POST"])
def Create_account1():
    email = request.form.get('gmail_user')
    account_name = request.form.get('account_name')
    name_user = request.form.get('name_user')
    password_user = request.form.get('password_user')
    connection = mysql.connector.connect(**config)
    try:
        # connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Create_account1 where gmail_user=%s", (email,))
            user = cursor.fetchall()
            if not user:
                token = s.dumps({'email': email, 'account_name': account_name, 'name_user': name_user, 'password_user': password_user}, salt=app.config["SECURITY_PASSWORD_SALT"])
                msg = Message('Xác nhận tài khoản', sender=app.config['MAIL_USERNAME'], recipients=[email])
                link = url_for('confirm_email', token=token, _external=True)  # link đến route 'confirm_email'
                msg.body = "Your confirmation link is " + link
                mail.send(msg)
                message = {'status': 200, 'message': "Please check your email or spam"}

            else:
                message = {'status': 400, 'message': "Account or email already exists"}

            cursor.close()

    except Exception as e:
        print("Error while connecting to MySQL", e)
        message = {'status': 500, 'message': 'Error connecting to the database'}

    finally:
        
        if connection.is_connected():
            connection.close()

    return jsonify(message)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        data = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=300)  # max_age = 1 day
        email = data['email']
        account_name = data['account_name']
        name_user = data['name_user']
        password_user = data['password_user']

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM Create_account1 where gmail_user=%s", (email,))
                user = cursor.fetchall()
                if not user:
                    hashed_password = bcrypt.hashpw(password_user.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("INSERT INTO Create_account1 (name_account, name_user, password, gmail_user) VALUES (%s,%s,%s,%s)",
                                   (account_name, name_user, hashed_password, email))
                    connection.commit()
                    cursor.close()
                    message = {'status': 200, 'message': 'Account created and email confirmed. Please check your email or spam.'}
                else:
                    message = {'status': 400, 'message': 'Account or email already exists'}
        except Exception as e:
            print("Error while connecting to MySQL", e)
            message = {'status': 500, 'message': 'Error while adding account to the database'}

    except SignatureExpired:
        message = {'status': 400, 'message': 'The confirmation link is invalid or has expired.'}

    return jsonify(message)

    ####   API Đăng nhập tài khoản
def get_check(password_user,hashed_password):
    return bcrypt.checkpw(password_user.encode('utf-8'), hashed_password.encode('utf-8'))


@app.route("/login", methods=["GET"])
def get_login():
    email = request.form.get('gmail_user')
    password = request.form.get('password_user')
    # hashed_password = bcrypt.hashpw(password_user.encode('utf-8'), bcrypt.gensalt())
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM Create_account1 WHERE gmail_user = %s", (email,))
            result = cursor.fetchone()
            if result is not None and get_check(password,result[0]):
                data = 'Đăng nhập thành công.'
            else:
                data = 'Email hoặc mật khẩu không chính xác.'
        else:
            data = 'Không thể kết nối đến cơ sở dữ liệu.'
    except Exception as e:
        print("Error while connecting to MySQL", e)
        data = 'Lỗi khi kết nối đến cơ sở dữ liệu.'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return jsonify({"message": data})

 ####   API lay lai mat khau
@app.route("/forgot_pass", methods=["GET"])
def get_forgotpass():
    email = request.form.get('gmail_user')
    password_user = request.form.get('password_user')
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM Create_account1 WHERE gmail_user = %s", (email,))
            result = cursor.fetchone()
            if result[0] is not None:
                token = s.dumps({'email': email,  'password': password_user}, salt=app.config["SECURITY_PASSWORD_SALT"])
                msg = Message('Xác nhận tài khoản', sender=app.config['MAIL_USERNAME'], recipients=[email])
                link = url_for('confirm_account', token=token, _external=True)  # link đến route 'confirm_email'
                msg.body = "Your confirmation link is " + link
                mail.send(msg)
                data = {'status': 200, 'message': "Please check your email or spam"}
            else:
                data = 'Email không tồn tại'
        else:
            data = 'Không thể kết nối đến cơ sở dữ liệu.'
    except Exception as e:
        print("Error while connecting to MySQL", e)
        data = 'Lỗi khi kết nối đến cơ sở dữ liệu.'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return jsonify({"message": data})

@app.route('/confirm_account/<token>')
def confirm_account(token):
    try:
        data = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=300)
        email = data['email']
        password_user = data['password']
        hashed_password = bcrypt.hashpw(password_user.encode('utf-8'), bcrypt.gensalt())
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("UPDATE Create_account1 SET password=%s WHERE gmail_user=%s", (hashed_password, email))
                connection.commit()
                message = {'status': 200, 'message': 'Password reset successful'}
            else:
                message = {'status': 500, 'message': 'Lỗi kết nối đến cơ sở dữ liệu'}
        except Exception as e:
            print("Error while connecting to MySQL", e)
            message = {'status': 500, 'message': 'Lỗi khi thêm tài khoản vào cơ sở dữ liệu'}

    except SignatureExpired:
        message = {'status': 400, 'message': 'Liên kết xác nhận không hợp lệ hoặc đã hết hạn.'}

    return jsonify(message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    
    
