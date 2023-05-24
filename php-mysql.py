from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import base64
import json
# from docx import Document
# from docx.opc.constants import RELATIONSHIP_TYPE as RT
from flask_cors import CORS, cross_origin
import mysql.connector
from numpy import random
import base64
import hashlib

app = Flask(__name__)
cors = CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True # bat dinh dang file Json cua flask
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/lovehistory/<string:idLove>', methods=['GET'])
def getDataLoveHistory(idLove):
    print(idLove)
    thong_tin = {}
    list_thong_tin = []
    config = {
                'user': 'root',
                'password': 'password',
                'host': 'localhost',
                'port': 3306,
                'database': 'sonpro'
            }
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * from deptrai where id ={idLove}")
        result2 = mycursor.fetchall()
        print(result2)
        index_get_data = 0
        for i in range(0, 1):
            thong_tin["id"] = result2[i][0]

            thong_tin["name"] = result2[i][1]

            list_thong_tin.append(thong_tin)
            thong_tin = {}
            # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thong_tin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_thong_tin


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=19883)   
