import argparse

import cv2
from flask import request, jsonify
import mysql.connector
from numpy import random
from face_detection import select_face, select_all_faces
from face_swap import face_swap

import random
from PIL import Image
from datetime import datetime
from tqdm import tqdm
import base64
import json
import shutil

import requests
from flask import Flask
from flask_cors import CORS

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


@app.route('/getdata', methods=['GET', 'POST'])
def index5():
    list_return_data = []
    index_demo = 0
    random_case = 1

    array_direct = []
    get_id_js = []
    print("random_case", random_case)
    if random_case == 1:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
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
                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 12)
                index_sk = [random.randint(1, 12), random.randint(1, 12), random.randint(1, 12), random.randint(1, 12),
                            random.randint(1, 12), random.randint(1, 12)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

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
                item1SuKien["image couple"] = my_string12

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
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
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

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

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

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

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

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

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

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id"] = result2[0][0]
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
    if random_case == 2:
        while (True):
            item1SuKien = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
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
            item1SuKien["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            item1SuKien["loaddata2"] = f'{progress_bar}'

            progress_bar.update(4)
            item1SuKien["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)

            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
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
                item1SuKien["image couple"] = my_string12
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
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2
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
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")

            list_return_data.append(item1SuKien)

            index_demo += 1
            if index_demo == 6:
                break
            print("index_demo", index_demo)
        return list_return_data
    if random_case == 3:
        while (True):
            item1SuKien = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
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
            item1SuKien["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            item1SuKien["loaddata2"] = f'{progress_bar}'

            progress_bar.update(4)
            item1SuKien["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)

            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
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
                item1SuKien["image couple"] = my_string12
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
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

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

                item1SuKien["thongtin"] = my_string
                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            list_return_data.append(item1SuKien)
            index_demo += 1
            if index_demo == 3:
                break
            print("index_demo", index_demo)
        return list_return_data
#________SONPIPI________17-5-2023_____
@app.route('/lovehistory/all', methods=['GET'])
def getDataLoveHistory():
    list_toan_bo_sukien_saved = []
    config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
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
        mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
        PhanTuMax = mycursor.fetchall()
        soPhanTu = PhanTuMax[0][0]   
        for idItemPhanTu in range(0, soPhanTu):
            Mot_LanQuerryData = []
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={idItemPhanTu}")
            result2 = mycursor.fetchall()
            print(result2)
            index_get_data = 0
            thong_tin = {}
            for i in range(0, 6):
                thong_tin["id"] = result2[i][0]
                thong_tin["link_nam_goc"] = result2[i][1]
                thong_tin["link_nu_goc"] = result2[i][2]
                thong_tin["link_nam_chua_swap"] = result2[i][3]
                thong_tin["link_nu_chua_swap"] = result2[i][4]
                thong_tin["link_da_swap"] = result2[i][5]
                thong_tin["real_time"] = result2[i][6]
                thong_tin["ten_su_kien"] = result2[i][7]
                thong_tin["noi_dung_su_kien"] = result2[i][8]
                thong_tin["so_thu_tu_su_kien"] = result2[i][10]
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}
            list_toan_bo_sukien_saved.append(Mot_LanQuerryData)
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
    return list_toan_bo_sukien_saved

@app.route('/lovehistory/<string:idLove>', methods=['GET'])
def getDataLoveHistory(idLove):
    print(idLove)
    thong_tin = {}
    list_thong_tin = []
    config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
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

        mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={idLove}")
        result2 = mycursor.fetchall()
        print(result2)
        index_get_data = 0
        for i in range(0, 6):
            thong_tin["id"] = result2[i][0]

            thong_tin["link_nam_goc"] = result2[i][1]

            thong_tin["link_nu_goc"] = result2[i][2]

            thong_tin["link_nam_chua_swap"] = result2[i][3]

            thong_tin["link_nu_chua_swap"] = result2[i][4]

            thong_tin["link_da_swap"] = result2[i][5]

            thong_tin["real_time"] = result2[i][6]

            thong_tin["ten_su_kien"] = result2[i][7]

            thong_tin["noi_dung_su_kien"] = result2[i][8]

            thong_tin["so_thu_tu_su_kien"] = result2[i][10]

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)
