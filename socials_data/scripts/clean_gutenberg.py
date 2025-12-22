import re
import argparse

def clean_gutenberg_text(text):
    """
    Strips standard Project Gutenberg headers and footers.
    """
    lines = text.splitlines()

    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK",
    ]

    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK",
    ]

    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        for marker in start_markers:
            if re.search(marker, line, re.IGNORECASE):
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Search for end marker, starting from the end
    for i in range(len(lines) - 1, start_idx, -1):
        line = lines[i]
        for marker in end_markers:
            if re.search(marker, line, re.IGNORECASE):
                end_idx = i
                break
        if end_idx < len(lines):
            break

    # Also strip some common transcribers notes if they appear right after start
    # or look for "Produced by"

    content = lines[start_idx:end_idx]

    # Strip leading empty lines
    while content and not content[0].strip():
        content.pop(0)

    # Strip trailing empty lines
    while content and not content[-1].strip():
        content.pop()

    return "\n".join(content)

def main():
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg texts.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to the output text file.")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned_text = clean_gutenberg_text(text)

        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Cleaned {args.input_file} -> {args.output_file}")

    except Exception as e:
        print(f"Error cleaning file: {e}")

if __name__ == "__main__":
    main()
