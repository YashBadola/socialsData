import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic Project Gutenberg header/footer cleaner
    # It tries to find the start and end markers and removes everything outside them.

    # Common start markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"START OF THE PROJECT GUTENBERG EBOOK",
        r"START OF THIS PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"END OF THE PROJECT GUTENBERG EBOOK",
        r"END OF THIS PROJECT GUTENBERG EBOOK",
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

    # Additional cleanup if necessary (e.g. removing license text that might remain)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {filepath}")

def main():
    base_dir = "socials_data/personalities/immanuel_kant/raw"
    files = [
        "critique_of_pure_reason.txt",
        "critique_of_practical_reason.txt",
        "metaphysic_of_morals.txt"
    ]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
