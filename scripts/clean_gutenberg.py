import re
import sys
import os

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from text.
    """
    # Common header patterns
    # We look for the standard start lines.
    # Example: *** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***
    header_patterns = [
        r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        r"\*\*\*\s*START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common footer patterns
    # Example: *** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***
    footer_patterns = [
        r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK",
    ]

    start_idx = 0
    end_idx = len(text)

    # Find end of header
    for pattern in header_patterns:
        # We use DOTALL so . matches newlines, but we use *? for non-greedy match
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            print(f"Found header match: {match.group(0)[:50]}... at {match.start()}-{match.end()}")
            # We want the last occurrence of the start header if there are multiple,
            # but usually the first "START OF ..." is the right one after the small license preamble.
            # Actually, sometimes the small license preamble also contains "Project Gutenberg".
            # The standard marker is usually explicit.
            # Let's trust the first match of the specific "*** START OF..." pattern.
            start_idx = match.end()
            break # Stop after finding the first valid header marker

    # Find start of footer
    for pattern in footer_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"Found footer match: {match.group(0)[:50]}... at {match.start()}-{match.end()}")
            end_idx = match.start()
            break # Stop after finding the first valid footer marker

    if start_idx >= end_idx:
        print(f"Warning: start_idx ({start_idx}) >= end_idx ({end_idx}). Returning full text or empty.")
        # Fallback: if we matched nothing reasonable, maybe return the whole text or try to be smarter.
        # But if we matched a header after a footer (unlikely) or overlapping, something is wrong.
        if start_idx == 0 and end_idx == len(text):
            return text
        return ""

    clean_text = text[start_idx:end_idx].strip()
    return clean_text

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original length: {len(content)}")
    cleaned_content = clean_gutenberg_text(content)

    # Remove excessive newlines
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    if len(cleaned_content) == 0:
        print("Error: Cleaned content is empty!")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filepath}. New length: {len(cleaned_content)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/clean_gutenberg.py <file1> <file2> ...")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print(f"File not found: {file_path}")
