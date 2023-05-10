import base64
import json
import shutil
import string
from builtins import print, property, reversed, range, list
from calendar import prcal
from io import BytesIO
from os import link
from random import random

import mysql.connector
import requests
from PIL import Image
from PIL._imagingmath import mul_I
from _cffi_backend import string
from _dlib_pybind11 import points
import pymysql
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import cv2
import argparse

from nacl.utils import random
from numpy.core.defchararray import index
from tqdm import tqdm
from flask_cors import CORS
from yaml import load
from datetime import datetime
from face_detection import select_face, select_all_faces
from face_swap import face_swap
import random

app = Flask(__name__)
cors = CORS(app)

def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
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
@app.route('/hometh3', methods=['GET', 'POST'])
def index5():
    list_data = []
    index_demo = 0
    random_case =1
    ten_su_kien=[]
    print("random_case", random_case)
    array_direct = []
    if random_case==1:
        while (True):
            loaded = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
            # link_full3 = request.headers.get('Link_img3')
            # link_full4 = request.headers.get('Link_img4')
            # khởi tạo thanh tiến trình
            progress_bar = tqdm(total=55, unit="records")
            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")
            progress_bar.update(1)
            # print("process1 ",progress_bar)
            loaded["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            loaded["loaddata2"] = f'{progress_bar}'

            progress_bar.update(4)
            loaded["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            # download_image(link_full3, filename3)
            # download_image(link_full4, filename4)

            config = {
                'user': 'root',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'swapcouple'
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

                # mycursor1.execute("Select * from skhanhphuc")
                # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
                # print('maek', make_counter(8, 1))
                # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                # val = (link_full1, link_full2, link_full3, link_full4 )
                # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
                print(random_sukien[index_demo])
                loaded["tensukien"]=random_sukien[index_demo]
                rd=random.randint(1, 12)
                index_sk= [random.randint(1, 12) ,random.randint(1, 12) ,random.randint(1, 12) ,random.randint(1, 12) ,random.randint(1, 12),random.randint(1, 12)]
                print("index  sk " , index_sk[index_demo])
                print("index demosk " , index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                loaded["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                loaded["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                loaded["image wife"] = my_string2




                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2!="0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1!="0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                loaded["thongtin"] = my_string


                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()


                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    # if dst_faceBoxes2 is None:
                    #     print('Detect 0 Face !!!')
                    #     exit(-1)
                    # output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    # for k, dst_face2 in dst_faceBoxes2.items():
                    #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                    #                         args1)
                    # output_path2 = 'results/output2.jpg'
                    # cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'

                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'

                    api_key = "43e6acb9de376698edbf6301ccd2d5d9"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()



                if choose_case == 2:

                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #
                    # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                    #                            correct_color=False, no_debug_window=True)
                    # src_img2 = cv2.imread(args1.src)
                    # dst_img2 = cv2.imread(args1.dst)
                    # src_points2, src_shape2, src_face2 = select_face(src_img2)
                    # dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    # if dst_faceBoxes2 is None:
                    #     print('Detect 0 Face !!!')
                    #     exit(-1)
                    # output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    # for k, dst_face2 in dst_faceBoxes2.items():
                    #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                    #                         args1)
                    # output_path2 = 'results/output2.jpg'
                    # cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'

                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    # result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "43e6acb9de376698edbf6301ccd2d5d9"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()

                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)
                        progress_bar.update(6)
                        loaded["loaddata6"] = f'{progress_bar}'
                        print("process6 ", progress_bar)
                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2
                        progress_bar.update(7)
                        loaded["loaddata7"] = f'{progress_bar}'
                        print("process7 ", progress_bar)
                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)
                        progress_bar.update(8)
                        loaded["loaddata8"] = f'{progress_bar}'
                        # print("thanh cong ")
                        # image = cv2.imread('results/output1.jpg')
                        # print()
                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        progress_bar.update(9)
                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')
                        # image_1 = cv2.imread('results/output1.jpg')
                        # image_2 = cv2.imread('results/output2.jpg')
                        progress_bar.update(9)
                        loaded["loaddata9"] = f'{progress_bar}'
                        # print("image1",image_1.shape)
                        # print("image2",image_2.shape)

                        # ghép hai ảnh lại với nhau theo chiều ngang
                        # combined_img = cv2.hconcat([image_1, image_2])
                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # cv2.imshow('Combined Image', combined_img)
                        # cv2.imwrite(result_img, new_image)
                        # Return the output image
                        # return send_file(result_img, mimetype='image/jpeg')
                        api_key = "43e6acb9de376698edbf6301ccd2d5d9"
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        # loaded.append(direct_link)
                        loaded["Link_img"] = direct_link
                        progress_bar.update(10)
                        loaded["loaddata91=finish"] = f'{progress_bar}'
                        # print("process10 ", progress_bar)
                        progress_bar.close()

                        # index_demo += 1
                        # if index_demo == 5:
                        #     break
                        # print("index_demo", index_demo)
                        # return list_data
                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)
                        progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2
                        progress_bar.update(7)
                        loaded["loaddata7"] = f'{progress_bar}'
                        print("process7 ", progress_bar)
                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)
                        progress_bar.update(8)
                        loaded["loaddata8"] = f'{progress_bar}'
                        # print("thanh cong ")
                        # image = cv2.imread('results/output1.jpg')
                        # print()
                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        progress_bar.update(9)
                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')
                        # image_1 = cv2.imread('results/output1.jpg')
                        # image_2 = cv2.imread('results/output2.jpg')
                        progress_bar.update(9)
                        loaded["loaddata9"] = f'{progress_bar}'
                        # print("image1",image_1.shape)
                        # print("image2",image_2.shape)

                        # ghép hai ảnh lại với nhau theo chiều ngang
                        # combined_img = cv2.hconcat([image_1, image_2])
                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # cv2.imshow('Combined Image', combined_img)
                        # cv2.imwrite(result_img, new_image)
                        # Return the output image
                        # return send_file(result_img, mimetype='image/jpeg')
                        api_key = "43e6acb9de376698edbf6301ccd2d5d9"
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        # loaded.append(direct_link)
                        loaded["Link_img"] = direct_link
                        progress_bar.update(10)
                        loaded["loaddata91=finish"] = f'{progress_bar}'
                        # print("process10 ", progress_bar)
                        progress_bar.close()
                if choose_case == 4:
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'

                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'

                    result_img = 'results/output.jpg'

                    api_key = "43e6acb9de376698edbf6301ccd2d5d9"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link

                    progress_bar.close()

                array_direct.append(direct_link)
                list_data.append(loaded)

                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)

                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
                # mycursor1.execute("Select thongtin from skhanhphuc")x

                # connection.commit()



                loaded["thongtin"] = my_string




                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
            # mycursor1.execute("Select thongtin from skhanhphuc")x
            # connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")

            # return loaded

            index_demo += 1
            if index_demo == 6:
                break


            print("direct link" , direct_link)

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor()
            # mycursor1.execute("Select * from skhanhphuc")
            # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
            # print('maek', make_counter(8, 1))
            # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            # val = (link_full1, link_full2, link_full3, link_full4 )
            # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

            mycursor.execute(f"SELECT MAX(id_case) from case2")
            result2 = mycursor.fetchall()



            sql = f"INSERT INTO case2 (skchiatay ,sknym , skhanhphuc ,skkethon , skmuasam , sklyhon , id_case) VALUES (%s, %s , %s ,%s ,%s  , %s ,{result2[0][0]+1} )"
            val = (list_data[0]["thongtin"], list_data[1]["thongtin"],list_data[2]["thongtin"],list_data[3]["thongtin"],list_data[4]["thongtin"] , list_data[5]["thongtin"])
            mycursor.execute(sql, val)
            result1 = mycursor.fetchall()

            sql = f"INSERT INTO ketquaswap (swapct ,swapnym , swaphp ,swapkh , swapms , swaplyhon , id_swap) VALUES (%s, %s , %s ,%s ,%s  , %s ,{result2[0][0] + 1 })"
            val = (array_direct[0] , array_direct[1]  ,array_direct[2] ,array_direct[3]  ,array_direct[4] ,array_direct[5] )
            mycursor.execute(sql, val)
            result1 = mycursor.fetchall()

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
            # mycursor1.execute("Select thongtin from skhanhphuc")x
            # connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return list_data
    if random_case==2:
        while (True):
            loaded = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
            # link_full3 = request.headers.get('Link_img3')
            # link_full4 = request.headers.get('Link_img4')
            # khởi tạo thanh tiến trình
            progress_bar = tqdm(total=55, unit="records")
            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")
            progress_bar.update(1)
            # print("process1 ",progress_bar)
            loaded["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            loaded["loaddata2"] = f'{progress_bar}'
            # if (link_full3[0:19] == 'https://github.com/'):
            #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full3:
            #         link_full3 = link_full3.replace("blob/", '')
            #     if "/main" in link_full3:
            #         link_full3 = link_full3.replace("/raw/", "/")
            # progress_bar.update(3)
            # loaded["loaddata3"] = f'{progress_bar}'
            # if (link_full4[0:19] == 'https://github.com/'):
            #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full4:
            #         link_full4 = link_full4.replace("blob/", '')
            #     if "/main" in link_full4:
            #         link_full4 = link_full4.replace("/raw/", "/")

            progress_bar.update(4)
            loaded["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            # download_image(link_full3, filename3)
            # download_image(link_full4, filename4)

            config = {
                'user': 'root',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'swapcouple'
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
                mycursor1 = connection.cursor()
                # mycursor1.execute("Select * from skhanhphuc")
                # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
                # print('maek', make_counter(8, 1))
                # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                # val = (link_full1, link_full2, link_full3, link_full4 )
                # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
                random_sk = random.choice(random_sukien)
                print(random_sk)
                index_sk = random.randint(1, 12)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                loaded["image couple"] = my_string12
                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                loaded["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                loaded["image wife"] = my_string2
                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0":
                    choose_case = 2
                    download_image(my_string1, filename3)

                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                loaded["thongtin"] = my_string
                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()

                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
                # mycursor1.execute("Select thongtin from skhanhphuc")x
                # connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")

            list_data.append(loaded)
            # return loaded

            index_demo += 1
            if index_demo == 6:
                break
            print("index_demo", index_demo)
        return list_data
    if random_case==3:
        while (True):
            loaded = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
            # link_full3 = request.headers.get('Link_img3')
            # link_full4 = request.headers.get('Link_img4')
            # khởi tạo thanh tiến trình
            progress_bar = tqdm(total=55, unit="records")
            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")
            progress_bar.update(1)
            # print("process1 ",progress_bar)
            loaded["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            loaded["loaddata2"] = f'{progress_bar}'
            # if (link_full3[0:19] == 'https://github.com/'):
            #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full3:
            #         link_full3 = link_full3.replace("blob/", '')
            #     if "/main" in link_full3:
            #         link_full3 = link_full3.replace("/raw/", "/")
            # progress_bar.update(3)
            # loaded["loaddata3"] = f'{progress_bar}'
            # if (link_full4[0:19] == 'https://github.com/'):
            #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full4:
            #         link_full4 = link_full4.replace("blob/", '')
            #     if "/main" in link_full4:
            #         link_full4 = link_full4.replace("/raw/", "/")

            progress_bar.update(4)
            loaded["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            # download_image(link_full3, filename3)
            # download_image(link_full4, filename4)

            config = {
                'user': 'root',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'swapcouple'
            }

            def make_counter(start, step):
                count = start

                def counter():
                    nonlocal count
                    result = count
                    count += step
                    return result

                return counter

            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                mycursor1 = connection.cursor()
                # mycursor1.execute("Select * from skhanhphuc")
                # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
                # print('maek', make_counter(8, 1))
                # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                # val = (link_full1, link_full2, link_full3, link_full4 )
                # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

                # mycursor.execute(sql, val)
                random_sukien = ['skhanhphuc', 'skkethon', 'skmuasam']
                random_sk = random.choice(random_sukien)
                print(random_sk)
                index_sk = random.randint(1, 12)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                loaded["image couple"] = my_string12
                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                loaded["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                loaded["image wife"] = my_string2


                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0":
                    choose_case = 2
                    download_image(my_string1, filename3)

                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                loaded["thongtin"] = my_string
                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()

                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
                # mycursor1.execute("Select thongtin from skhanhphuc")x
                # connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")

            list_data.append(loaded)
                # return loaded

            index_demo += 1
            if index_demo == 3:
                break
            print("index_demo", index_demo)
        return list_data

@app.route('/getid', methods=['GET', 'POST'])
def getid():
    id = request.headers.get('id')
    print("id" , id)
    thongtin={}
    config = {
        'user': 'root',
        'password': 'BAdong14102001!',
        'host': 'localhost',
        'port': 3306,
        'database': 'swapcouple'
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
        # mycursor1.execute("Select * from skhanhphuc")
        # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
        # print('maek', make_counter(8, 1))
        # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        # val = (link_full1, link_full2, link_full3, link_full4 )
        # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"


        mycursor.execute(f"SELECT skchiatay from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["skchiatay"] = my_string

        mycursor.execute(f"SELECT sknym from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["sknym"] = my_string

        mycursor.execute(f"SELECT skhanhphuc from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["skhanhphuc"] = my_string

        mycursor.execute(f"SELECT skkethon from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["skkethon"] = my_string

        mycursor.execute(f"SELECT skkethon from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["skkethon"] = my_string

        mycursor.execute(f"SELECT skmuasam from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["skmuasam"] = my_string

        mycursor.execute(f"SELECT sklyhon from case2 where id_case={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["sklyhon"] = my_string

        #swap image
        mycursor.execute(f"SELECT swapct from ketquaswap where id_swap={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["swapct"] = my_string

        mycursor.execute(f"SELECT swapnym from ketquaswap where id_swap={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["swapnym"] = my_string

        mycursor.execute(f"SELECT swaphp from ketquaswap where id_swap={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["swaphp"] = my_string

        mycursor.execute(f"SELECT swapms from ketquaswap where id_swap={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["swapms"] = my_string

        mycursor.execute(f"SELECT swapkh from ketquaswap where id_swap={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["swapkh"] = my_string

        mycursor.execute(f"SELECT swaplyhon from ketquaswap where id_swap={id}")
        result2 = mycursor.fetchall()
        my_string = ', '.join(result2[0])
        print('mystring', my_string)
        thongtin["swaplyhon"] = my_string




        # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thongtin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thongtin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return thongtin
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
