import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup

def process_wittgenstein(personality_dir):
    personality_dir = Path(personality_dir)
    raw_file = personality_dir / "raw" / "tractatus.html"
    processed_dir = personality_dir / "processed"
    output_file = processed_dir / "data.jsonl"

    if not raw_file.exists():
        print(f"File not found: {raw_file}")
        return

    processed_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading {raw_file}...")
    with open(raw_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    # Find all rows in the table
    # We look for rows that contain the specific classes
    rows = soup.find_all("tr")

    data = []

    print(f"Found {len(rows)} rows. Processing...")

    for row in rows:
        # Check if it has the relevant cells
        pnum_cell = row.find("td", class_="pnum")
        ger_cell = row.find("td", class_="ger")
        ogd_cell = row.find("td", class_="ogd")
        pmc_cell = row.find("td", class_="pmc")

        if pnum_cell and ger_cell and ogd_cell and pmc_cell:
            pnum = pnum_cell.get_text(strip=True)
            # Remove the '*' from pnum if present (it's a footnote marker)
            if pnum.endswith('*'):
                pnum = pnum[:-1]

            ger_text = " ".join(ger_cell.stripped_strings)
            ogd_text = " ".join(ogd_cell.stripped_strings)
            pmc_text = " ".join(pmc_cell.stripped_strings)

            # Create record
            # We use PMC as the main text
            record = {
                "text": pmc_text,
                "proposition": pnum,
                "german": ger_text,
                "ogden": ogd_text,
                "pears_mcguinness": pmc_text,
                "source": "Tractatus Logico-Philosophicus"
            }
            data.append(record)

    # Write to data.jsonl
    with open(output_file, "w", encoding="utf-8") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")

    print(f"Processed {len(data)} propositions to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/process_wittgenstein.py <personality_dir>")
        sys.exit(1)

    process_wittgenstein(sys.argv[1])
