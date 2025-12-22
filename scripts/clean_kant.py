import os

def clean_kant():
    filepath = 'socials_data/personalities/immanuel_kant/raw/critique_of_pure_reason.txt'
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    # Find the start of the preface, which is the start of the actual content
    for i, line in enumerate(lines):
        if "PREFACE TO THE FIRST EDITION 1781" in line:
            start_index = i
            break

    # Fallback if specific header not found
    if start_index == -1:
        print("Warning: Specific start marker not found. Falling back to generic Gutenberg start.")
        for i, line in enumerate(lines):
            if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
                start_index = i + 1
                break

    # Find the end of the book
    for i, line in enumerate(lines):
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        cleaned_lines = lines[start_index:end_index]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        print(f"Cleaned {filepath}. Kept lines {start_index} to {end_index}.")
    else:
        print(f"Could not find start ({start_index}) or end ({end_index}) markers.")

if __name__ == "__main__":
    clean_kant()
