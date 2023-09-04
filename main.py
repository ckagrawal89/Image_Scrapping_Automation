#!/usr/bin/env python
# coding: utf-8

import time
from PIL import Image
import requests
import base64
import io
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select


latestchrome=ChromeDriverManager().install()

# Creating Options for Chrome
options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--safebrowsing-disable-download-protection")
options.add_argument('disable-infobars')
options.add_argument("--no-sandbox")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs",{"safebrowsing.enabled":False})


url = ("https://www.google.com/search?q={s}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568")

str_input=input("Enter keyWord to search: ")
key_word=str_input.replace(' ','+')
folder_file_name=str_input.replace(' ','_')

print("\nOpening the Browser\n")

driver = webdriver.Chrome(options=options,service=Service(latestchrome))
driver.get(url.format(s=key_word))


# To manage SafeSearch
res=True
try:
    manage_settings=driver.find_elements(By.XPATH,"//div[contains(@class,'DgqC7c')]")
    manage_settings[0].click()
except:
    res=False
    
try:
    off_button=driver.find_elements(By.XPATH,"//label[contains(@data-value,'off')]")
    off_button[0].click()
except:
    print("\n")
    
if res:
    print("Back Done")
    driver.back()
    

endPageMessage="Looks like you've reached the end"

imgResults=[]
src=list()
endPage=""
print("\nFetching the links and Scrolling to the end\n")

while True:
    
    imgResults = driver.find_elements(By.XPATH,"//img[contains(@class,'rg_i Q4LuWd')]")
    src=[img.get_attribute('src') for img in imgResults]
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(3)
    
    
    imgResults = driver.find_elements(By.XPATH,"//img[contains(@class,'rg_i Q4LuWd')]")
    src=[img.get_attribute('src') for img in imgResults]    
    
    seeMore=driver.find_elements(By.XPATH,"//span[contains(@class,'XfJHbe')]")
    if(seeMore):
        if(seeMore[0].text=="See more anyway"):
            driver.find_elements(By.XPATH,"//span[contains(@class,'XfJHbe')]")[0].click()
    
    endPage=driver.find_element(By.XPATH,"//div[contains(@class,'OuJzKb Yu2Dnd')]").text
    if(endPage==endPageMessage):
        print("We've reached at the end of the page")
        break
 
    
    try:
        button=driver.find_element(By.XPATH,"//input[contains(@class,'LZ4I')]")
        button.click()
    except:
        continue
    
   

# Removing the NONE Value using filter method
src=list(filter(None,src))

# Printing the total number of valid Links fetched
print("Total number of links for images: ",len(src))

# Closing the driver
driver.close()


n=int(input("Enter a number of images to download: "))

folder_input=input("\nEnter the path to save the images: ")
if(folder_input[-1]=='\\'):
   folder_input=folder_input[:-1]


# Formatting the Folder Name and File Name

save_folder = folder_input.replace('\\','/')+"/{s}"
save_file=folder_input.replace('\\',"\\\\")+"\\\\{s}\\\\{s}{i}.png"

print("Making a directory named '"+folder_file_name+"'")
# Creting a folder at specified path
os.makedirs(save_folder.format(s=folder_file_name),exist_ok=True)
print("Directory Created!!\n")


print("\n\n----------Downloading Started----------")

for i in range(n):
    
    # if it's base64 images
    if src[i].startswith('data'):
        imgdata = base64.b64decode(src[i].split(',')[1])
        img = Image.open(io.BytesIO(imgdata))
        img.save(save_file.format(s=folder_file_name,i=i+1))
        
        # if it's image url
    else:
        img = Image.open(requests.get(src[i], stream=True).raw).convert('RGB')
        img.save(save_file.format(s=folder_file_name,i=i+1))

print("\n\n----------Downloading Completed ----------")


print("Total {n} images has downloaded!!!".format(n=n))


try:
    ex=int(input("Press 'ENTER' to EXIT"))
except:
    print("----------------Thank You!!!------------------")
    time.sleep(1)