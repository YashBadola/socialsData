import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
            break

    # Search from end
    for i in range(len(lines) - 1, -1, -1):
        if end_marker in lines[i]:
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        # Keep content between markers
        content = lines[start_index + 1 : end_index]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(content)
        print(f"Cleaned {filepath}")
    else:
        print(f"Markers not found in {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/immanuel_kant/raw"

    files = [
        {
            "filename": "critique_of_pure_reason.txt",
            "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"
        },
        {
            "filename": "critique_of_practical_reason.txt",
            "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PRACTICAL REASON ***",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PRACTICAL REASON ***"
        }
    ]

    for item in files:
        filepath = os.path.join(base_dir, item["filename"])
        clean_file(filepath, item["start"], item["end"])
