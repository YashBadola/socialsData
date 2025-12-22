
import re
from pathlib import Path

def clean_hume_text(filepath):
    path = Path(filepath)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find start and end markers
    # Project Gutenberg texts usually start with "START OF THE PROJECT GUTENBERG EBOOK"
    # and end with "END OF THE PROJECT GUTENBERG EBOOK"

    start_marker_pattern = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*"
    end_marker_pattern = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*"

    start_match = re.search(start_marker_pattern, text)
    end_match = re.search(end_marker_pattern, text)

    start_index = 0
    end_index = len(text)

    if start_match:
        start_index = start_match.end()

    if end_match:
        end_index = end_match.start()

    cleaned_text = text[start_index:end_index].strip()

    # Optional: Remove extra metadata or table of contents if present at the top
    # For this specific text, we might want to verify.
    # But stripping the main headers is the most important step.

    with open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Cleaned {path}")

if __name__ == "__main__":
    clean_hume_text("socials_data/personalities/david_hume/raw/enquiry_concerning_human_understanding.txt")
