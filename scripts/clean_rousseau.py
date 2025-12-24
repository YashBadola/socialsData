import os

def clean_text(filepath, start_marker, end_marker, output_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break # Stop after first end marker to avoid license at end

    if start_index == -1:
        print(f"Warning: Start marker '{start_marker}' not found in {filepath}")
        return
    if end_index == -1:
        # Fallback to check for "END OF THE PROJECT GUTENBERG" if specific marker not found
        # Or just use the end of file but warn
        print(f"Warning: End marker '{end_marker}' not found in {filepath}. Looking for generic footer.")
        for i in range(len(lines) - 1, start_index, -1):
            if "END OF THE PROJECT GUTENBERG" in lines[i]:
                end_index = i
                break
        if end_index == -1:
             print(f"Error: Could not find end marker in {filepath}")
             return

    # Extract content, skipping the marker lines themselves
    content = lines[start_index + 1 : end_index]

    # Optional: Additional trimming of whitespace/empty lines at start/end
    while content and not content[0].strip():
        content.pop(0)
    while content and not content[-1].strip():
        content.pop()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Cleaned {filepath} -> {output_path}")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"

# Define markers based on inspection
# Social Contract:
# Start: "*** START OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***"
# End: "*** END OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***"
# Note: There is some front matter (Title, publisher) after the start marker.
# I can refine the start marker to "THE SOCIAL CONTRACT & DISCOURSES" but that appears twice.
# Let's use the standard PG markers for the first pass, as the 'process' tool chunks everything.
# However, to be cleaner, I should probably skip the "Produced by..." lines.
# But standard PG markers are safe enough.

tasks = [
    {
        "file": "social_contract_and_discourses.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***"
    },
    {
        "file": "confessions.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***"
    },
    {
        "file": "emile.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK EMILE ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK EMILE ***"
    }
]

for task in tasks:
    input_p = os.path.join(base_dir, task["file"])
    # Overwrite in place or create new? The plan said "overwrite the files in raw/ with the clean versions".
    # But usually it's safer to have a distinct clean file or just overwrite if we are sure.
    # I'll overwrite to keep it simple as per plan.
    clean_text(input_p, task["start"], task["end"], input_p)
