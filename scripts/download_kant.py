import os
import requests
import time

# Define the base directory for raw files
BASE_DIR = "socials_data/personalities/immanuel_kant/raw"
os.makedirs(BASE_DIR, exist_ok=True)

# Define the texts to download (Title, ID)
texts = [
    ("critique_of_pure_reason.txt", "4280"),
    ("critique_of_practical_reason.txt", "5683"),
    ("fundamental_principles_metaphysic_morals.txt", "5682"),
    ("metaphysical_elements_ethics.txt", "5684"),
    ("critique_of_judgement.txt", "48433")
]

def download_text(filename, pg_id):
    url = f"https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt"
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Handle encoding (Project Gutenberg texts are usually UTF-8, but sometimes need help)
        response.encoding = 'utf-8-sig'
        content = response.text

        filepath = os.path.join(BASE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {filepath}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    for filename, pg_id in texts:
        download_text(filename, pg_id)
        time.sleep(1) # Be nice to the server
