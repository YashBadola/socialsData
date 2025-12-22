import re
from pathlib import Path

def clean_gutenberg_text(text):
    # Find Start and End markers
    start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    end_match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)

    start_idx = start_match.end() if start_match else 0
    end_idx = end_match.start() if end_match else len(text)

    content = text[start_idx:end_idx]

    # Remove license text if it appears inside (sometimes it does)
    # Also remove common Gutenberg boilerplate if any

    return content.strip()

def main():
    base_dir = Path("socials_data/personalities/seneca")
    raw_file = base_dir / "raw" / "morals.txt"

    if not raw_file.exists():
        print(f"File {raw_file} not found.")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned_text = clean_gutenberg_text(text)

    # Overwrite the file or save as new?
    # Usually better to save as new or overwrite if we are confident.
    # The processor reads all .txt files. Let's overwrite or better, create a clean version.
    # But the processor reads *all* txt files. So we should probably replace the original or move it.

    with open(raw_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Cleaned {raw_file}")

if __name__ == "__main__":
    main()
