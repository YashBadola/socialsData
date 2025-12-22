import os
import re
import sys
import glob

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from text.
    Based on common markers.
    """
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Common start markers
    start_markers = [
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
        "***START OF THIS PROJECT GUTENBERG EBOOK"
    ]

    # Common end markers
    end_markers = [
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
        "***END OF THIS PROJECT GUTENBERG EBOOK",
        "End of the Project Gutenberg EBook",
        "End of Project Gutenberg's"
    ]

    # Find start
    for i, line in enumerate(lines):
        for marker in start_markers:
            if marker.lower() in line.lower():
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Find end
    for i, line in enumerate(lines):
        if i < start_idx: continue
        for marker in end_markers:
            if marker.lower() in line.lower():
                end_idx = i
                break
        if end_idx < len(lines):
            break

    cleaned_lines = lines[start_idx:end_idx]

    # Trim empty lines from start and end
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    return "\n".join(cleaned_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_gutenberg.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    files = glob.glob(os.path.join(target_dir, "*.txt"))

    if not files:
        print(f"No .txt files found in {target_dir}")
        return

    print(f"Found {len(files)} files in {target_dir}")

    for filepath in files:
        print(f"Cleaning {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_gutenberg_text(content)

            # Simple check to see if we actually removed something
            if len(cleaned_content) < len(content):
                print(f"  Removed {len(content) - len(cleaned_content)} characters.")
                # Overwrite the file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
            else:
                print("  No changes made (markers not found?).")

        except Exception as e:
            print(f"  Error processing {filepath}: {e}")

if __name__ == "__main__":
    main()
