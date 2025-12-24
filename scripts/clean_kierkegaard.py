import os

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Find Gutenberg markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK SELECTIONS FROM THE WRITINGS OF KIERKEGAARD ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SELECTIONS FROM THE WRITINGS OF KIERKEGAARD ***"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Markers not found, checking generic markers...")
        if start_idx == -1:
            start_idx = content.find("*** START OF THIS PROJECT GUTENBERG EBOOK")
        if end_idx == -1:
            end_idx = content.find("*** END OF THIS PROJECT GUTENBERG EBOOK")

    if start_idx == -1 or end_idx == -1:
        print("Could not find Gutenberg markers.")
        return

    content = content[start_idx + len(start_marker):end_idx]

    # Refine start to skip intro/TOC
    # We look for the second occurrence of "DIAPSALMATA" which marks the beginning of the text
    # The first one is in the TOC
    # Based on grep output: 85 is TOC, 1257 is start of text.

    # Let's find "DIAPSALMATA[1]" which seems to be the header of the section
    real_start_marker = "DIAPSALMATA[1]"
    real_start_idx = content.find(real_start_marker)

    if real_start_idx != -1:
        print(f"Found real start at index {real_start_idx}")
        content = content[real_start_idx:]
    else:
        print("Could not find real start marker 'DIAPSALMATA[1]', using Gutenberg start.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    filepath = "socials_data/personalities/soren_kierkegaard/raw/selections.txt"
    if os.path.exists(filepath):
        clean_file(filepath)
    else:
        print(f"File not found: {filepath}")
