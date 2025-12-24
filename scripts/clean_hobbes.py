
import os

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1:
        print(f"Warning: Start marker not found in {filepath}")
    else:
        # Move past the marker
        start_idx += len(start_marker)

    if end_idx == -1:
        print(f"Warning: End marker not found in {filepath}")

    if start_idx != -1 and end_idx != -1:
        content = content[start_idx:end_idx]

        # Further refinement to skip transcriber notes if present
        # Looking at the file content, there are "TRANSCRIBER’S NOTES ON THE E-TEXT"
        # and then "THE INTRODUCTION".
        # Let's try to find the start of the actual text or Introduction.

        real_start_marker = "THE INTRODUCTION"
        real_start_idx = content.find(real_start_marker)
        if real_start_idx != -1:
             content = content[real_start_idx:]

        # Strip leading/trailing whitespace
        content = content.strip()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully cleaned {filepath}")
    else:
        print(f"Could not clean {filepath} properly due to missing markers.")

if __name__ == "__main__":
    filepath = "socials_data/personalities/thomas_hobbes/raw/leviathan.txt"
    if os.path.exists(filepath):
        clean_file(filepath)
    else:
        print(f"File not found: {filepath}")
