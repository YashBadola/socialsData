
import os
import re

def clean_text(text):
    # Standard Gutenberg start/end markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
    ]

    lines = text.split('\n')
    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        for marker in start_markers:
            if re.search(marker, line):
                start_idx = i + 1
                break

    for i, line in enumerate(lines):
        for marker in end_markers:
            if re.search(marker, line):
                end_idx = i
                break

    if start_idx == 0 and end_idx == len(lines):
        # Fallback for some files if regex didn't catch specific format
        pass

    content = lines[start_idx:end_idx]

    # Remove translator introductions or TOCs if identifiable
    # For Kant's Critique (pg4280), it often starts with translator's preface
    # We will try to find the actual start of Kant's text.
    # A common starting point for Critique is "PREFACE TO THE FIRST EDITION"

    cleaned_content = []
    in_intro = True

    # Heuristics for specific files
    # Critique of Pure Reason
    if "Critique of Pure Reason" in text[:5000]:
        # Look for "PREFACE TO THE FIRST EDITION"
        found_start = False
        for i, line in enumerate(content):
            if "PREFACE TO THE FIRST EDITION" in line.upper():
                content = content[i:]
                found_start = True
                break

    # Metaphysic of Morals
    if "METAPHYSIC OF MORALS" in text[:5000].upper():
         # Look for "PREFACE"
        found_start = False
        for i, line in enumerate(content):
            if line.strip() == "PREFACE.":
                content = content[i:]
                found_start = True
                break

    return "\n".join(content).strip()

def main():
    base_dir = "socials_data/personalities/immanuel_kant/raw"
    files = [f for f in os.listdir(base_dir) if f.endswith(".txt")]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        print(f"Cleaning {filename}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        cleaned = clean_text(text)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"Cleaned {filename}. Length: {len(text)} -> {len(cleaned)}")

if __name__ == "__main__":
    main()
