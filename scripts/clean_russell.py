
import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Start marker not found in {filepath}")
        return

    # Adjust start index to skip the marker itself
    start_idx += len(start_marker)

    end_idx = content.find(end_marker)
    if end_idx == -1:
        print(f"End marker not found in {filepath}")
        return

    cleaned_content = content[start_idx:end_idx].strip()

    # Overwrite the file with cleaned content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/bertrand_russell/raw"

files = [
    {
        "name": "problems_of_philosophy.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE PROBLEMS OF PHILOSOPHY ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE PROBLEMS OF PHILOSOPHY ***"
    },
    {
        "name": "analysis_of_mind.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE ANALYSIS OF MIND ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE ANALYSIS OF MIND ***"
    },
    {
        "name": "mysticism_and_logic.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK MYSTICISM AND LOGIC AND OTHER ESSAYS ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK MYSTICISM AND LOGIC AND OTHER ESSAYS ***"
    }
]

for file_info in files:
    clean_file(os.path.join(base_dir, file_info["name"]), file_info["start"], file_info["end"])
