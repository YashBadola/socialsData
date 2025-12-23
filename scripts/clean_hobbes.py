
import os

def clean_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Define markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"

    # Find markers
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1:
        print(f"Error: Start marker not found in {filepath}")
        return
    if end_idx == -1:
        print(f"Error: End marker not found in {filepath}")
        return

    # Adjust start index to skip the marker
    start_idx += len(start_marker)

    # Extract content
    text = content[start_idx:end_idx].strip()

    # Additional cleanup: Remove the "LEVIATHAN" title block and Transcriber notes if possible
    # Searching for "Introduction" or the start of the actual text
    # Looking at the file content:
    # "LEVIATHAN By Thomas Hobbes 1651... TRANSCRIBER’S NOTES... Paris APRILL 15/25 1651. CONTENTS..."
    # The actual text effectively starts after the intro or table of contents.
    # However, keeping the front matter (To my most honor'd friend...) is usually fine.
    # But looking at "Introduction" might be a good start point.
    # Let's keep the title page and contents for context, just strip the Gutenberg metadata.

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Successfully cleaned {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/thomas_hobbes/raw"
    filepath = os.path.join(base_dir, "leviathan.txt")
    if os.path.exists(filepath):
        clean_file(filepath)
    else:
        print(f"File not found: {filepath}")
