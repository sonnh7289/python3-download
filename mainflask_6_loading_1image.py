import base64
import json
import shutil
import string
from builtins import print
from calendar import prcal
from io import BytesIO
from os import link

import requests
from PIL import Image
from _dlib_pybind11 import points
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import cv2
import argparse
from tqdm import tqdm
from flask_cors import CORS
from yaml import load

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

@app.route('/home', methods=['GET', 'POST'])
def index():
    loaded={}
    link_full1 = request.headers.get('Link_img1')
    link_full2 = request.headers.get('Link_img2')
    link_full3 = request.headers.get('Link_img3')
    link_full4 = request.headers.get('Link_img4')
    # khởi tạo thanh tiến trình
    progress_bar = tqdm(total=55, unit ="records")
    if (link_full1[0:19] == 'https://github.com/'):
        link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full1:
            link_full1 = link_full1.replace("blob/", '')
        if "/main" in link_full1:
            link_full1 = link_full1.replace("/raw/", "/")
    progress_bar.update(1)
    # print("process1 ",progress_bar)
    loaded["loaddata1"]=f'{progress_bar}'
    if(link_full2[0:19]=='https://github.com/'):
        link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full2:
            link_full2 = link_full2.replace("blob/", '')
        if "/main" in link_full2:
            link_full2=link_full2.replace("/raw/","/")
    progress_bar.update(2)
    loaded["loaddata2"] = f'{progress_bar}'
    if (link_full3[0:19] == 'https://github.com/'):
        link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full3:
            link_full3 = link_full3.replace("blob/", '')
        if "/main" in link_full3:
            link_full3 = link_full3.replace("/raw/", "/")
    progress_bar.update(3)
    loaded["loaddata3"] = f'{progress_bar}'
    if (link_full4[0:19] == 'https://github.com/'):
        link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full4:
            link_full4 = link_full4.replace("blob/", '')
        if "/main" in link_full4:
            link_full4 = link_full4.replace("/raw/", "/")

    progress_bar.update(4)
    loaded["loaddata4"] = f'{progress_bar}'
    filename1 = 'imgs/anhtam1.jpg'
    filename2 = 'imgs/anhtam2.jpg'
    filename3 = 'imgs/anhtam3.jpg'
    filename4 = 'imgs/anhtam4.jpg'
    download_image(link_full1, filename1)
    download_image(link_full2, filename2)
    download_image(link_full3, filename3)
    download_image(link_full4, filename4)
    # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("download thanh cong")
    # download_image(link_full3 , filename3)
    #rescale image

    # img_scale = Image.open("imgs/anhtam1.jpg")
    # print("hihia")
    # img_scale = Image.open(BytesIO(response.content))

    # new_image = img_scale.resize((500, 700))
    # new_image.save('imgs/example_resized1.jpg')
    #
    #
    # img_scale1 = Image.open("imgs/anhtam2.jpg")
    # new_image1 = img_scale1.resize((500, 700))
    # new_image1.save('imgs/example_resized2.jpg')
    progress_bar.update(5)
    loaded["loaddata5"] = f'{progress_bar}'
    # return f"{progress_bar}"
    # # Get the uploaded files
    # src_file = request.files['src']
    # dst_file = request.files['dst']
    # from_file=request.files['from']
    # my_list=[src_file , dst_file]
    # val=random.choice(my_list)
    # print(val)
    # Save the uploaded files to disk
    # src_path =  'imgs/src_img1.jpg'
    # dst_path =  'imgs/src_img2.jpg'
    # from_path=  'imgs/couple.jpg'
    # val.save(src_path)
    # src_file.save(src_path)
    # dst_file.save(dst_path)
    # from_file.save(from_path)

    # open image
    # index=0
    # img = Image.open("imgs/anhtam3.jpg")
    # # new_image = img.resize((500, 500))
    # # new_image.save('example_resized.jpg')
    # # lấy kích thước ảnh
    # width, height = img.size
    #
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped1 = img.crop((0, 0, width//2 -40, height))
    # # lưu ảnh đã cắt
    # img_cropped1.save("imgs/img_1.jpg")
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped2 = img.crop((width//2-40, 0, width, height))
    # # lưu ảnh đã cắt
    # img_cropped2.save("imgs/img_2.jpg")

    # Swap faces
    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg', warp_2d=False, correct_color=False, no_debug_window=True)
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)
    src_points, src_shape, src_face = select_face(src_img)
    dst_faceBoxes = select_all_faces(dst_img)


    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False, correct_color=False, no_debug_window=True)
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
        exit(-1)
    output = dst_img

    if dst_faceBoxes2 is None:
        print('Detect 0 Face !!!')
        exit(-1)
    output2 = dst_img2
    progress_bar.update(7)
    loaded["loaddata7"] = f'{progress_bar}'
    print("process7 ", progress_bar)
    for k, dst_face in dst_faceBoxes.items():
        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output, args)
    output_path = 'results/output1.jpg'
    cv2.imwrite(output_path, output)


    for k, dst_face2 in dst_faceBoxes2.items():
        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2, args1)
    output_path2 = 'results/output2.jpg'
    cv2.imwrite(output_path2, output2)
    progress_bar.update(8)
    loaded["loaddata8"] = f'{progress_bar}'
    # print("thanh cong ")
    # image = cv2.imread('results/output1.jpg')
    # print()
    image_1 = cv2.imread('results/output1.jpg')
    image_2 = cv2.imread('results/output2.jpg')
    imgOpen = Image.open("results/output1.jpg") #SONPIPI
    imgOpen_2 = Image.open("results/output2.jpg")
    width_output1, height_output1 = imgOpen.size
    # # cắt lấy nửa ảnh đầu trên
    img_cropped2 = imgOpen_2.crop((0, 0, width_output1, height_output1))
    img_cropped2.save("results/output2_fix_size.jpg")
    image_Load_cropped2 = cv2.imread('results/output2_fix_size.jpg')
    #________________END_SONPIPI___
    progress_bar.update(9)
    loaded["loaddata9"] = f'{progress_bar}'
    # print("image1",image_1.shape)
    # print("image2",image_2.shape)

    # ghép hai ảnh lại với nhau theo chiều ngang
    combined_img = cv2.hconcat([image_1, image_Load_cropped2])
    result_img='results/output.jpg'
    # hiển thị ảnh đã ghép
    # cv2.imshow('Combined Image', combined_img)
    cv2.imwrite(result_img, combined_img)
    # Return the output image
    # return send_file(result_img, mimetype='image/jpeg')
    api_key = "fd81b5da86e162ade162a05220c0eb89"
    direct_link = upload_image_to_imgbb(result_img, api_key)
    # loaded.append(direct_link)
    loaded["Link_img"]=direct_link
    progress_bar.update(10)
    loaded["loaddata91=finish"]=f'{progress_bar}'
    # print("process10 ", progress_bar)
    progress_bar.close()
    return loaded

