import requests
import os
import re

PERSONALITY_ID = "aristotle"
BASE_DIR = f"socials_data/personalities/{PERSONALITY_ID}/raw"
os.makedirs(BASE_DIR, exist_ok=True)

WORKS = [
    {"id": "8438", "title": "nicomachean_ethics", "start_marker": "INTRODUCTION", "end_marker": "End of the Project Gutenberg EBook"},
    {"id": "6762", "title": "politics", "start_marker": "A TREATISE ON GOVERNMENT", "end_marker": "End of the Project Gutenberg EBook"}, # Adjusted after inspection if needed
    {"id": "1974", "title": "poetics", "start_marker": "ARISTOTLE’S POETICS", "end_marker": "*** END OF THIS PROJECT GUTENBERG EBOOK"},
    {"id": "2412", "title": "the_categories", "start_marker": "THE CATEGORIES", "end_marker": "*** END OF THIS PROJECT GUTENBERG EBOOK"}
]

# Alternative markers might be needed. I'll inspect after first run or add fallback logic.
# For 8438, "INTRODUCTION" is the start of the book content roughly.
# For 6762, title is "A Treatise on Government".
# For 1974, snippet showed "Identity exists...". Wait, 1974 starts with "Analysis of Contents".
# For 2412, "THE CATEGORIES" is likely the start.

def download_and_clean(work):
    url = f"https://www.gutenberg.org/cache/epub/{work['id']}/pg{work['id']}.txt"
    print(f"Downloading {work['title']} from {url}...")
    response = requests.get(url)
    response.encoding = 'utf-8-sig'
    text = response.text

    # Generic Gutenberg cleaning first
    # This removes the license header and footer roughly
    # We look for "*** START OF" and "*** END OF"

    start_match = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', text)
    end_match = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK', text)

    start_idx = 0
    end_idx = len(text)

    if start_match:
        start_idx = start_match.end()

    if end_match:
        end_idx = end_match.start()

    cleaned_text = text[start_idx:end_idx].strip()

    # Second pass: remove specific intros if markers are provided and found
    if work.get("start_marker"):
        # Case insensitive search for the marker
        marker_match = re.search(re.escape(work["start_marker"]), cleaned_text, re.IGNORECASE)
        if marker_match:
            print(f"  Found start marker '{work['start_marker']}' at index {marker_match.start()}")
            cleaned_text = cleaned_text[marker_match.start():]
        else:
            print(f"  Warning: Start marker '{work['start_marker']}' not found. Saving generic clean.")

    # Second pass end marker (less critical usually as footer is often caught by generic)

    output_path = os.path.join(BASE_DIR, f"{work['title']}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"Saved {output_path} ({len(cleaned_text)} chars).")

if __name__ == "__main__":
    for work in WORKS:
        try:
            download_and_clean(work)
        except Exception as e:
            print(f"Error processing {work['title']}: {e}")
