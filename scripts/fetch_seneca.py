import requests
from bs4 import BeautifulSoup
import os
import re

def fetch_letters():
    base_url = "https://en.wikisource.org/wiki/Moral_letters_to_Lucilius/Letter_"
    output_dir = "socials_data/personalities/seneca/raw"
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i in range(1, 6):
        url = f"{base_url}{i}"
        print(f"Fetching {url}...")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            content_div = soup.find('div', class_='mw-parser-output')

            if content_div:
                text_content = []
                # Wikisource text is usually in P tags.
                # Sometimes headers are relevant too.
                for element in content_div.find_all(['p', 'div']):
                    # Divs might contain the text in some layouts, but P is standard.
                    # Let's stick to P and maybe look for the "Greetings" pattern if possible.
                    # But extracting all P tags in mw-parser-output usually works for Wikisource.
                    pass

                # Let's just iterate over all direct children or specific tags
                for element in content_div.find_all(['p']):
                    # Check if it's not a navigation element or hidden
                    if element.find_parent(class_=['ws-noexport', 'navbox', 'mw-jump-link']):
                        continue
                    text = element.get_text().strip()
                    if text:
                        text_content.append(text)

                full_text = "\n\n".join(text_content)

                # Remove reference markers like [1], [2]
                full_text = re.sub(r'\[\d+\]', '', full_text)

                # Filter out obvious non-content
                # (Simple heuristic)

                filename = os.path.join(output_dir, f"letter_{i}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                print(f"Saved {filename}")
            else:
                print(f"Could not find content for letter {i}")
        else:
            print(f"Failed to fetch letter {i}: {response.status_code}")

if __name__ == "__main__":
    fetch_letters()
