import os
import re
import requests

# Base directory for Rousseau's raw data
BASE_DIR = "socials_data/personalities/jean_jacques_rousseau/raw"
os.makedirs(BASE_DIR, exist_ok=True)

# Files to download
URLS = {
    "the_social_contract_and_discourses.txt": "https://www.gutenberg.org/ebooks/46333.txt.utf-8",
    "emile.txt": "https://www.gutenberg.org/ebooks/5427.txt.utf-8",
    "confessions.txt": "https://www.gutenberg.org/ebooks/3913.txt.utf-8",
    "discourse_on_inequality.txt": "https://www.gutenberg.org/ebooks/11136.txt.utf-8",
}

def clean_gutenberg_text(text):
    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*", # More permissive
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*",
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start_idx = match.end()
            break

    end_idx = len(text)
    for pattern in end_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            end_idx = match.start()
            break

    return text[start_idx:end_idx].strip()

def download_and_clean():
    for filename, url in URLS.items():
        filepath = os.path.join(BASE_DIR, filename)
        print(f"Downloading {filename} from {url}...")
        try:
            # Gutenberg can be picky about User-Agents
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, allow_redirects=True, timeout=60, headers=headers)
            response.raise_for_status()
            content = response.content.decode('utf-8') # Decode as utf-8 explicitly

            print(f"Cleaning {filename}...")
            cleaned_text = clean_gutenberg_text(content)

            if not cleaned_text:
                print(f"Warning: Cleaned text for {filename} is empty! Dumping raw start...")
                print(content[:500])

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            print(f"Saved {filepath}")

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    download_and_clean()
