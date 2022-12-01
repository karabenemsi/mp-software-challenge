from os import path
from bs4 import BeautifulSoup
import httpx
import json
from app.data_handler import DataHandler

from app.wool import Wool


BASE_URL = "https://www.wollplatz.de/wolle"
AVAILABLE_TEXT = "Lieferbar"

# Note: Hahn Alpacca is not listed on the page. Using SMC Alpacca Cloud instead
# ToDo: get paths by search on site
woolPathList = ["/stylecraft/stylecraft-special-dk", "/drops/drops-safran",
                "/dmc/dmc-natura-xl", "/drops/drops-baby-merino-mix", "/smc-schachenmayr/smc-alpaca-cloud"]


def getWoolFromUrlPath(woolUrl):

    with httpx.Client() as client:
        response = client.get(woolUrl)
        parser = BeautifulSoup(response.text, 'html.parser')
        name = parser.find(id="pageheadertitle").text
        wool = Wool(name)

        infoTable = parser.find(id="pdetailTableSpecs").find("table")

        wool.composition = infoTable.find('td', text="Zusammenstellung").next_sibling.text
        wool.needleGauge = infoTable.find('td', text="Nadelstärke").next_sibling.text
        wool.price = float(parser.find('span', class_="product-price").attrs["content"])
        wool.isAvailable = parser.find(id="ContentPlaceHolder1_upStockInfoDescription").find('span').text == AVAILABLE_TEXT
        wool.brand = infoTable.find('td', text="Marke").next_sibling.find('span').text

        return wool


if __name__ == "__main__":

    wools = []
    for woolPath in woolPathList:
        wools.append(getWoolFromUrlPath(BASE_URL + woolPath))
    DataHandler.saveToFile(wools)
