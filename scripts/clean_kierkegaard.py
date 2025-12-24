import re
from pathlib import Path

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Find the start and end of the actual text
    # Start marker based on the file content inspection
    start_marker = "INTRODUCTION I"
    end_marker = "End of the Project Gutenberg eBook"

    # Fallback end marker
    if end_marker not in content:
        # Try to find the standard license end if the specific one is missing
        # Based on the tail output, it ends with standard license info.
        # Often PG texts end before the license.
        # Let's look for a marker before the license.
        pass

    # Actually, let's use the standard PG markers if possible, but refining it.
    # The head shows: *** START OF THE PROJECT GUTENBERG EBOOK ... ***
    # Then "UNIVERSITY OF TEXAS BULLETIN..."
    # Then "INTRODUCTION I" seems to be the start of the actual content.

    # The tail shows the license.
    # Usually there is an "END OF THE PROJECT GUTENBERG EBOOK" line.
    # Let's search for it.

    start_idx = content.find(start_marker)
    if start_idx == -1:
        # Fallback to standard start
        print(f"Warning: Specific start marker '{start_marker}' not found. Using standard PG start.")
        match = re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', content)
        if match:
            start_idx = match.end()
        else:
            start_idx = 0

    # For end marker, we can look for the license start
    end_idx = content.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if end_idx == -1:
         end_idx = content.find("End of the Project Gutenberg eBook")

    if end_idx == -1:
        # Look for the license footer start
        match = re.search(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', content)
        if match:
            end_idx = match.start()
        else:
            # Try finding the license section
            end_idx = content.find("End of the Project Gutenberg eBook")

    if end_idx != -1:
        content = content[start_idx:end_idx]
    else:
        content = content[start_idx:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    base_dir = Path("socials_data/personalities/soren_kierkegaard/raw")
    clean_file(base_dir / "selections.txt")
