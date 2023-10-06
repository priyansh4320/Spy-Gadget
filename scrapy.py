import requests
from bs4 import BeautifulSoup 
import pandas as pd
from functools import cache
import os
import base64

#---------------------------------------------------------------------------------
#read input_data and store all urls in list
df  = pd.read_excel("result.xlsx")
#print(df.columns, "\n", df.head())

urls = [url for url in df['urls']]
#print(type(urls[0]))

#---------------------------------------------------------------------------------
#function to extract titles
def extract_title(ip_url,class_names):
    res = requests.get(ip_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    title = soup.find('h1' , {'class':class_names})
    

    if title is not None:
        title = title.text
    return title

#-------------------------------------------------------------------------------
#function to extract paragraphs
def extract_para(ip_url,class_name):
  res = requests.get(ip_url)
  soup = BeautifulSoup(res.content, 'html.parser')

  para = soup.findAll(attrs={'class':class_name},)
  #print(para)
  if len(para)>0:
    for i in range(len(para)):
      para[i] = para[i].text.replace("\n"," ")
      para[i] = para[i].replace("\xa0"," ")
    para = " ".join(para)
  return para

#--------------------------------------------------------------------------------------------
#store title with text in text file with filename as URL in results folder
def save_list_to_file(folder_path, file_name, text_list):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Encode the URL to base64 to make it a valid file name
        encoded_file_name = base64.urlsafe_b64encode(file_name.encode()).decode()
        file_path = os.path.join(folder_path, encoded_file_name + '.txt')
        
        with open(file_path, 'w') as file:
            for line in text_list:
                file.write(line + '\n')
        print("List of text saved to", file_path)
    except Exception as e:
        print("Error occurred while saving the list of text:", e)

#----------------------------------------------------------------------------------------------------------------
#store title-text,..  text into an excel file for further cleaning  
class_name = ["entry-title","post-full-title"]
class_para = ["h-box","entry-content single-content","entry-content clearfix","amp_content","channel-profile","post-content","single-body entry-content typography-copy","entry-content","et_pb_module et_pb_post_content et_pb_post_content_0_tb_body"]
title_para_pair = {
    'text':[],
    'url':[]
}
for url in urls:
    print(url)
    title = extract_title(url,class_name)
    para = extract_para(url,class_para)
    title_para_pair['text'].append(" ".join([str(title),str(para)]))
    title_para_pair['url'].append(str(url))
    #save_list_to_file('results',f"{str(url)}.txt",[title,para])

tp = pd.DataFrame(title_para_pair)
tp.to_csv("text.csv")