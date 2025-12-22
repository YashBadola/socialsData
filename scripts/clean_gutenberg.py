import re
import sys
from pathlib import Path

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from text.
    Also attempts to remove translator introductions if standard markers are found.
    """
    lines = text.splitlines()
    start_marker_idx = -1
    end_marker_idx = -1

    # Standard Gutenberg markers
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK",
    ]

    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK",
    ]

    for i, line in enumerate(lines):
        for pattern in start_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                start_marker_idx = i
                break
        if start_marker_idx != -1:
            break

    # If standard start not found, try to find the title/author block end
    if start_marker_idx == -1:
        # Fallback: look for empty lines after a block of metadata?
        # Or just keep it as is if we can't find the marker.
        pass

    # Search for end marker from the end
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        for pattern in end_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                end_marker_idx = i
                break
        if end_marker_idx != -1:
            break

    start_content = 0
    if start_marker_idx != -1:
        start_content = start_marker_idx + 1

    end_content = len(lines)
    if end_marker_idx != -1:
        end_content = end_marker_idx

    cleaned_lines = lines[start_content:end_content]

    # Strip leading empty lines
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)

    # Strip trailing empty lines
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    return "\n".join(cleaned_lines)

def process_file(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return

    print(f"Processing {filepath}...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = clean_gutenberg_text(content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_gutenberg.py <file1> [file2 ...]")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        process_file(file_path)
