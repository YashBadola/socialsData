import os
from pathlib import Path

def clean_file(filepath, start_markers, end_markers, extra_start_skip_lines=0):
    print(f"Cleaning {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return

    start_index = 0
    end_index = len(lines)

    # Find start marker
    for i, line in enumerate(lines):
        for marker in start_markers:
            if marker in line:
                start_index = i + 1 + extra_start_skip_lines
                print(f"Found start marker at line {i+1}: '{marker.strip()}'")
                break
        if start_index != 0:
            break

    # Find end marker
    for i, line in enumerate(lines):
        for marker in end_markers:
            if marker in line:
                end_index = i
                print(f"Found end marker at line {i+1}: '{marker.strip()}'")
                break
        if end_index != len(lines):
            break

    if start_index == 0:
        print("Warning: Start marker not found. Using beginning of file.")
    if end_index == len(lines):
        print("Warning: End marker not found. Using end of file.")

    cleaned_content = "".join(lines[start_index:end_index]).strip()

    if not cleaned_content:
         print(f"Warning: Cleaned content is empty for {filepath}")
         return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath} (kept lines {start_index} to {end_index}).")


def main():
    base_dir = Path("socials_data/personalities/immanuel_kant/raw")

    # Critique of Pure Reason
    clean_file(
        base_dir / "critique_of_pure_reason.txt",
        start_markers=["*** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"]
    )

    # Critique of Practical Reason
    clean_file(
        base_dir / "critique_of_practical_reason.txt",
        start_markers=["*** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PRACTICAL REASON ***"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PRACTICAL REASON ***"]
    )

    # Critique of Judgement
    clean_file(
        base_dir / "critique_of_judgement.txt",
        start_markers=["*** START OF THE PROJECT GUTENBERG EBOOK KANT'S CRITIQUE OF JUDGEMENT ***"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK KANT'S CRITIQUE OF JUDGEMENT ***"]
    )

    # Fundamental Principles of the Metaphysic of Morals
    clean_file(
        base_dir / "metaphysic_of_morals.txt",
        start_markers=["*** START OF THE PROJECT GUTENBERG EBOOK FUNDAMENTAL PRINCIPLES OF THE METAPHYSIC OF MORALS ***"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK FUNDAMENTAL PRINCIPLES OF THE METAPHYSIC OF MORALS ***"]
    )

if __name__ == "__main__":
    main()
