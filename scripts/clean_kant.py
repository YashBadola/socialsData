import os

BASE_DIR = "socials_data/personalities/immanuel_kant/raw"

def clean_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_index = 0
    end_index = len(lines)

    for i, line in enumerate(lines):
        if "*** START OF" in line:
            start_index = i + 1
        if "*** END OF" in line:
            end_index = i
            break

    # Refine start index - remove potential empty lines after the marker
    while start_index < end_index and not lines[start_index].strip():
        start_index += 1

    cleaned_content = "".join(lines[start_index:end_index]).strip()

    if len(cleaned_content) < 100:
        print(f"Warning: Cleaned content for {filename} is suspiciously short ({len(cleaned_content)} chars).")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
    print(f"Cleaned {filename}")

if __name__ == "__main__":
    files = [
        "critique_of_pure_reason.txt",
        "critique_of_practical_reason.txt",
        "fundamental_principles_metaphysic_morals.txt",
        "metaphysical_elements_ethics.txt",
        "critique_of_judgement.txt"
    ]

    for f in files:
        clean_file(f)
