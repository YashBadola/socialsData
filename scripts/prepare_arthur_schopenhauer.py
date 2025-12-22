import os
import re
import urllib.request
import time

def clean_text(text):
    """
    Removes Project Gutenberg headers and footers.
    """
    # Common start markers
    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
        r"START OF THIS PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
        r"END OF THIS PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
    ]

    lines = text.split('\n')
    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        for marker in start_markers:
            if re.search(marker, line, re.IGNORECASE):
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Look for end marker from the end
    for i in range(len(lines) - 1, start_idx, -1):
        line = lines[i]
        for marker in end_markers:
            if re.search(marker, line, re.IGNORECASE):
                end_idx = i
                break
        if end_idx < len(lines):
            break

    # Special handling for translator's prefaces or specific internal markers if needed
    # For now, just standard Gutenberg cleaning

    return '\n'.join(lines[start_idx:end_idx]).strip()

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        # Use a user agent to avoid 403s
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8', errors='ignore')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
        print("Download complete.")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    personality_dir = os.path.join(base_dir, 'socials_data', 'personalities', 'arthur_schopenhauer')
    raw_dir = os.path.join(personality_dir, 'raw')

    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)

    sources = [
        {
            "filename": "world_as_will_vol1.txt",
            "url": "https://www.gutenberg.org/ebooks/38427.txt.utf-8"
        },
        {
            "filename": "essays_of_schopenhauer.txt",
            "url": "https://www.gutenberg.org/ebooks/11945.txt.utf-8"
        },
        {
            "filename": "counsels_and_maxims.txt",
            "url": "https://www.gutenberg.org/ebooks/10715.txt.utf-8"
        }
    ]

    for source in sources:
        filepath = os.path.join(raw_dir, source["filename"])
        # Download
        if download_file(source["url"], filepath):
            # Clean
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_text(content)

            # Simple check if cleaning worked (Gutenberg header usually has license info)
            if "PROJECT GUTENBERG EBOOK" in cleaned_content[:1000] and "START" in cleaned_content[:1000]:
                 print(f"Warning: It seems the start marker was not found or removed correctly for {source['filename']}")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Cleaned {source['filename']}")

            # Sleep to be nice to the server
            time.sleep(1)

if __name__ == "__main__":
    main()
