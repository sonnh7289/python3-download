from coinApp import get_coin_snap
from configparser import ConfigParser
import ast
import os
from PIL import Image

config = ConfigParser()
config.read(r"D:\DevSenior_Training\coin_detection\coin_recognize\config.ini")

i_path = ast.literal_eval(config['TEST']['test_path'])

b_img = os.path.join(i_path, "backside.jpg")
b_image = Image.open(b_img)

f_img = os.path.join(i_path, "frontside.jpg")
f_image = Image.open(f_img)

predict_img = get_coin_snap(b_image, f_image)
print(predict_img)