from os import path
from bs4 import BeautifulSoup
import httpx
import json


class Wool:

    isAvailable = True
    needleGauge = "someAmmount"
    name = "SomeWool"
    price = 0.0
    composition = "100% Wool"
    brand = "SomeBrand"

    def __init__(self, name):
        self.name = name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

BASE_URL = "https://www.wollplatz.de/wolle"
AVAILABLE_TEXT = "Lieferbar"

# Note: Hahn Alpacca is not listed on the page. Using SMC Alpacca Cloud instead
# ToDo: get paths by search on site
woolPathList = ["/stylecraft/stylecraft-special-dk", "/drops/drops-safran",
                "/dmc/dmc-natura-xl", "/drops/drops-baby-merino-mix", "/smc-schachenmayr/smc-alpaca-cloud"]


def getWoolFromUrlPath(woolPath):

    with httpx.Client(base_url=BASE_URL) as client:
        response = client.get(BASE_URL + woolPath)
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
        wools.append(getWoolFromUrlPath(woolPath))
        
    # Save in json lines format, each line is a valid json object
    with open('./data.jsonl', 'w', encoding='utf-8') as dataFile:
        dataFile.writelines([x.toJSON() + '\n' for x in wools])

