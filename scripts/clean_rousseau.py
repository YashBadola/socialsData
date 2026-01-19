import os
import re
import requests

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, content)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            end_idx = match.start()
            break

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

def download_file(url, filepath):
    print(f"Downloading from {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Download complete.")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
files = [
    {
        "filename": "social_contract.txt",
        "url": "https://www.gutenberg.org/ebooks/46333.txt.utf-8"
    }
]

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

for item in files:
    filepath = os.path.join(base_dir, item["filename"])
    if not os.path.exists(filepath):
        try:
            download_file(item["url"], filepath)
            clean_gutenberg_text(filepath)
        except Exception as e:
            print(f"Failed to process {item['filename']}: {e}")
    else:
        print(f"File already exists: {filepath}")
