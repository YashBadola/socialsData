import os
import requests
import re
from pathlib import Path

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle potential BOM
    content = response.content.decode('utf-8-sig')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_text(text, start_markers, end_markers):
    start_idx = -1
    for marker in start_markers:
        # Use regex for flexible matching if marker starts with regex:
        if marker.startswith("regex:"):
             pattern = marker[6:]
             match = re.search(pattern, text, re.IGNORECASE)
             if match:
                 start_idx = match.end()
                 break
        else:
            idx = text.find(marker)
            if idx != -1:
                start_idx = idx + len(marker)
                break

    if start_idx == -1:
        print(f"Warning: Start marker not found. Markers tried: {start_markers}")
        # Fallback: look for standard PG start
        pg_start = "*** START OF THE PROJECT GUTENBERG EBOOK"
        idx = text.find(pg_start)
        if idx != -1:
            # Find end of that line
            newline_idx = text.find('\n', idx)
            if newline_idx != -1:
                start_idx = newline_idx + 1
            else:
                start_idx = idx + len(pg_start)
            print("Fallback: Found standard Project Gutenberg start marker.")
        else:
             print("Warning: Standard Project Gutenberg start marker also not found. Using beginning of file.")
             start_idx = 0

    end_idx = -1
    for marker in end_markers:
        if marker.startswith("regex:"):
            pattern = marker[6:]
            match = re.search(pattern, text[start_idx:], re.IGNORECASE)
            if match:
                end_idx = start_idx + match.start()
                break
        else:
            idx = text.find(marker, start_idx)
            if idx != -1:
                end_idx = idx
                break

    if end_idx == -1:
         # Fallback: look for standard PG end
        pg_end = "*** END OF THE PROJECT GUTENBERG EBOOK"
        idx = text.find(pg_end, start_idx)
        if idx != -1:
            end_idx = idx
            print("Fallback: Found standard Project Gutenberg end marker.")
        else:
            print(f"Warning: End marker not found. Markers tried: {end_markers}")
            print("Warning: Standard Project Gutenberg end marker also not found. Using end of file.")
            end_idx = len(text)

    return text[start_idx:end_idx].strip()

def main():
    base_dir = Path("socials_data/personalities/jean_jacques_rousseau")
    raw_dir = base_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    sources = [
        {
            "id": "46333",
            "filename": "the_social_contract_and_discourses.txt",
            "url": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
            "start_markers": ["THE SOCIAL CONTRACT OR PRINCIPLES OF POLITICAL RIGHT"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THIS PROJECT GUTENBERG EBOOK"]
        },
        {
            "id": "3913",
            "filename": "the_confessions.txt",
            "url": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
            "start_markers": ["THE CONFESSIONS OF JEAN JACQUES ROUSSEAU"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THIS PROJECT GUTENBERG EBOOK"]
        },
        {
            "id": "5427",
            "filename": "emile.txt",
            "url": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt",
            "start_markers": ["regex:AUTHOR'S PREFACE"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THIS PROJECT GUTENBERG EBOOK"]
        }
    ]

    for source in sources:
        filepath = raw_dir / source["filename"]
        try:
            download_file(source["url"], filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_text(content, source["start_markers"], source["end_markers"])

            if len(cleaned_content) < 1000:
                 print(f"Warning: Cleaned content for {source['filename']} is suspiciously short ({len(cleaned_content)} chars).")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            print(f"Processed {source['filename']}")

        except Exception as e:
            print(f"Error processing {source['filename']}: {e}")

if __name__ == "__main__":
    main()
