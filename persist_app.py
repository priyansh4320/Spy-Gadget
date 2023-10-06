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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchWindowException , WebDriverException
from selenium.webdriver.chrome.options import Options

import base64
from io import BytesIO

import requests
from bs4 import BeautifulSoup 

import pandas as pd

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
## define pimeyes----------------------------------------------------------------------------------
def pimeye():
    options = Options() 
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    
    # Open the website
    driver.get("https://pimeyes.com/en/login")  # Replace with the URL of the website you want to login to

    # Find the login form elements (e.g., username and password fields, su
    #login
    type_attribute_value_pass = "password" 
    type_attribute_value_user = "email" 
    username = driver.find_element(By.XPATH, f'//*[@type="{type_attribute_value_user}"]')  # Replace "username" with the actual ID of the username field
    password = driver.find_element(By.XPATH, f'//*[@type="{type_attribute_value_pass}"]')  # Replace "password" with the actual ID of the password field
    submit_button = driver.find_element(By.CLASS_NAME, "login-btn")  # Replace "login-button" with the actual ID of the submit button

    # Enter your login credentials
    username.send_keys("aimagic123@mailinator.com")
    password.send_keys("Aiismagic123!")
    driver.find_element(By.XPATH,f'//input[@name="remember"]').click()
    submit_button.click()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"icon notranslate")))
    #open homepage
    home_attribute = "Open mainpage"

    homepage = driver.find_element(By.XPATH, f'//*[@aria-label="{home_attribute}"]')
    link_url = homepage.get_attribute("href")
    driver.execute_script(f'window.open("{link_url}");')
    driver.switch_to.window(driver.window_handles[-1])


    #upload faces
    driver.find_element(By.CLASS_NAME,"understand").click()
    driver.find_element(By.CLASS_NAME,"upload").click()
    #time.sleep(30)

    #start reverse search
    checkbox = "checkbox"
    checkbox = WebDriverWait(driver, 60).until(
        EC.visibility_of_any_elements_located((By.XPATH, f'//*[@type="{checkbox}"]'))
    )
    for i in checkbox:
        i.click()

    buttons = driver.find_elements(By.XPATH,f'//button[@data-v-a60bceaf=""]')
    buttons[3].click()


    #export result csv
    try:
        while(True):
            
            lines = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, f'//button[@data-v-5cd5e023=""]'))
            )
            lines.click()
            export = 'download'
            export = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@alt="{export}"]'))
            )
            export.click()

            filename = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "filename"))
            )
            filename.send_keys("results")

            export_csv = driver.find_element(By.XPATH,f'//button[@data-v-bbba1abc=""]').click()

            if WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"container limited-container"))).click():
                driver.close()
            upload_agian = WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, f'//button[@data-v-7e26e312=""]'))
            )
            upload_agian.click()

            search_agian = WebDriverWait(driver, 30).until(
                EC.visibility_of_any_elements_located((By.XPATH, f'//button[@data-v-a60bceaf=""]'))
            )
            search_agian[3].click()
    except (NoSuchWindowException,TimeoutException,WebDriverException) :
        st.write(":: exception Occured ::")
        driver.close()

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
            dlinks.append(dlink)
        time.sleep(5)
        pimeye()
        
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
        