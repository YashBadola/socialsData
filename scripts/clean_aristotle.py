import re
from pathlib import Path

RAW_DIR = Path("socials_data/personalities/aristotle/raw")

def clean_text(text):
    # Find start and end markers
    start_marker_match = re.search(r"\*\*\* START OF T(HE|HIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    end_marker_match = re.search(r"\*\*\* END OF T(HE|HIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)

    start_idx = 0
    end_idx = len(text)

    if start_marker_match:
        start_idx = start_marker_match.end()

    if end_marker_match:
        end_idx = end_marker_match.start()

    # Extract content
    content = text[start_idx:end_idx]

    # Strip leading/trailing whitespace
    return content.strip()

def main():
    for file_path in RAW_DIR.glob("*.txt"):
        print(f"Cleaning {file_path.name}...")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned_text = clean_text(text)

        # Overwrite the file with cleaned text
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print(f"Cleaned {file_path.name}")

if __name__ == "__main__":
    main()
