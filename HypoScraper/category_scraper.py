from bs4 import BeautifulSoup
from collections import defaultdict
from product_scraper import ProductScraper

import re
import time

class CategoryScraper:
    def __init__(self, driver, env_url):
        self.__driver = driver
        self.__main_url = env_url

    def getCategoryJson(self, url):
        self.__driver.get(url)
        # check how to use webdriverwait here
        # temporary workaround
        time.sleep(10)  

        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')

        category_json = defaultdict()

        regex = re.compile('container[-]fluid.+')
        container = soup.find("div", {"class": regex})
        frames = container.find("turbo-frame", {"id": re.compile("products[-]list[-]\d+")})
        regexCards = re.compile("col[-].+")
        cards = frames.find_all("div", {"class": regexCards})
        products = list(defaultdict())

        product_scraper = ProductScraper(driver = self.__driver)
        for card in cards:
            product = defaultdict()
            ahref = card.find("a", "post-link")
            category_href = ahref.get('href')
            
            imgcard = ahref.find("div", "card-img-top")

            img = imgcard.find("img")
            # picture from service
            img_src = img.get("src")
            product["image"] = img_src

            # card content
            card_body = ahref.find("div", "card-body")
            card_content = card_body.find("div", "card-content")
            title = card_content.find("h5").string
            prices_range = card_content.find("p").string
            product["title"] = title
            product["prices_range"] = prices_range
            small_content = card_content.find("small")
            if (small_content != None):
                product["details"] = small_content.string.strip()

            # env_url is the original url defined in the scraper.py file
            product["extra"] = product_scraper.getProductJsonFromUrl(self.__main_url + category_href)

            products.append(product)

        category_json["products"] = products
            
        return category_json
        