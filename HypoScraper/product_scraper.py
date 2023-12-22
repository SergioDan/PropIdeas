from bs4 import BeautifulSoup
from collections import defaultdict

import json
import re
import time

class ProductScraper:
    def __init__(self, driver):
        self.__driver = driver

    def getProductJsonFromUrl(self, url):
        self.__driver.get(url)
        time.sleep(10) 
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')

        product_json = defaultdict()

        container = soup.find("div", {"class" : re.compile("col-12 product-container adj-pad")})
        parent_div = container.parent
        product_id = parent_div.get("id")
        product_json["id"] = product_id
        turbo_frame_image = container.find("turbo-frame", {"id":re.compile("product[-]\d+[-]image[-]frame")})

        product_json["image"] = turbo_frame_image.find("img").get("src")
        col_product_description = container.find("div", {"class": re.compile("col[-]sm[-]\d+\scol[-]md[-]\d+\sorder[-]\d+\sorder[-]md[-]\d+")})

        title = col_product_description.find("div", {"class": re.compile("product[-]title[-]\d+")}).find("p").string
        product_json["title"] = title.strip()
        description_paragraph = col_product_description.find("p", {"class":re.compile("trix[-]content\slead\scustom[-]text[-]color")})

        product_json["description"] = description_paragraph.string.strip()

        prices_list_frame = col_product_description.find("turbo-frame", {"id": re.compile("product[-]\d+[-]price[-]frame")})
        prices_list_divs = prices_list_frame.find_all("div")

        def getSpan(price_div):
            span_price = price_div.find("span")
            return span_price.string.strip()

        def findSelectedDiv(x):
            if "d-block" in x.get("class"):
                return True
            else:
                return False

        filtered = filter(findSelectedDiv, prices_list_divs)
        selected = next(filtered)

        prices = []
        for price in prices_list_divs:
            if price == selected:
                pass
            span_price = getSpan(price)
            prices.append(span_price)

        prices.sort()
        product_json["prices"] = prices

        variant_size = col_product_description.find("select", {"name":"variant_size"})

        if variant_size != None:
            options_list = variant_size.find_all("option")
            list = []
            for option in options_list:
                list.append(option.string)
            list.sort()
            product_json["sizes"] = list

        return product_json
