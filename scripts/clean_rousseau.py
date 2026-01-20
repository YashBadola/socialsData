import os
import re

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Standard patterns
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"End of the Project Gutenberg EBook",
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            start_idx = match.end()
            break

    # Fallback/Specifics
    if "social_contract.txt" in filepath and start_idx == 0:
        # Start at "THE SOCIAL CONTRACT & DISCOURSES"
        match = re.search(r"THE SOCIAL CONTRACT & DISCOURSES", content)
        if match:
            start_idx = match.start()

    if "confessions.txt" in filepath and start_idx == 0:
         # Start at "BOOK I."
        match = re.search(r"BOOK I\.", content)
        if match:
            start_idx = match.start()


    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            end_idx = match.start()
            break

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
files = [
    "social_contract.txt",
    "confessions.txt"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        clean_gutenberg_text(filepath)
    else:
        print(f"File not found: {filepath}")
