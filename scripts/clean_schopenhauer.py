import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic Project Gutenberg header/footer stripper
    # This is a heuristic. It attempts to find the start and end of the book content.

    # Common start markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
        r"END OF THE PROJECT GUTENBERG EBOOK",
    ]

    start_pos = 0
    end_pos = len(content)

    for marker in start_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            start_pos = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            end_pos = match.start()
            break

    cleaned_content = content[start_pos:end_pos].strip()

    # Additional cleanup: remove license boilerplate if it leaked through
    # Sometimes there is a small prologue before the actual start

    return cleaned_content

def main():
    base_dir = "socials_data/personalities/arthur_schopenhauer/raw"
    files = [
        "world_as_will_and_idea_vol1.txt",
        "studies_in_pessimism.txt",
        "art_of_literature.txt",
        "counsels_and_maxims.txt"
    ]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            print(f"Cleaning {filename}...")
            cleaned = clean_file(filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"Cleaned {filename}. Length: {len(cleaned)}")
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    main()
