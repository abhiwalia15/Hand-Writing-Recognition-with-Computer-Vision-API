# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 19:39:28 2018

@author: Manoj
"""
#import pytesseract as pt
import cv2
#import tesseract
import pytesseract
from pytesseract import image_to_string
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Python37-32\Lib\site-packages\pytesseract'

def xyz():
	x = [1,2,3]
	y = np.asarray(x)
	print(y)

def readImage():
     print("in readImage")
     img1 = Image.open("1.jpg")
	 
     #img = cv2.imread("data/1.jpg")
     print("start")
     text = image_to_string(img1)
     print(text)
     print("done")
    



def main():

	
    print("in main")
    readImage()
    #xyz()
	





if __name__=="__main__":
    main()
    #readImage()