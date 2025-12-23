import os

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line or "*** START OF THIS PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
            break

    # Find end
    for i, line in enumerate(lines):
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line or "*** END OF THIS PROJECT GUTENBERG EBOOK" in line:
            end_idx = i
            break

    content = "".join(lines[start_idx:end_idx]).strip()

    # Simple check to remove potential preamble if "Produced by" repeats or similar,
    # but the marker is usually reliable enough for a first pass.
    # However, let's look for the actual title again to skip "Produced by..." headers if they appear after the marker.

    # Only write back if we found content
    if content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {filepath}. Size: {len(content)} chars.")
    else:
        print(f"Warning: No content found for {filepath}")

def main():
    base_dir = "socials_data/personalities/plato/raw"
    files = ["the_republic.txt", "symposium.txt", "apology.txt"]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
