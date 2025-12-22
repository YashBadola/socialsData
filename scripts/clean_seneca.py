import re
import sys

def clean_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start and end of the actual text
    # Project Gutenberg usually marks start with "*** START OF THIS PROJECT GUTENBERG EBOOK ..."
    # and end with "*** END OF THIS PROJECT GUTENBERG EBOOK ..."

    start_marker = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content)
    end_marker = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content)

    if start_marker:
        start_index = start_marker.end()
        content = content[start_index:]

    if end_marker:
        end_index = end_marker.start()
        content = content[:end_index] # Since we sliced start, the end index is relative to the ORIGINAL string, but wait.
        # If we slice start first, the indices shift.
        # Let's do it cleanly.

    # Re-read to be safe and use indices relative to original string
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content)
    end_marker = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content)

    start_idx = 0
    end_idx = len(content)

    if start_marker:
        start_idx = start_marker.end()

    if end_marker:
        end_idx = end_marker.start()

    text = content[start_idx:end_idx]

    # Additional cleaning: remove Sir Roger L'Estrange's intro if present
    # The snippet showed "The opening portion provides a preface by ... Sir Roger L'Estrange"
    # Let's inspect the file first to be sure, but general cleaning:

    # Remove excessive newlines
    lines = [line.rstrip() for line in text.splitlines()]

    # Remove lines that look like Table of Contents or Headers if easy to identify
    # For now, just basic cleaning.

    cleaned_text = '\n'.join(lines).strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_text(sys.argv[1])
    else:
        print("Usage: python clean_seneca.py <filepath>")
