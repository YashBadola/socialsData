import os
import re

def main():
    try:
        with open("sartre_full_text.txt", "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print("sartre_full_text.txt not found.")
        return

    # Clean header/footer based on raw structure first
    # Find start
    start_marker = "My purpose here is to offer a defence"
    match_start = re.search(re.escape(start_marker).replace(r'\ ', r'\s+'), raw_text)
    if match_start:
         raw_text = raw_text[match_start.start():]

    # Find end
    end_marker = "Further Reading:"
    match_end = re.search(re.escape(end_marker).replace(r'\ ', r'\s+'), raw_text)
    if match_end:
        raw_text = raw_text[:match_end.start()]


    output_dir = "socials_data/personalities/jean_paul_sartre/raw/"
    os.makedirs(output_dir, exist_ok=True)

    markers = [
        "My purpose here is to offer a defence",
        "The question is only complicated because there are two kinds of",
        "This may enable us to understand what is meant by such terms",
        "As for “despair,” the meaning of this expression is extremely simple.",
        "We have now, I think, dealt with a certain number of the reproaches",
        "I have been reproached for suggesting that existentialism is a form of humanism",
        "You can see from these few reflections that nothing could be more unjust"
    ]

    file_names = [
        "01_intro_reproaches.txt",
        "02_existence_precedes_essence.txt",
        "03_anguish_abandonment.txt",
        "04_despair_and_action.txt",
        "05_subjectivity_and_others.txt",
        "06_existential_humanism.txt",
        "07_conclusion.txt"
    ]

    indices = []
    for m in markers:
        # Search in raw_text, ignoring newlines for the match
        # We replace space in marker with \s+ to match across line breaks
        pattern = re.escape(m).replace(r'\ ', r'\s+')
        match = re.search(pattern, raw_text)
        if match:
            indices.append(match.start())
        else:
            print(f"Could not find marker: {m}")
            indices.append(-1)

    # Add end of text
    indices.append(len(raw_text))

    for i in range(len(file_names)):
        start = indices[i]
        # Skip if marker wasn't found
        if start == -1: continue

        # Find next valid start index
        next_valid_idx = len(raw_text)
        for j in range(i+1, len(indices)):
            if indices[j] != -1:
                next_valid_idx = indices[j]
                break

        end = next_valid_idx

        chunk = raw_text[start:end]

        # Clean up paragraphs
        lines = chunk.split('\n')
        paragraphs = []
        current_para = []
        for line in lines:
            line = line.strip()
            if not line:
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
            else:
                current_para.append(line)
        if current_para:
            paragraphs.append(" ".join(current_para))

        final_content = "\n\n".join(paragraphs)

        with open(os.path.join(output_dir, file_names[i]), "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Created {file_names[i]}")

if __name__ == "__main__":
    main()
