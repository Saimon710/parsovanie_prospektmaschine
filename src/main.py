import json
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from leaflet_parser import ProspektParser

# Output path relative to project root
OUTPUT_FILE = Path(__file__).parent.parent / "output" / "leaflets.json"


def main():
    parser = ProspektParser()
    leaflets = parser.parse_leaflets()

    data = [leaflet.__dict__ for leaflet in leaflets]

    # Create output directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Uložených letákov: {len(data)}")


if __name__ == "__main__":
    main()
