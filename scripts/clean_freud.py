import os

raw_dir = "socials_data/personalities/sigmund_freud/raw/"

files_config = {
    "dream_psychology.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK DREAM PSYCHOLOGY: PSYCHOANALYSIS FOR BEGINNERS ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK DREAM PSYCHOLOGY: PSYCHOANALYSIS FOR BEGINNERS ***"
    },
    "psychopathology_of_everyday_life.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK PSYCHOPATHOLOGY OF EVERYDAY LIFE ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK PSYCHOPATHOLOGY OF EVERYDAY LIFE ***"
    },
    "the_interpretation_of_dreams.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE INTERPRETATION OF DREAMS ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE INTERPRETATION OF DREAMS ***"
    },
    "three_contributions_theory_of_sex.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THREE CONTRIBUTIONS TO THE THEORY OF SEX ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THREE CONTRIBUTIONS TO THE THEORY OF SEX ***"
    }
}

for filename, markers in files_config.items():
    filepath = os.path.join(raw_dir, filename)
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    start_marker = markers["start"]
    end_marker = markers["end"]

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1:
        print(f"Warning: Start marker not found for {filename}")
        continue
    if end_idx == -1:
        print(f"Warning: End marker not found for {filename}")
        # If end marker missing, maybe just take until end of file (less risky than nothing)
        end_idx = len(content)

    # Adjust start index to skip the marker itself
    start_idx += len(start_marker)

    cleaned_content = content[start_idx:end_idx].strip()

    # Overwrite the file with cleaned content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {filename}")