@app.route('/homev1', methods=['GET', 'POST'])
def index1():
    loaded={}
    link_full1 = request.headers.get('Link_img1')
    link_full2 = request.headers.get('Link_img2')
    # link_full3 = request.headers.get('Link_img3')
    # link_full4 = request.headers.get('Link_img4')
    # khởi tạo thanh tiến trình
    progress_bar = tqdm(total=55, unit ="records")
    if (link_full1[0:19] == 'https://github.com/'):
        link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full1:
            link_full1 = link_full1.replace("blob/", '')
        if "/main" in link_full1:
            link_full1 = link_full1.replace("/raw/", "/")
    progress_bar.update(1)
    # print("process1 ",progress_bar)
    loaded["loaddata1"]=f'{progress_bar}'
    if(link_full2[0:19]=='https://github.com/'):
        link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full2:
            link_full2 = link_full2.replace("blob/", '')
        if "/main" in link_full2:
            link_full2=link_full2.replace("/raw/","/")
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
    # filename3 = 'imgs/anhtam3.jpg'
    # filename4 = 'imgs/anhtam4.jpg'
    download_image(link_full1, filename1)
    download_image(link_full2, filename2)
    # download_image(link_full3, filename3)
    # download_image(link_full4, filename4)
    # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("download thanh cong")
    # download_image(link_full3 , filename3)
    #rescale image

    # img_scale = Image.open("imgs/anhtam1.jpg")
    # print("hihia")
    # img_scale = Image.open(BytesIO(response.content))

    # new_image = img_scale.resize((500, 700))
    # new_image.save('imgs/example_resized1.jpg')
    #
    #
    # img_scale1 = Image.open("imgs/anhtam2.jpg")
    # new_image1 = img_scale1.resize((500, 700))
    # new_image1.save('imgs/example_resized2.jpg')
    progress_bar.update(5)
    loaded["loaddata5"] = f'{progress_bar}'
    # return f"{progress_bar}"
    # # Get the uploaded files
    # src_file = request.files['src']
    # dst_file = request.files['dst']
    # from_file=request.files['from']
    # my_list=[src_file , dst_file]
    # val=random.choice(my_list)
    # print(val)
    # Save the uploaded files to disk
    # src_path =  'imgs/src_img1.jpg'
    # dst_path =  'imgs/src_img2.jpg'
    # from_path=  'imgs/couple.jpg'
    # val.save(src_path)
    # src_file.save(src_path)
    # dst_file.save(dst_path)
    # from_file.save(from_path)

    # open image
    # index=0
    # img = Image.open("imgs/anhtam3.jpg")
    # # new_image = img.resize((500, 500))
    # # new_image.save('example_resized.jpg')
    # # lấy kích thước ảnh
    # width, height = img.size
    #
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped1 = img.crop((0, 0, width//2 -40, height))
    # # lưu ảnh đã cắt
    # img_cropped1.save("imgs/img_1.jpg")
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped2 = img.crop((width//2-40, 0, width, height))
    # # lưu ảnh đã cắt
    # img_cropped2.save("imgs/img_2.jpg")

    # Swap faces
    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam2.jpg', out='results/output1.jpg', warp_2d=False, correct_color=False, no_debug_window=True)
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)
    src_points, src_shape, src_face = select_face(src_img)
    dst_faceBoxes = select_all_faces(dst_img)


    # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False, correct_color=False, no_debug_window=True)
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
        exit(-1)
    output = dst_img

    # if dst_faceBoxes2 is None:
    #     print('Detect 0 Face !!!')
    #     exit(-1)
    # output2 = dst_img2
    progress_bar.update(7)
    loaded["loaddata7"] = f'{progress_bar}'
    print("process7 ", progress_bar)
    for k, dst_face in dst_faceBoxes.items():
        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output, args)
    output_path = 'results/output1.jpg'
    cv2.imwrite(output_path, output)


    # for k, dst_face2 in dst_faceBoxes2.items():
    #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2, args1)
    # output_path2 = 'results/output2.jpg'
    # cv2.imwrite(output_path2, output2)
    progress_bar.update(8)
    loaded["loaddata8"] = f'{progress_bar}'
    # print("thanh cong ")
    # image = cv2.imread('results/output1.jpg')
    # print()
    # image_1 = cv2.imread('results/output1.jpg')
    # image_2 = cv2.imread('results/output2.jpg')
    # progress_bar.update(9)
    # loaded["loaddata9"] = f'{progress_bar}'
    # # print("image1",image_1.shape)
    # # print("image2",image_2.shape)
    #
    # # ghép hai ảnh lại với nhau theo chiều ngang
    # combined_img = cv2.hconcat([image_1, image_2])
    result_img='results/output1.jpg'
    # # hiển thị ảnh đã ghép
    # cv2.imshow('Combined Image', combined_img)
    # cv2.imwrite(result_img, combined_img)
    # Return the output image
    # return send_file(result_img, mimetype='image/jpeg')
    api_key = "fd81b5da86e162ade162a05220c0eb89"
    direct_link = upload_image_to_imgbb(result_img, api_key)
    # loaded.append(direct_link)1
    loaded["Link_img"]=direct_link
    progress_bar.update(10)
    loaded["loaddata91=finish"]=f'{progress_bar}'
    # print("process10 ", progress_bar)
    progress_bar.close()
    return loaded

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port =2663)