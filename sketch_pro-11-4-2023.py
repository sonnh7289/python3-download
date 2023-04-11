#import libraries
import numpy as np
import imageio
import scipy.ndimage
import cv2
import requests

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
app = Flask(__name__)
def dodge(front,back):
    result=front*255/(255-back)
    result[result>255]=255
    result[result==255]=255
    return result.astype("uint8")
def grayscale(rgb):
    return np.dot(rgb[...,:3],[0.299,0.587,0.114]) # thsi is the  formula convert an image to black and white
@app.route("/home", methods=["GET"])
def get_Home():
    link_full = request.headers.get('Link-Full')
    img_data = requests.get(link_full)
    with open('my.jpg', 'wb') as f:
        f.write(img_data.content)
    #lets create a variable which store a image
    
    #this function will convert your image into sketch formate
    imageColor = imageio.imread("my.jpg")   
    g=grayscale(imageColor)
    i=255-g

    #lets create blurred image
    b=scipy.ndimage.filters.gaussian_filter(i,sigma=10)
    imageOut=dodge(b,g)

    #write the name of the picture which you have want
    cv2.imwrite("my_sketch.png",imageOut)
    response = requests.put("https://api.imgbb.com/1/upload?expiration=600&key=2d2e8117df677dffe0644a0ca32dd45d", headers=0, data=open("my_sketch.png",'r').read())
    return response    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1938)
