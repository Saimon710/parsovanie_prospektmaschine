import requests
from bs4 import BeautifulSoup
from typing import List
from models import Leaflet


class pParser:
    URL = "https://www.prospektmaschine.de/hypermarkte/"

    def fetch_page(self) -> BeautifulSoup:
        response = requests.get(self.URL, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def parse_leaflets(self) -> List[Leaflet]:
        soup = self.fetch_page()
        leaflets = []

        items = soup.select("div.brochure-thumb")
        print("TOTAL ITEMS FOUND:", len(items))

        for item in items:
            try:
                title = item.select_one(".grid-item-content strong").get_text(strip=True)

                shop_name = item.select_one(".grid-logo img")["alt"].replace("Logo ", "")

                img = item.select_one(".img-container img")
                thumbnail = img.get("src") or img.get("data-src")

                date = item.select_one("p.grid-item-content small.hidden-sm").get_text(strip=True)
                valid_from, valid_to = date.split(" - ")


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
                # stabilita riešenia – ak jeden zlyhá, ostatné idú ďalej
                continue

        return leaflets
