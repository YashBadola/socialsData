import os
import requests
import re

def main():
    url = "https://www.gutenberg.org/cache/epub/59/pg59.txt"
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    text = response.text

    # Basic cleaning of Gutenberg header/footer
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_pos = text.find(start_marker)
    if start_pos != -1:
        # Find the end of that line
        newline_pos = text.find("\n", start_pos)
        text = text[newline_pos+1:]

    end_pos = text.find(end_marker)
    if end_pos != -1:
        text = text[:end_pos]

    output_dir = "socials_data/personalities/rene_descartes/raw"
    os.makedirs(output_dir, exist_ok=True)

    # Regex to find the headers. They seem to be on their own lines.
    # We look for "PART X" or "PREFATORY NOTE BY THE AUTHOR" surrounded by newlines or start of string.
    # The Gutenberg text has CRLF or LF.

    # Let's try to split by these headers.
    # Note: re.split with capturing group returns [pre_match, separator, post_match, separator, ...]

    pattern = r'(\r?\n\s*(?:PART [IV]+|PREFATORY NOTE BY THE AUTHOR)\s*\r?\n)'

    parts = re.split(pattern, text)

    # parts[0] is everything before the first header (Title, Contents, etc.)
    # parts[1] is the first header (e.g. "\nPREFATORY NOTE BY THE AUTHOR\n")
    # parts[2] is the content of that section
    # parts[3] is the second header
    # parts[4] is the content of that section

    print(f"Found {len(parts)} segments (should be odd).")

    # Mapping for filenames
    name_map = {
        "PREFATORY NOTE BY THE AUTHOR": "prefatory_note.txt",
        "PART I": "part_1.txt",
        "PART II": "part_2.txt",
        "PART III": "part_3.txt",
        "PART IV": "part_4.txt",
        "PART V": "part_5.txt",
        "PART VI": "part_6.txt"
    }

    for i in range(1, len(parts), 2):
        header_raw = parts[i]
        content = parts[i+1].strip()

        header_clean = header_raw.strip()

        filename = name_map.get(header_clean)
        if not filename:
            print(f"Warning: Unknown header '{header_clean}'. Saving as unknown_{i}.txt")
            filename = f"unknown_{i}.txt"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header_clean + "\n\n" + content)
        print(f"Wrote {filepath} ({len(content)} chars)")

if __name__ == "__main__":
    main()
