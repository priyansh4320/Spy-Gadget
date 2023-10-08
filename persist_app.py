import streamlit as st
from transformers import pipeline, set_seed
import os
import cv2
import argparse
import filetype as ft
import numpy as np
from pathlib import Path
from PIL import Image
from facedetector import FaceDetector

import time

import base64
from io import BytesIO

import requests
from bs4 import BeautifulSoup 

import pandas as pd

##-------------------------------------------
def rev_search(img_url):
    url = "https://reverse-image-search-by-copyseeker.p.rapidapi.com/"

    querystring = {"imageUrl":f"{img_url}"}

    headers = {
        "X-RapidAPI-Key": "19f351f953mshe8f8e82d609061bp1ff0a1jsn8affa0ab462b",
        "X-RapidAPI-Host": "reverse-image-search-by-copyseeker.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    result = response.json()
    return result

## define face extraction--------------------------------------------------------------------------

def face_extraction(uploaded_video):
    video = cv2.VideoCapture(uploaded_video)

    # Create a folder to store the extracted faces.
    if not os.path.exists('faces'):
        os.mkdir('faces')

    # Iterate through the frames of the video.
    images= []
    padding = 1.0
    while True:

        # Read the frame.
        ret, frame = video.read()
        if ret and isinstance(frame, np.ndarray):
            image = {
                "file": frame,
                "sourcePath": video,
                "sourceType": "video",
            }
            images.append(image)
        else:
            break
    video.release()
    cv2.destroyAllWindows()
    for (i, image) in enumerate(images):
        print("[INFO] processing image {}/{}".format(i + 1, len(images)))
        faces = FaceDetector.detect(image["file"])

        array = cv2.cvtColor(image['file'], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(array)

        j = 1
        extracted_face = []
        for face in faces:     
            bbox = face['bounding_box']
            pivotX, pivotY = face['pivot']
            
            if bbox['width'] < 10 or bbox['height'] < 10:
                continue
            
            left = pivotX - bbox['width'] / 1.0 * padding
            top = pivotY - bbox['height'] / 1.0 * padding
            right = pivotX + bbox['width'] / 1.0 * padding
            bottom = pivotY + bbox['height'] / 1.0 * padding
            cropped = img.crop((left, top, right, bottom))
            extracted_face.append(cropped)
        return extracted_face
    pass

## extract para----------------------------------------------------------------------------------
def extract_para(ip_url):
  ip_url = ip_url.strip('"\'') 
  res = requests.get(ip_url,verify=False)
  print("req g")
  soup = BeautifulSoup(res.content, 'html.parser')
  para = soup.findAll(attrs={'p',"h1"})
  return para
## ddefine LLMs pipelines------------------------------------------------------------------------

@st.cache_resource
def name_extract(text):
    name_pipe = pipeline("text2text-generation", model="Priyansh4320/name_extract_model")
    out = name_pipe(text,max_length=50)[0]['generated_text']
    return out
    pass

@st.cache_resource
def getinfo(text):
    info_pipe = pipeline("text-generation", model="bigscience/bloomz-1b7")
    info_out = info_pipe(text, max_length=200)[0]['generated_text']
    return info_out

##  app--------------------------------------------------------

st.set_page_config(layout="wide")
st.title("SPY KIDS GADGET")
st.write("PERSIST venture Assignment")
dlinks =[]
face_extract = st.form(key = 'extract faces')
face_extract.title("extract faces from video")
face_extract.text("upload video")
uploaded_video = face_extract.file_uploader("Upload Mp4 file", type=["mp4"])
extract_face_btn = face_extract.form_submit_button("extract_faces")
if extract_face_btn:
    if not uploaded_video:
        face_extract.write("cant recognize")
    else:
        vid = uploaded_video.name
        img = face_extraction(vid)
        
        for idx, i in enumerate(img):
            img_array = Image.fromarray(np.array(i))
            buffered = BytesIO()
            img_array.save(buffered,format='JPEG')
            img_bytes = buffered.getvalue()
            img_b64 = base64.b64encode(img_bytes).decode()
            href = f'<a href="data:file/jpg;base64,{img_b64}" download="image{idx + 1}.jpg">Download Image {idx + 1}</a>'
            dlink = st.markdown(href, unsafe_allow_html=True)
            dlinks.append(f'data:file/jpg;base64,{img_b64}')
        st.write(dlinks)
        time.sleep(5)
        res = rev_search(dlink[0])
        st.write(res)
        
        #scrape and save the data
scrap_form = st.form(key="scrapping")
uploaded_data_files = scrap_form.file_uploader(
            label="Choose Files",
            type=["csv"],  # Specify the allowed file types if needed
            accept_multiple_files=True
        )
scrap_btn=scrap_form.form_submit_button("scrap the file")
if scrap_btn:
    scrap_form.write("start-scrapping")
    df =  pd.DataFrame(columns=["name","image","source_links","scraped_data"])
    for i,file in enumerate(list(uploaded_data_files)):
        temp = pd.read_csv(file)
        urls = [x for x in  temp['Source URL'][:15]]
        df['source_links'][i]=urls
        urls = [extract_para(str(x)) for x in urls]
        df["scraped_data"][i]=urls   
        scrap_form.write(st.dataframe(df))
    scrap_form.write("scraped")     
pass
        