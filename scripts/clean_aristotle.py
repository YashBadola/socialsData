import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
        content = f.read()

    # Generic Gutenberg start/end markers
    start_pattern = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
    end_pattern = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

    start_match = re.search(start_pattern, content)
    end_match = re.search(end_pattern, content)

    if start_match and end_match:
        content = content[start_match.end():end_match.start()]
    else:
        print(f"Warning: Could not find standard Gutenberg markers in {filepath}")
        # If we can't find markers, we might want to fail or just leave it (risky).
        # But looking at the grep output, they seem consistent.

    # Extra cleaning: remove leading/trailing whitespace
    content = content.strip()

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "socials_data", "personalities", "aristotle", "raw")

    for filename in os.listdir(raw_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(raw_dir, filename)
            clean_file(filepath)

if __name__ == "__main__":
    main()
