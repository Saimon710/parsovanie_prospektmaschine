import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from models import Leaflet


class ProspektParser:
    URL = "https://www.prospektmaschine.de/hypermarkte/"

    def fetch_page(self) -> BeautifulSoup:
        response = requests.get(self.URL, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def parse_leaflets(self) -> List[Leaflet]:
        soup = self.fetch_page()
        leaflets = []

        #Selects all leaflet items
        items = soup.select("div.brochure-thumb")

        for item in items:
            try:
                #Getting the title
                title = item.select_one(".grid-item-content strong").get_text(strip=True) 

                #Getting the shop name
                shop_name = item.select_one(".grid-logo img")["alt"].replace("Logo ", "") 

                #Getting the image source
                img = item.select_one(".img-container img") 
                thumbnail = img.get("src") or img.get("data-src")  # Handles lazy-loaded images
                
                #Getting the validity dates
                date = item.select_one("p.grid-item-content small.hidden-sm").get_text(strip=True)
                valid_from_str, valid_to_str = date.split(" - ")
                # Convert from dd.mm.yyyy to yyyy-mm-dd
                valid_from = datetime.strptime(valid_from_str, "%d.%m.%Y").strftime("%Y-%m-%d")
                valid_to = datetime.strptime(valid_to_str, "%d.%m.%Y").strftime("%Y-%m-%d")

                leaflet = Leaflet(
                    title=title,
                    thumbnail=thumbnail,
                    shop_name=shop_name,
                    valid_from=valid_from,
                    valid_to=valid_to,
                    parsed_time=Leaflet.current_time(),
                )
                leaflets.append(leaflet)

            except Exception:
                continue

        return leaflets
