import requests
import re
import os

URLS = {
    "critique_of_pure_reason.txt": "https://www.gutenberg.org/cache/epub/4280/pg4280.txt",
    "critique_of_practical_reason.txt": "https://www.gutenberg.org/cache/epub/5683/pg5683.txt"
}

OUTPUT_DIR = "socials_data/personalities/immanuel_kant/raw"

def clean_text(text, filename):
    # Standard Gutenberg markers
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    end_idx = len(text)

    for pattern in start_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start_idx = match.end()
            break

    for pattern in end_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            end_idx = match.start()
            break

    if start_idx == 0:
        print(f"Warning: Start marker not found for {filename}")
    if end_idx == len(text):
        print(f"Warning: End marker not found for {filename}")

    return text[start_idx:end_idx].strip()

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename, url in URLS.items():
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Ensure correct encoding if possible, usually utf-8 for these IDs
            response.encoding = 'utf-8'

            raw_text = response.text
            cleaned_text = clean_text(raw_text, filename)

            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            print(f"Saved cleaned {filename} to {output_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
