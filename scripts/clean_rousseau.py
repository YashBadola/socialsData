
import os

def clean_file(filepath, start_marker, end_marker, content_start_marker=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1

    # First pass: find Gutenberg markers
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
        if end_marker in line:
            end_idx = i
            break # Stop at first end marker found

    if start_idx == -1 or end_idx == -1:
        print(f"Warning: Markers not found in {filepath}. Start: {start_idx}, End: {end_idx}")
        return

    # Refine start index if content_start_marker is provided
    # IMPORTANT: We want to exclude the marker itself, so we start AFTER it.
    if content_start_marker:
        found_content_start = False
        for i in range(start_idx, end_idx):
            if content_start_marker in lines[i]:
                start_idx = i
                found_content_start = True
                break
        if not found_content_start:
             print(f"Warning: Content start marker '{content_start_marker}' not found in {filepath}. Using Gutenberg start.")
             start_idx += 1 # Skip the Gutenberg start marker line
    else:
        # Default behavior: skip the marker line itself
        start_idx += 1

    # Safety check: if start_idx still points to a line containing Gutenberg marker or "Produced by"
    # we want to skip forward until we hit real text or the content start marker.
    # But if we used content_start_marker, we are probably at the Title.

    # If content_start_marker was NOT used (or not found), we might have "Produced by..." right after Gutenberg marker.
    # Let's check for "Produced by" in the first few lines of the candidate content and skip them.
    # We only scan a small window (e.g., 20 lines) to avoid skipping real content.

    scan_limit = min(start_idx + 20, end_idx)
    for i in range(start_idx, scan_limit):
        line_strip = lines[i].strip()
        if not line_strip:
            continue
        if "Produced by" in lines[i] or "Start of the Project Gutenberg" in lines[i] or "*** START OF" in lines[i]:
             start_idx = i + 1
        else:
            # We found a non-empty line that doesn't look like boilerplate. Stop skipping.
            # But wait, sometimes there are multiple "Produced by" lines or blank lines.
            # The logic above advances start_idx every time it sees "Produced by".
            # If we see a real line, we break.
            break

    # Also ensure we don't include the start marker line itself if we didn't move past it
    if start_idx < len(lines) and (start_marker in lines[start_idx] or "*** START OF" in lines[start_idx]):
        start_idx += 1

    cleaned_lines = lines[start_idx:end_idx]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    print(f"Cleaned {filepath}")

def main():
    base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"

    # Define markers for each file
    files = [
        {
            "name": "the_social_contract_and_discourses.txt",
            "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***",
            "content_start": "THE SOCIAL CONTRACT & DISCOURSES"
        },
        {
            "name": "confessions.txt",
            "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***",
            "content_start": "THE CONFESSIONS OF JEAN JACQUES ROUSSEAU"
        },
        {
            "name": "emile.txt",
            "start": "*** START OF THE PROJECT GUTENBERG EBOOK EMILE ***",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK EMILE ***",
            "content_start": "EMILE"
        }
    ]

    for file_info in files:
        filepath = os.path.join(base_dir, file_info["name"])
        if os.path.exists(filepath):
            clean_file(filepath, file_info["start"], file_info["end"], file_info.get("content_start"))
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
