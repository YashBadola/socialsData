import os
import re

def clean_gutenberg_text(filepath, start_marker=None):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
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

    if start_idx == 0:
        print("Warning: Start marker not found.")
    if end_idx == len(content):
        print("Warning: End marker not found.")

    # Initial clean based on stars
    text = content[start_idx:end_idx].strip()

    # Additional custom cleaning if start_marker is provided
    if start_marker:
        marker_idx = text.find(start_marker)
        if marker_idx != -1:
             print(f"Found custom start marker: '{start_marker}'")
             text = text[marker_idx:]
        else:
             print(f"Warning: Custom start marker '{start_marker}' not found.")

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

def main():
    base_dir = "socials_data/personalities/bertrand_russell/raw"

    # Map filename to optional custom start marker
    files = {
        "problems_of_philosophy.txt": "THE PROBLEMS OF PHILOSOPHY",
        "analysis_of_mind.txt": "THE ANALYSIS OF MIND",
        "mysticism_and_logic.txt": "MYSTICISM AND LOGIC"
    }

    for filename, start_marker in files.items():
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_gutenberg_text(filepath, start_marker)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
