import os
import re

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    # Added \s* to handle potential spaces
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK .*\*\*\*", # No spaces
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK .*\*\*\*", # No spaces
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, content)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            end_idx = match.start()
            break

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Additional cleaning for specific artifacts (like "Produced by..." appearing after the marker)
    # We remove the first few lines if they look like credits
    lines = text.splitlines()
    cleaned_lines = []
    header_passed = False

    # Heuristic: Skip initial lines that are empty or contain "Produced by" or "Updated:"
    # until we hit a substantial title or text.
    # Actually, simply removing "Produced by" lines might be safer.

    for line in lines:
        if not header_passed:
            if not line.strip():
                continue
            if "Produced by" in line or "Updated:" in line:
                continue
            # If we reach here, we assume it's the start of the book (Title usually)
            header_passed = True
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/bertrand_russell/raw"
files = [
    "problems_of_philosophy.txt",
    "analysis_of_mind.txt"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        clean_gutenberg_text(filepath)
    else:
        print(f"File not found: {filepath}")
