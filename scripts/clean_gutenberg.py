import re
import sys

def clean_gutenberg_text(text):
    """
    Strips Project Gutenberg headers and footers from text.
    """
    # Common start markers
    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
    ]

    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines):
        for marker in start_markers:
            if re.search(marker, line):
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Find end
    for i, line in enumerate(lines):
        for marker in end_markers:
            if re.search(marker, line):
                end_idx = i
                break
        # Don't break immediately to find the *last* occurrence if multiple?
        # Actually usually the first end marker after start is correct.
        if end_idx < len(lines):
            break

    # If we found markers, trim. If not, return original (or partial).
    if start_idx < end_idx:
        return "\n".join(lines[start_idx:end_idx]).strip()
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_gutenberg.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = clean_gutenberg_text(content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        print(f"Cleaned {file_path}")
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")
