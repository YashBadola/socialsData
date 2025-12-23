import requests
import re
import os
import subprocess
from pathlib import Path

def download_file(url):
    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()
    # Gutenberg files often have BOM
    text = response.content.decode('utf-8-sig')
    return text

def clean_text(text, start_marker, end_marker):
    start_idx = text.find(start_marker)
    if start_idx == -1:
        # Try a more generic approach if specific marker fails, or just fail
        # Often Gutenberg start is "*** START OF THE PROJECT GUTENBERG EBOOK"
        # Let's try to find the standard Gutenberg header end
        print(f"Specific start marker '{start_marker}' not found. Searching for generic Gutenberg header...")
        match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
        if match:
             start_idx = match.end()
        else:
             print("Warning: Could not find start marker.")
             start_idx = 0
    else:
        start_idx += len(start_marker)

    end_idx = text.find(end_marker)
    if end_idx == -1:
        # Try finding standard Gutenberg footer
        print(f"Specific end marker '{end_marker}' not found. Searching for generic Gutenberg footer...")
        match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
        if match:
            end_idx = match.start()
        else:
             print("Warning: Could not find end marker.")
             end_idx = len(text)

    return text[start_idx:end_idx].strip()

def main():
    base_dir = Path("socials_data/personalities/john_locke/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    # 1. Second Treatise of Government
    url1 = "https://www.gutenberg.org/cache/epub/7370/pg7370.txt"
    text1 = download_file(url1)
    # Generic regex cleaner might be safer given I can't interactively check easily without download.
    # But I can read the start/end of the downloaded string in this script to debug if needed.

    # For 7370:
    cleaned1 = clean_text(text1, "*** START OF THE PROJECT GUTENBERG EBOOK SECOND TREATISE OF GOVERNMENT ***", "*** END OF THE PROJECT GUTENBERG EBOOK SECOND TREATISE OF GOVERNMENT ***")

    with open(base_dir / "second_treatise_of_government.txt", "w", encoding="utf-8") as f:
        f.write(cleaned1)
        print("Saved second_treatise_of_government.txt")

    # 2. An Essay Concerning Human Understanding (Vol 1 & 2)
    # Vol 1: Books 1-2
    url2 = "https://www.gutenberg.org/cache/epub/10615/pg10615.txt"
    text2 = download_file(url2)
    cleaned2 = clean_text(text2, "*** START OF THE PROJECT GUTENBERG EBOOK HUMAN UNDERSTANDING VOL 1 ***", "*** END OF THE PROJECT GUTENBERG EBOOK HUMAN UNDERSTANDING VOL 1 ***")

    # Vol 2: Books 3-4
    url3 = "https://www.gutenberg.org/cache/epub/10616/pg10616.txt"
    text3 = download_file(url3)
    cleaned3 = clean_text(text3, "*** START OF THE PROJECT GUTENBERG EBOOK HUMAN UNDERSTANDING VOL 2 ***", "*** END OF THE PROJECT GUTENBERG EBOOK HUMAN UNDERSTANDING VOL 2 ***")

    # Combine them
    combined_essay = cleaned2 + "\n\n" + cleaned3
    with open(base_dir / "an_essay_concerning_human_understanding.txt", "w", encoding="utf-8") as f:
        f.write(combined_essay)
        print("Saved an_essay_concerning_human_understanding.txt")

    # Run the processing command
    print("Running process command...")
    # Using subprocess to call the CLI command.
    # Assumes the script is run from the root or PYTHONPATH is set correctly, but we can call it via python -m
    try:
        subprocess.run(["python", "-m", "socials_data.cli", "process", "john_locke", "--skip-qa"], check=True)
        print("Processing complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
