import os

def clean_file(filepath, start_marker, end_marker, target_start_occurrence=1):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    current_occurrence = 0
    for i, line in enumerate(lines):
        if start_marker in line:
            current_occurrence += 1
            if current_occurrence == target_start_occurrence:
                start_index = i
                break

    # Find end
    for i, line in enumerate(lines):
        if end_marker in line:
            end_index = i
            break

    if start_index == -1 or end_index == -1:
        print(f"Markers not found in {filepath}. Start index: {start_index}, End index: {end_index}")
        print("The file might have already been cleaned.")
        return

    # Extract content
    cleaned_lines = lines[start_index:end_index]

    # Remove leading/trailing whitespace lines
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/niccolo_machiavelli/raw"

    # The Prince: "DEDICATION" at line 467 is the 2nd occurrence.
    clean_file(
        os.path.join(base_dir, "the_prince.txt"),
        "DEDICATION",
        "*** END OF THE PROJECT GUTENBERG EBOOK 1232 ***",
        target_start_occurrence=2
    )

    # Discourses:
    # 34: PREFACE (TOC Book I)
    # 235: PREFACE (TOC Book II)
    # 549: PREFACE (Actual Book I text start)
    # So we want the 3rd occurrence.
    clean_file(
        os.path.join(base_dir, "discourses_on_livy.txt"),
        "PREFACE",
        "*** END OF THE PROJECT GUTENBERG EBOOK 10827 ***",
        target_start_occurrence=3
    )
