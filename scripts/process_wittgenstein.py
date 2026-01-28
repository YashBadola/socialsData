import re
import json
import os

# Path to files
RAW_FILE = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.html"
PROCESSED_DIR = "socials_data/personalities/ludwig_wittgenstein/processed"
PROCESSED_FILE = os.path.join(PROCESSED_DIR, "data.jsonl")

def process():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    with open(RAW_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find table rows with depth
    rows = re.findall(r'<tr class="tlpdepth(\d+)">(.*?)</tr>', content, re.DOTALL)

    with open(PROCESSED_FILE, 'w', encoding='utf-8') as out:
        for depth, inner in rows:
            # Extract ID
            id_match = re.search(r'<td class="pnum"[^>]*>(.*?)</td>', inner, re.DOTALL)
            if not id_match: continue

            # Clean ID (remove <a> tags, etc)
            raw_id = id_match.group(1)
            # Remove html tags
            clean_id = re.sub(r'<[^>]+>', '', raw_id).strip()
            # Remove * or other markers
            clean_id = clean_id.replace('*', '')

            # Extract Texts
            ger_match = re.search(r'<td class="ger">(.*?)</td>', inner, re.DOTALL)
            ogd_match = re.search(r'<td class="ogd">(.*?)</td>', inner, re.DOTALL)
            pmc_match = re.search(r'<td class="pmc">(.*?)</td>', inner, re.DOTALL)

            def clean_text(t):
                # Unescape entities if necessary, strip tags
                t = re.sub(r'<br\s*/?>', '\n', t) # Handle line breaks
                t = re.sub(r'<[^>]+>', '', t)
                t = t.replace('&nbsp;', ' ')
                t = t.replace('\n', ' ').strip()
                return " ".join(t.split()) # Collapse whitespace

            ger = clean_text(ger_match.group(1)) if ger_match else ""
            ogd = clean_text(ogd_match.group(1)) if ogd_match else ""
            pmc = clean_text(pmc_match.group(1)) if pmc_match else ""

            # Construct record
            # We'll use Pears/McGuinness as default text, or Ogden if Pears is empty
            text = pmc if pmc else ogd

            record = {
                "id": clean_id,
                "depth": int(depth),
                "text": f"{clean_id} {text}",
                "german": ger,
                "english_ogden": ogd,
                "english_pears": pmc,
                "source": "Tractatus Logico-Philosophicus"
            }

            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Processed {len(rows)} propositions.")

if __name__ == "__main__":
    process()
