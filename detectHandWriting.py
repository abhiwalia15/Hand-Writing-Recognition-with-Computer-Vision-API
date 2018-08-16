# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 23:23:01 2018

@author: Manoj
"""

import requests, base64, io
import difflib
from PIL import Image
#import matplotlib.pyplot as plt 
from PIL import Image
from io import BytesIO
import glob
import time
from matplotlib.patches import Polygon
from matplotlib import pyplot as plt
#import matplotlib.patches as patches

import xlsxwriter

def writeToExcel(locImage,image,locCode,code):
    
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('images.xlsx','rb')
    worksheet = workbook.add_worksheet()
    worksheet.insert_image(locImage, image)
    #worksheet.write(locCode,code)
    workbook.close()

global code, preCode, postCode
#'CBGET * 0 05','CCAND 0 05',
codes = [ 'CCAINDOLE', 'CCAINDORF', 'CBGSSTOOK', 'CCAINDOOR',
         'CCAINDOOF', 'CLAINDOOS', 'CCAINDOOR', 'CCAINDOIO']

preCode = ["CBG","CCA","CSM","CCM","KCB","CCB","LLL","SSC","SSB"]
postCode = ["TX","ND","ST","PL","PR"]

def leetCode(my_string):

    replacements = ( ('*','X'), ('S','5'), ('F','7'), ('R','2'),
                    ('L','1'), ('O','0'), ('t','+'),('E','4' ),('I','1'), ('K','4'))
    
    new_string = my_string
    for old, new in replacements:
        new_string = new_string.replace(old, new)

    #print ( new_string )
    return new_string


def postProcess(code):
        
        code = "".join(code.split())
        if "*" in code:
            code = code.replace("*","X")
        if len(code)==9:
            
            print("code", code)
            detectedPreCode = code[0:3]
            detectedPostCode = code[4:6]
            detectedMiddleNum = code[3]
            detectedLastNums = code[6:]
            matchMid = leetCode(detectedMiddleNum)
            matchLast = leetCode(detectedLastNums)
            #print("detectedPreCode",detectedPreCode)
            #print("detectedPostCode",detectedPostCode)
            #print("detectedMiddleNum",detectedMiddleNum)
            #print("detectedLastNums",detectedLastNums)
            matchPre = difflib.get_close_matches(detectedPreCode, preCode)
            if matchPre:
                matchPre = matchPre[0]
                
            else:
                matchPre = detectedPreCode
            #print("matchPre",matchPre)
            matchPost = difflib.get_close_matches(detectedPostCode, postCode)
            if matchPost:
                matchPost = matchPost[0]
            else:
                matchPost = detectedPostCode
            #matchPre = difflib.get_close_matches(detectedPreCode, preCode)[0]
            #print("matchMid",matchMid)
            #print("matchLast",matchLast)
        
        
            #print("matchPost",matchPost)
            finalCode = matchPre + matchMid + matchPost + matchLast
            print("finalCode",finalCode)
            
            return finalCode
        
        else:
            return False
        
        

        
        
        
        
    


def OCR():
    ocr_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText"
    code = []
    i=1
    for file in glob.glob("data/*.jpg"):
        print(file)
        print("********************************************************************************************************")
        image = open(file,'rb').read()
   
        headers  = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': '6ff74a8c035442bcb4430728fd243ea1'}
        params   = {'handwriting' : True}   
        response = requests.post(ocr_url, headers=headers, params=params, data=image)
        response.raise_for_status()
        print("response:",response)
        operation_url = response.headers["Operation-Location"]
        analysis = {}
        while not "recognitionResult" in analysis:
            response_final = requests.get(response.headers["Operation-Location"], headers=headers)
            analysis       = response_final.json()
            time.sleep(1)
        
        polygons = [(line["boundingBox"], line["text"]) for line in analysis["recognitionResult"]["lines"]]    
        plt.figure(figsize=(15,15))

        #image  = Image.open(BytesIO(requests.get(image_url).content))
        image  = Image.open(BytesIO(image))
        #image.save("images/"+str(i)+".jpg","JPEG")
        
        ax     = plt.imshow(image)
        for polygon in polygons:
            vertices = [(polygon[0][i], polygon[0][i+1]) for i in range(0,len(polygon[0]),2)]
            text     = polygon[1]
            print("TEXT:",text)
            code.append(text)
            patch    = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
            ax.axes.add_patch(patch)
            plt.text(vertices[0][0], vertices[0][1], text,weight="bold", fontsize=20, va="top")
            _ = plt.axis("off")
            
        finalCode = postProcess(text)
        if finalCode==False:
            print("Can't Recognize")
        else:
            image.save("images/"+finalCode+".jpg","JPEG")
            #writeToExcel("A"+str(i),"images/"+finalCode+".jpg",finalCode,"B"+str(i))
            #print(code)
            i=i+1

def main():
   OCR()
   #postProcess()
   #leetCode()
   #detect_handwritten_ocr("data/1.jpg")
   #writeToExcel()
    


if __name__=="__main__":
    main()

   


