import re
import sys

def clean_text(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Find the start of the content (after START OF THE PROJECT GUTENBERG EBOOK)
    # The header usually ends with "*** START OF THE PROJECT GUTENBERG EBOOK ETHICS ***" or similar
    # But let's look for "ETHICS" as the main title start after metadata.

    # Actually, Gutenberg headers end with "*** START OF THE PROJECT GUTENBERG EBOOK ... ***"
    start_marker = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    if start_marker:
        text = text[start_marker.end():]
    else:
        print("Warning: Start marker not found.")

    # Find the end (before END OF THE PROJECT GUTENBERG EBOOK)
    end_marker = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    if end_marker:
        text = text[:end_marker.start()]
    else:
        # Fallback for old footer
        end_marker = re.search(r"End of the Project Gutenberg EBook", text, re.IGNORECASE)
        if end_marker:
            text = text[:end_marker.start()]
        else:
             print("Warning: End marker not found.")

    # Remove extra newlines or specific artifacts if needed.
    # Spinoza's Ethics has parts like "PART I." "PART II." etc.
    # We can try to strip potential translator intros if they are massive, but typically Gutenberg is just the text + license.
    # The current text seems to start with "ETHICS" and then "PART I".

    # Let's remove any leading whitespace
    text = text.strip()

    # Save cleaned text
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Cleaned text saved to {output_path}")

if __name__ == "__main__":
    clean_text("socials_data/personalities/baruch_spinoza/raw/ethics.txt", "socials_data/personalities/baruch_spinoza/raw/ethics.txt")
