import requests
import os
import re

PERSONALITY_DIR = "socials_data/personalities/aristotle/raw"
OS_PERSONALITY_DIR = os.path.join(os.getcwd(), PERSONALITY_DIR)

# Politics: 6762
# Nicomachean Ethics: 8438
# Poetics: 1974
# Removed Metaphysics because 10616 is John Locke, and a good PD Metaphysics text is not easily found.

FILES = {
    "politics.txt": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
    "nicomachean_ethics.txt": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
    "poetics.txt": "https://www.gutenberg.org/cache/epub/1974/pg1974.txt"
}

def clean_gutenberg_text(text):
    # Find start
    # Look for "START OF THE PROJECT GUTENBERG" or similar
    start_match = re.search(r"\*\*\* ?START OF TH(E|IS) PROJECT GUTENBERG EBOOK.*?(\*\*\*|$)", text, re.IGNORECASE | re.MULTILINE)

    if start_match:
        start_index = start_match.end()
    else:
        # Fallback to simple scan if regex fails or variations exist
        print("Warning: Could not find standard start marker. Checking for 'Produced by'...")
        start_match = re.search(r"Produced by.*?\n\n", text, re.IGNORECASE)
        start_index = start_match.end() if start_match else 0

    # Find end
    end_match = re.search(r"\*\*\* ?END OF TH(E|IS) PROJECT GUTENBERG EBOOK", text, re.IGNORECASE | re.MULTILINE)
    if end_match:
        end_index = end_match.start()
    else:
        end_index = len(text)

    content = text[start_index:end_index]

    return content.strip()

def main():
    if not os.path.exists(OS_PERSONALITY_DIR):
        os.makedirs(OS_PERSONALITY_DIR)

    for filename, url in FILES.items():
        print(f"Downloading {filename} from {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Project Gutenberg files are usually UTF-8 with BOM
            response.encoding = 'utf-8-sig'
            text = response.text

            cleaned_text = clean_gutenberg_text(text)

            filepath = os.path.join(OS_PERSONALITY_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            print(f"Saved {filename} ({len(cleaned_text)} chars).")

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
