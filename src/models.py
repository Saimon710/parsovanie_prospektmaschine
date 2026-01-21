from dataclasses import dataclass
from datetime import datetime

@dataclass
class Leaflet:
    title: str
    thumbnail: str
    shop_name: str
    valid_from: str
    valid_to: str
    parsed_time: str

    @staticmethod
    def current_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
