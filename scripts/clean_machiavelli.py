
import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
            break

    # If specific start marker not found, fallback to Gutenberg start
    if start_idx == -1:
        for i, line in enumerate(lines):
             if "*** START OF THE PROJECT" in line:
                 start_idx = i + 1
                 break

    # Search for end marker (reverse)
    for i in range(len(lines) - 1, -1, -1):
        if end_marker in lines[i]:
            end_idx = i
            break

    if start_idx != -1 and end_idx != -1:
        cleaned_content = "".join(lines[start_idx:end_idx])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filepath}")
    else:
        print(f"Markers not found for {filepath}: Start {start_idx}, End {end_idx}")

base_path = "socials_data/personalities/niccolo_machiavelli/raw/"

# The Prince
# DEDICATION seems to be the start of the content, but let's check if there is content before.
# The `sed` output showed "DEDICATION" then "THE PRINCE".
# Actually "NICOLO MACHIAVELLI" is usually at the top.
# Let's use "DEDICATION" for The Prince as it is the first meaningful header after the table of contents (Wait, the sed output shows DEDICATION then table of contents).
# Actually, usually we want to keep the text body.
# "DEDICATION" is fine.
clean_file(
    os.path.join(base_path, "the_prince.txt"),
    "DEDICATION",
    "*** END OF THE PROJECT"
)

# Discourses
# "BOOK I." is line 56. "PREFACE" follows.
clean_file(
    os.path.join(base_path, "discourses_on_livy.txt"),
    "BOOK I.",
    "*** END OF THE PROJECT"
)

# History of Florence
# "BOOK I" is line 216.
clean_file(
    os.path.join(base_path, "history_of_florence.txt"),
    "BOOK I",
    "*** END OF THE PROJECT"
)
