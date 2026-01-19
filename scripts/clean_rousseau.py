import os
import re

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"Produced by .*",
        r"Distributed Proofreading Team",
        r"Note: Images of the original pages",
        r"the Google Books Library Project",
        r"http://www.google.com/books.*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"End of the Project Gutenberg EBook",
    ]

    start_idx = 0
    found_standard_start = False

    # Try standard start first
    for pattern in start_patterns[:2]:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            start_idx = match.end()
            found_standard_start = True
            break

    if not found_standard_start:
        # Try specific patterns in the first 5000 chars
        # We repeat the search to strip multiple lines if they match different patterns
        # For example, line 1 matches pattern A, line 2 matches pattern B.
        # We want to find the furthest reaching match.

        # Actually, if we have header junk, we want to cut *after* all of it.
        # So finding the match with the largest .end() is the strategy.
        for pattern in start_patterns[2:]:
             # Find all matches in the first chunk
             # But re.search only finds the first one.
             # If we want to catch "line 3", we need to search the whole first chunk?
             # re.search searches the whole string.

             match = re.search(pattern, content, re.IGNORECASE)
             if match and match.start() < 2000:
                 start_idx = max(start_idx, match.end())

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            end_idx = min(end_idx, match.start())

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
files = [
    "social_contract.txt",
    "emile.txt",
    "confessions.txt"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        clean_gutenberg_text(filepath)
    else:
        print(f"File not found: {filepath}")
