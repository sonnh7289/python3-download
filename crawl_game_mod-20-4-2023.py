from selenium import webdriver
from flask import Flask, jsonify, request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import json
from flask import Flask, session
from flask_session import Session
from flask import jsonify
from flask_restful import Api, Resource
# from utils.utils import beetoon_api
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time



# cấu hình driver
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--disk-cache=true')
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="D:\Intern\crawl_game\chromedriver")


# khởi tạo
global_var = []

app = Flask(__name__)

Session(app)
# duyệt dữ liệu để crawl
@app.route("/home/<int:index>",methods=["GET"])
def get_link(index):
    global global_var
    a_list_infos=[]
    info_page_game={}
    link = "https://an1.com/games/page/"+ str(index+1)
    driver.get(link)
   
    # đợi web load dữ liệu khi chuyển trang
    time.sleep(1)
    
    # dùng beautiful soup để lấy các thẻ a chứa đường dẫn tới trang download
    request = requests.get(link)
    soup = BeautifulSoup(request.text,'html.parser')
    
    div_tags = soup.find_all('div', class_="item")
    for a in div_tags:
        info_page_game["title"] = a.find('a',{'title': True}).get('title')
        info_page_game["link"]= a.find('a',{'title': True}).get('href')
        a_list_infos.append(info_page_game)
        info_page_game={}
    
    global_var = a_list_infos
    return jsonify(a_list_infos)


@app.route("/download/<int:index>", methods=["GET"])
def get_info_Game(index):   
    global global_var
    game_mod_info = {}
    # lấy link từ thẻ a để vào trang download
    a_list_info = global_var[index]
    
    el=a_list_info['link']
    driver.get(el)
    curl = driver.current_url
    driver.get(curl)
    
    # lấy ảnh screenshots
    request = requests.get(curl)
    soup = BeautifulSoup(request.text,'html.parser')
    
    img_urls =[]
    img_shots = soup.find('div', class_="app_screens_in")
    for img_shot in img_shots.find_all("img"):
        img_url = img_shot.get("src")
        img_urls.append(img_url)
        
    # dùng selenium tìm kiếm nút download
    el = driver.find_element(By.CLASS_NAME, "btn-lg")
    el.click()
        
    # lấy link trực tiếp để truy cập
    curl = driver.current_url
        
    # # chờ đợi trang web 15s để xuất hiện phần tử cần tìm
    wait = WebDriverWait(driver, 15)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-lg")))
        
    # sử dụng beautifulsoup để lấy các thuộc tính trang web
    request = requests.get(curl)
    soup = BeautifulSoup(request.text,'html.parser')
    
    # khai báo lại biến game_mod_info và game_mod_info
    game_mod_info['game_mod_name']=soup.find('h1').text
    game_mod_info['game_mod_img_icon']=soup.find('img').get('src')
    game_mod_info['game_mod_img_screenshots'] = img_urls
    game_mod_info['game_mod_link']=soup.find('a', class_="btn-lg").get('href')
    return jsonify(game_mod_info)
  
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=2888)
 