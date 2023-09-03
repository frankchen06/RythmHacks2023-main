from bs4 import BeautifulSoup as bs
import urllib
import time
import random
import json
import requests

import ider

URL = "https://www.google.com/search?sca_esv=562232441&tbs=isz:l&sxsrf=AB5stBg6ucJfFBrkemVs_m3rMrKBYI13Pg:1693688218614&q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwibwYWl6IyBAxXEFlkFHbjsBtoQ0pQJegQIDBAB&biw=1536&bih=851"

# adds items to the queue based off of a search query
def get_images_from_query(query):
    soup = bs(requests.get(URL.format(query=urllib.parse.quote(query))).text, features="html.parser")
    image_elements = soup.select("tr>td>a>div>img", limit=10)
    print(len(image_elements))
    with open("./test.html", "w") as f:
        f.write(str(soup))
    return_queue = []
    for i in range(len(image_elements)):
        image_url = image_elements[i].get("src")
        image_title = ider.identify_image(image_url)
        return_queue.append(gen_dir(image_url, image_title))
    return return_queue
    
# gets images related to the first item in the queue and
# adds them to the end of the queue
def get_related_images(image_title):
    soup = bs(requests.get(URL.format(query=urllib.parse.quote(image_title))).text, features="html.parser")
    # print(URL.format(query=urllib.parse.quote(image_title)))
    image_elements = soup.select("tr>td>a>div>img", limit=5)
    # print(len(image_elements))
    with open("./test.html", "w") as f:
        f.write(str(soup))
    return_queue = []
    print(len(image_elements))
    for i in range(len(image_elements)):
        image_url = image_elements[i].get("src")
        image_title = ider.identify_image(image_url)
        return_queue.append(gen_dir(image_url, image_title))
    return return_queue

def get_image_tags(urls):
    tags = []
    for url in urls:
        id_tags = ider.identify_image(url)
        for x in id_tags.split(","):
            tags.append(x)
    return tags

def gen_dir(image_url, image_title):
    return {
        "x":(random.random()*2-1)*45,
        "y":(random.random()*2-1)*45,
        "rot":random.random()*20-10,
        "image_url": image_url,
        "image_title": image_title
    }