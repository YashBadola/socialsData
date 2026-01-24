import re
from pathlib import Path

def split_text():
    raw_dir = Path("socials_data/personalities/soren_kierkegaard/raw")
    full_text_path = raw_dir / "full_text.txt"

    with open(full_text_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define sections
    # Using regex to find the start of sections
    sections = [
        ("introduction.txt", r"INTRODUCTION I\s+\n"),
        ("diapsalmata.txt", r"DIAPSALMATA\[1\]"),
        ("in_vino_veritas.txt", r"IN VINO VERITAS \(THE BANQUET\)\s+\n"),
        ("fear_and_trembling.txt", r"FEAR AND TREMBLING\s+\n"),
        ("preparation_for_christian_life.txt", r"PREPARATION FOR A CHRISTIAN LIFE\s+\n"),
        ("the_present_moment.txt", r"THE PRESENT MOMENT\[1\]")
    ]

    # We will iterate and find indices
    indices = []
    for filename, pattern in sections:
        match = re.search(pattern, content)
        if match:
            indices.append((match.start(), filename))
        else:
            print(f"Warning: Could not find section for {filename} using pattern '{pattern}'")

    # Sort indices
    indices.sort()

    # Write files
    for i in range(len(indices)):
        start_idx, filename = indices[i]

        # Determine end index
        if i < len(indices) - 1:
            end_idx = indices[i+1][0]
        else:
            end_idx = len(content) # Until the end
            # Optionally stop before End of Project Gutenberg
            end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", content)
            if end_match:
                 end_idx = min(end_idx, end_match.start())

        section_content = content[start_idx:end_idx].strip()

        output_path = raw_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(section_content)

        print(f"Wrote {filename} ({len(section_content)} chars)")

if __name__ == "__main__":
    split_text()
