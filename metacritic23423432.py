import numpy as np
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import json
from bs4 import BeautifulStoneSoup as BS
from selenium.webdriver.common.by import By
import random
import  pandas as pd

driver=webdriver.Chrome(executable_path=r'chromedriver.exe')
# tạo vòng lặp
index=0
list_data=[]
while True:
    # gán link
    link_base = driver.get(f'https://www.metacritic.com/browse/movies/release-date/theaters/date?page={index}')
    # để mở 5s thì đóng
    sleep(5)
    # giá trị trang thay đổi n+1
    index +=1
    # Tìm tất cả các thẻ <img> trên trang
    get_img_data = driver.find_elements(By.CSS_SELECTOR , "img")
    # Lặp qua tất cả các hình ảnh và lấy các đường dẫn
    for item_get_img_data in get_img_data:
        data_model={}
        data_model['data_img']=item_get_img_data.get_attribute("src")
        data_model['data_name']=item_get_img_data.get_attribute("alt")
        data_model['data_time']=item_get_img_data.get_attribute("span")
        list_data.append(data_model)

    print(get_img_data)
    # biến đến 3 
    if index ==3:
        
        break

        # chạy vào file json
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(list_data, outfile)

