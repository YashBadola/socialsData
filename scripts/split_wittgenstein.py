import re
import os

def split_wittgenstein(filepath, output_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_file = "preface.txt"
    files = {
        "preface.txt": [],
        "prop_1.txt": [],
        "prop_2.txt": [],
        "prop_3.txt": [],
        "prop_4.txt": [],
        "prop_5.txt": [],
        "prop_6.txt": [],
        "prop_7.txt": [],
    }

    # Regex for main propositions 1 to 7.
    # Matches "1 " or "1." at start of line.
    # Actually, main props are "1 ", "2 " etc.
    # Sub props are "1.1" etc.
    # So checking if line starts with digit 1-7 is enough to switch context?
    # But we need to distinguish "1" from "1.1".
    # Actually we just want to group by the main number.
    # So if it starts with "1", it goes to prop_1.txt.

    for line in lines:
        stripped = line.strip()
        if not stripped:
            files[current_file].append(line)
            continue

        # Check if line starts with a number 1-7
        # Note: 10, 11 etc don't exist in Tractatus.
        if stripped[0].isdigit() and stripped[0] in "1234567":
             # Check if it's a proposition start
             # It should be followed by space or dot
             if len(stripped) > 1 and (stripped[1] == ' ' or stripped[1] == '.'):
                 main_num = stripped[0]
                 current_file = f"prop_{main_num}.txt"

        files[current_file].append(line)

    # Write files
    for filename, content in files.items():
        if not content:
            continue
        out_path = os.path.join(output_dir, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.writelines(content)
        print(f"Written {out_path}")

if __name__ == "__main__":
    split_wittgenstein(
        "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt",
        "socials_data/personalities/ludwig_wittgenstein/raw/"
    )
