from bs4 import BeautifulSoup
from category_scraper import CategoryScraper
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
# 
#import requests
url = os.getenv('WEBPAGE_URL')

#static pages
#page = requests.get(url)
#soup = BeautifulSoup(page.text, 'html')
#print(soup.prettify())

service = Service(executable_path=os.getenv('CHROME_DRIVER_PATH'))

# dynamic websites
options = webdriver.ChromeOptions()
driver = Chrome(service=service, options= options)
wait = WebDriverWait(driver, 10)
driver.get(url)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "less-padding-mb")))

soup = BeautifulSoup(driver.page_source, 'html.parser')

divs = soup.find_all("div", "less-padding-mb")
print(len(divs))

category_scraper = CategoryScraper(driver, url)
categories = list(defaultdict())
for item in divs:
    ahref = item.find("a")
    category = defaultdict()
    category_href = ahref.get('href')
    imgcard = ahref.find("div", "card-img-top")

    # picture from service
    img = imgcard.find("img")

    # card content
    card_body = ahref.find("div", "card-body")
    card_content = card_body.find("div", "card-content")
    span_title = card_content.find("span", "card-title")

    category["img"] = img.get("src")
    category["title"] = span_title.string.strip()

    category["content"] = category_scraper.getCategoryJson(url + category_href)

    categories.append(category)

# probably writing the result into a file is a better idea,
# but priting it in the terminal is fine
print(f'categories \n {json.dumps(categories)}')
