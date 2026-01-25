import requests
from bs4 import BeautifulSoup
import os
import time

def fetch_letters():
    base_url = "https://en.wikisource.org/wiki/Moral_letters_to_Lucilius/Letter_"
    output_dir = "socials_data/personalities/lucius_annaeus_seneca/raw"
    os.makedirs(output_dir, exist_ok=True)

    # Let's try to fetch first 20 letters to make it elaborate
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    for i in range(1, 21):
        url = f"{base_url}{i}"
        print(f"Fetching {url}...")
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # The text is usually in div class="prp-pages-output"
                content_div = soup.find('div', class_='prp-pages-output')

                if content_div:
                    paragraphs = content_div.find_all('p')
                    text = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

                    filename = f"letter_{i:03d}.txt"
                    filepath = os.path.join(output_dir, filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"Saved {filename}")
                else:
                    print(f"Could not find content for Letter {i}")
            else:
                print(f"Failed to fetch Letter {i}: Status {response.status_code}")
        except Exception as e:
            print(f"Error fetching Letter {i}: {e}")

        # Be nice to the server
        time.sleep(0.5)

if __name__ == "__main__":
    fetch_letters()
