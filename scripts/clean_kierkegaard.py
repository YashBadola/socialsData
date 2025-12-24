import os

def clean_text(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        text = f.read()

    # Find start and end markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK SELECTIONS FROM THE WRITINGS OF KIERKEGAARD ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SELECTIONS FROM THE WRITINGS OF KIERKEGAARD ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1:
        # Fallback to a simpler marker if the specific one isn't found
        start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
        start_idx = text.find(start_marker)

    if end_idx == -1:
         # Fallback to a simpler marker
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
        end_idx = text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"Warning: Could not find standard Gutenberg markers in {filepath}. Start: {start_idx}, End: {end_idx}")
        # Try finding the start of the actual text "INTRODUCTION"
        start_marker = "INTRODUCTION"
        start_idx = text.find(start_marker)
        if start_idx == -1:
             print("Could not find content start.")
             return

    # Adjust start index to skip the marker itself
    if start_idx != -1:
         # Find the line "INTRODUCTION" which seems to be the start of the content based on `head` output
         # The header ends, then some metadata, then "INTRODUCTION"
         # Let's look for "INTRODUCTION" after the Gutenberg header
         pass

    # Extract content
    # For this specific file, there is a lot of front matter.
    # Let's look at the head output again.
    # It has "INTRODUCTION" followed by "I".
    # But let's just stick to the Gutenberg markers first to be safe, then maybe refine.

    if start_idx != -1 and end_idx != -1:
        content = text[start_idx + len(start_marker):end_idx].strip()
    elif start_idx != -1:
        content = text[start_idx + len(start_marker):].strip()
    else:
        content = text

    # Remove the translator's introduction if possible, or just keep it as it provides context.
    # The memory says "first isolating content between the standard Gutenberg headers and footers, then refining the start index by searching for a specific internal marker... to remove translator introductions".
    # The `head` shows "INTRODUCTION". It is likely the translator's introduction.
    # The `head` also shows "I DIAPSALMATA".
    # Let's try to find "DIAPSALMATA" as the start of Kierkegaard's text.

    real_start_marker = "DIAPSALMATA"
    real_start_idx = content.find(real_start_marker)
    if real_start_idx != -1:
        print(f"Found real start marker '{real_start_marker}' at index {real_start_idx}. Trimming introduction.")
        content = content[real_start_idx:].strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaning complete.")

if __name__ == "__main__":
    filepath = "socials_data/personalities/soren_kierkegaard/raw/selections.txt"
    if os.path.exists(filepath):
        clean_text(filepath)
    else:
        print(f"File not found: {filepath}")
