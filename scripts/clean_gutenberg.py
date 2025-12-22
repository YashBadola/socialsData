import re
import sys
import argparse
from pathlib import Path

def clean_gutenberg_text(text):
    """
    Strips standard Project Gutenberg headers and footers.
    """
    # This is a heuristic. Gutenberg texts usually start with "*** START OF THIS PROJECT GUTENBERG EBOOK ..."
    # and end with "*** END OF THIS PROJECT GUTENBERG EBOOK ...".

    start_marker_pattern = re.compile(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?(\*\*\*|$)", re.IGNORECASE | re.MULTILINE)
    end_marker_pattern = re.compile(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?(\*\*\*|$)", re.IGNORECASE | re.MULTILINE)

    start_match = start_marker_pattern.search(text)
    end_match = end_marker_pattern.search(text)

    start_pos = 0
    end_pos = len(text)

    if start_match:
        start_pos = start_match.end()

    if end_match:
        end_pos = end_match.start()

    cleaned_text = text[start_pos:end_pos].strip()

    # Sometimes there is additional legalese or prologues that are part of the Gutenberg file but not the text.
    # However, for now, stripping the main markers is the standard procedure.
    # We might want to look for "Produced by ..." lines at the start.

    return cleaned_text

def main():
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg text files.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to save the cleaned text file.")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    if not input_path.exists():
        print(f"Error: File {input_path} does not exist.")
        sys.exit(1)

    try:
        content = input_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback for some Gutenberg files
        content = input_path.read_text(encoding='latin-1')

    cleaned = clean_gutenberg_text(content)

    # Some texts have 'Produced by ...' right after the header.
    # We can try to strip lines until we hit the title or Chapter 1, but that's risky.
    # For now, let's just strip the Gutenberg markers.

    output_path.write_text(cleaned, encoding='utf-8')
    print(f"Cleaned text written to {output_path}")

if __name__ == "__main__":
    main()
