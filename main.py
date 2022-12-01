from app.data_handler import DataHandler
import app.scraper as scraper




BASE_URL = "https://www.wollplatz.de/wolle"
AVAILABLE_TEXT = "Lieferbar"

# Note: Hahn Alpacca is not listed on the page. Using SMC Alpacca Cloud instead
# ToDo: get paths by search on site
woolPathList = ["/stylecraft/stylecraft-special-dk", "/drops/drops-safran",
                "/dmc/dmc-natura-xl", "/drops/drops-baby-merino-mix", "/smc-schachenmayr/smc-alpaca-cloud"]





if __name__ == "__main__":

    wools = []



    
    for woolPath in woolPathList:
        wools.append(scraper.getWoolFromUrlPath(BASE_URL + woolPath))
    DataHandler.saveToFile(wools)
