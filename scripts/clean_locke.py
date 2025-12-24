import os

def clean_file(filepath, start_marker, end_marker, actual_start_marker=None):
    print(f"Cleaning {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Failed to read {filepath} with utf-8, trying latin-1")
        with open(filepath, 'r', encoding='latin-1') as f:
            lines = f.readlines()

    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
        if end_marker in line:
            end_idx = i
            break

    if start_idx == -1 or end_idx == -1:
        print(f"Markers not found in {filepath}. Start: {start_idx}, End: {end_idx}")
        return

    content = lines[start_idx+1:end_idx]

    # Optional second pass for actual start
    if actual_start_marker:
        real_start_idx = -1
        for i, line in enumerate(content):
            if actual_start_marker in line:
                real_start_idx = i
                break
        if real_start_idx != -1:
            content = content[real_start_idx:]

    # Remove empty lines from beginning and end
    while content and not content[0].strip():
        content.pop(0)
    while content and not content[-1].strip():
        content.pop()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Cleaned {filepath}")

base_path = "socials_data/personalities/john_locke/raw"

# File 1: Second Treatise
clean_file(
    os.path.join(base_path, "second_treatise_of_government.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK SECOND TREATISE OF GOVERNMENT ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK SECOND TREATISE OF GOVERNMENT ***",
    actual_start_marker="SECOND TREATISE OF GOVERNMENT"
)

# File 2: Essay Vol 1
clean_file(
    os.path.join(base_path, "essay_human_understanding_vol1.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK AN ESSAY CONCERNING HUMANE UNDERSTANDING, VOLUME 1 ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK AN ESSAY CONCERNING HUMANE UNDERSTANDING, VOLUME 1 ***",
    actual_start_marker="An Essay Concerning Humane Understanding"
)

# File 3: Essay Vol 2
clean_file(
    os.path.join(base_path, "essay_human_understanding_vol2.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK AN ESSAY CONCERNING HUMANE UNDERSTANDING, VOLUME 2 ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK AN ESSAY CONCERNING HUMANE UNDERSTANDING, VOLUME 2 ***",
    actual_start_marker="AN ESSAY CONCERNING HUMAN UNDERSTANDING"
)
