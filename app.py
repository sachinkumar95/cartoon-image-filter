from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import base64
import socket
from io import BytesIO
import uuid
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


app = Flask(__name__)

@app.route('/')
def home():
    dir = app.static_folder
    # if os.listdir(dir) != []:
    #     print("yes")
    #     os.remove(os.path.join(app.static_folder,'test.png'))
    # if 'Cache-Control' not in response.headers:
    #     response.headers['Cache-Control'] = 'no-store'
    return render_template('index.html')

@app.route('/cartoonify',methods=['POST'])
def submit():
    if request.files['file'].filename == '':  # access the data inside 
        message = "No File Selected"
        return render_template('index.html', message=message)
   
 #   print(request.url_root)
    # read the image
    #print(request.files['file'].read());sys.exit()
 
   # originalmage = cv2.imread(request.files['file'], cv2.IMREAD_COLOR)
    originalmage = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imshow('img', originalmage) 
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')


    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')


    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    # fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    # for i, ax in enumerate(axes.flat):
    #     ax.imshow(images[i], cmap='gray')

    img = Image.fromarray(ReSized6, 'RGB')

    ran=str(uuid.uuid4())
    name = img.save('static/'+ran+'.png')
    #img.show()

    url = request.url_root+'static/'+ran+'.png'
    return render_template('plot.html', url =url)
    #plt.show()
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
