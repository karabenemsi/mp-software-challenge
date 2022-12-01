import httpx
from bs4 import BeautifulSoup
from wool import Wool

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


def searchWoolPathByBrandAndName(brand, name, portalUrl):
    return 'hello'
