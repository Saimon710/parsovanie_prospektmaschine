import json
from leaflet_parser import pParser

OUTPUT_FILE = "output/leaflets.json"


def main():
    parser = pParser()
    leaflets = parser.parse_leaflets()

    data = [leaflet.__dict__ for leaflet in leaflets]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Uložených letákov: {len(data)}")


if __name__ == "__main__":
    main()
