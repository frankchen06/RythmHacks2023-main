from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import time
import random
import json

PINTREST_URL = "https://www.pinterest.ca/search/pins/?q={query}&rs=typed"
driver = webdriver.Chrome()

# adds items to the queue based off of a search query
def get_images_from_query(query):
    driver.get(PINTREST_URL.format(query=urllib.parse.quote(query)))
    driver.implicitly_wait(1)
    image_elements = driver.find_elements(By.TAG_NAME, "img")
    return_queue = []
    for i in range(len(image_elements)):
        try:
            image_url = image_elements[i].get_attribute("src")
        except:
            print("fuck you")
            continue
        # img_data = requests.get(image_url).content
        # file_name = f'./scraped/{i}.jpg'
        return_queue.append({"image_url":image_url})
    link_elements = driver.find_elements(By.CSS_SELECTOR, ".Wk9.CCY.S9z.ho-.kVc.xQ4.iyn")
    for i in range(0, len(link_elements), 2):
        try:
            index = int(i/2)
            return_queue[index]["link"] = link_elements[i].get_attribute("href")
            return_queue[index]["dir"] = gen_dir()
        except:
            print("flippity flip")
    # make sure it works fuck me
    filtered = []
    for x in return_queue:
        if ("link" in x) and ("image_url" in x): filtered.append(x)  
    return filtered
    
# gets images related to the first item in the queue and
# adds them to the end of the queue
def get_related_images(link):
    driver.get(link)
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 1000);")
    # ignore first element as it is the already downloaded image
    temp_queue = []
    time.sleep(1)
    driver.implicitly_wait(1)  
    link_elements = driver.find_elements(By.CSS_SELECTOR, ".Wk9.CCY.S9z.ho-.kVc.xQ4.iyn")
    for i in range(0, len(link_elements), 2):
        if i == 0: continue
        try:
            temp_queue.append({"link": link_elements[i].get_attribute("href")})
        except:
            continue
    return_queue = []
    for x in temp_queue:
        driver.get(x["link"])
        driver.implicitly_wait(1)
        time.sleep(0.1)
        image_element = driver.find_elements(By.CSS_SELECTOR, ".hCL.kVc.L4E.MIw")[0]
        try:
            x["image_url"] = image_element.get_attribute("src")
            if x["image_url"] == 'https://i.pinimg.com/736x/12/38/12/123812aaf40d11c5a7be5aa0aefc2363.jpg' or x["image_url"] == "https://i.pinimg.com/736x/30/95/4d/30954d9d8d120175d52a151074b39f3c.jpg":
                continue
            return_queue.append({"image_url": x["image_url"], "link": x["link"], "dir":gen_dir()})
        except:
            print("bitch")
    return return_queue

def get_image_tags(urls):
    tags = []
    for url in urls:
        driver.get(url)
        time.sleep(0.3)
        tag_elements = driver.find_elements(By.CSS_SELECTOR, ".Wk9.CCY.S9z.OVX.KhY.xQ4.uCz.iyn")[5:]
        for y in tag_elements:
            try:
                tags.append(y.text)
            except:
                continue
    return tags




def gen_dir():
    return {
        "x":(random.random()*2-1)*45,
        "y":(random.random()*2-1)*45,
        "rot":random.random()*20-10
    }