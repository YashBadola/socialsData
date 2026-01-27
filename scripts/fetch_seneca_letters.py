import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://en.wikisource.org/wiki/Moral_letters_to_Lucilius/Letter_{}"
OUTPUT_DIR = "socials_data/personalities/seneca/raw"
HEADERS = {
    "User-Agent": "SocialsDataBot/0.1 (https://github.com/example/socials-data; bot@example.com)"
}

def fetch_letter(letter_num):
    url = BASE_URL.format(letter_num)
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch letter {letter_num}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract content
    # The content is usually in a div with class "mw-parser-output"
    content_div = soup.find('div', class_='mw-parser-output')

    if not content_div:
        print(f"Could not find content div for letter {letter_num}")
        return None

    # We want to exclude navigation, which might be in tables or divs with specific classes.
    # But simpler approach: get all paragraphs.
    paragraphs = content_div.find_all('p')

    text = []
    for p in paragraphs:
        t = p.get_text().strip()
        # Simple heuristic to skip short navigation links if they end up in P
        if len(t) > 0:
            text.append(t)

    full_text = "\n\n".join(text)

    return full_text

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Let's fetch first 20 letters
    for i in range(1, 21):
        content = fetch_letter(i)
        if content:
            filename = os.path.join(OUTPUT_DIR, f"letter_{i}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved {filename}")
        time.sleep(1) # Be nice to the server

if __name__ == "__main__":
    main()
