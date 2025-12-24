import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1

    # Find start marker
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
            break

    # Find end marker
    for i, line in enumerate(lines):
        if end_marker in line:
            end_idx = i
            # If we found a start marker, ensure end marker is after it
            if start_idx != -1 and end_idx > start_idx:
                break

    if start_idx == -1:
        print(f"Warning: Start marker '{start_marker}' not found in {filepath}")
        return

    if end_idx == -1:
        print(f"Warning: End marker '{end_marker}' not found in {filepath}")
        end_idx = len(lines)

    # Use content between markers
    cleaned_content = "".join(lines[start_idx:end_idx])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {filepath}")

def clean_aristotle():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "socials_data", "personalities", "aristotle", "raw")

    # Nicomachean Ethics
    # Use a unique sentence near the start to avoid TOC matches for "BOOK I"
    ethics_path = os.path.join(raw_dir, "nicomachean_ethics.txt")
    clean_file(
        ethics_path,
        "Every art, and every science reduced to a teachable form",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***"
    )

    # Politics
    # Use "BOOK I" but handle the specific case for Politics where we want the main text
    # The simple cleaner might pick up "BOOK I" from TOC if present, but for Politics
    # the TOC is structure differently or absent in a way that "BOOK I" works well enough
    # if we verify it.
    # To be safer, we can check for the Chapter I marker as well, but for simplicity
    # and given I've already verified the previous run, I'll stick to a robust enough marker.
    # The previous run logic was more complex, I will simplify but keep the robustness.

    # Re-implementing the specific check for Politics to be safe
    politics_path = os.path.join(raw_dir, "politics.txt")
    with open(politics_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = -1
    for i in range(len(lines)):
        if "BOOK I" in lines[i]:
            # Check for CHAPTER I nearby to confirm it's the start of text
            found_chap = False
            for j in range(1, 10):
                if i+j < len(lines) and "CHAPTER I" in lines[i+j]:
                    found_chap = True
                    break
            if found_chap:
                start_idx = i
                break

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***"
    end_idx = -1
    for i in range(len(lines)):
        if end_marker in lines[i]:
            end_idx = i
            break

    if start_idx != -1 and end_idx != -1:
        cleaned = "".join(lines[start_idx:end_idx])
        with open(politics_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"Cleaned {politics_path}")
    else:
        print(f"Warning: Markers not found for Politics in {politics_path}")

    # Poetics
    poetics_path = os.path.join(raw_dir, "poetics.txt")
    clean_file(
        poetics_path,
        "ARISTOTLE'S POETICS",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***"
    )

if __name__ == "__main__":
    clean_aristotle()
