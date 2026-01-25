import os
import re

def main():
    with open("temp_sartre.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Clean header and footer
    start_marker = "My purpose here is to offer a defence"
    end_marker = "Christians can describe us as without hope."

    # Simple string find for start/end usually works if they are short and don't span lines.
    # Start marker seems to be on one line.
    # End marker seems to be on one line.

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1:
        print("Error: Could not find start marker.")
        # Fallback using regex
        match = re.search(r"My purpose here is to offer a defence", text)
        if match:
            start_idx = match.start()
        else:
            return

    if end_idx == -1:
        print("Error: Could not find end marker.")
        match = re.search(r"Christians can describe us as without hope\.", text)
        if match:
            end_idx = match.start()
        else:
            return

    content = text[start_idx:end_idx + len(end_marker)]

    # Define sections
    sections = [
        ("01_introduction.txt", "My purpose here is to offer a defence"),
        ("02_types_of_existentialists.txt", "The question is only complicated because there are two kinds of existentialists."),
        ("03_existence_precedes_essence.txt", "Atheistic existentialism, of which I am a representative"),
        ("04_anguish_abandonment_despair.txt", "This may enable us to understand what is meant by such terms"),
        ("05_reality_in_action.txt", "Quietism is the attitude of people who say"),
        ("06_subjectivity_and_others.txt", "We have now, I think, dealt with a certain number of the reproaches"),
        ("07_inventing_values.txt", "The third objection, stated by saying"),
        ("08_conclusion.txt", "You can see from these few reflections")
    ]

    output_dir = "socials_data/personalities/jean_paul_sartre/raw/"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(sections)):
        filename, marker = sections[i]

        # Regex find
        # Escape the marker, then replace escaped spaces with \s+ to match newlines
        pattern_str = re.escape(marker).replace(r"\ ", r"\s+")
        pattern = re.compile(pattern_str)

        match = pattern.search(content)

        if not match:
            print(f"Warning: Marker for {filename} not found.")
            # Try finding a shorter substring if full sentence fails?
            # E.g. first 20 chars
            short_marker = marker[:20]
            pattern_str_short = re.escape(short_marker).replace(r"\ ", r"\s+")
            match = re.search(pattern_str_short, content)
            if not match:
                 print(f"  Failed even with short marker: '{short_marker}'")
                 continue

        s_idx = match.start()

        # Find start of next section (or end of content)
        e_idx = len(content)
        if i < len(sections) - 1:
            next_marker = sections[i+1][1]
            next_pattern_str = re.escape(next_marker).replace(r"\ ", r"\s+")
            next_match = re.search(next_pattern_str, content)

            if next_match:
                e_idx = next_match.start()
            else:
                 # Try short marker for next
                 short_next = next_marker[:20]
                 short_next_pattern = re.escape(short_next).replace(r"\ ", r"\s+")
                 next_match = re.search(short_next_pattern, content)
                 if next_match:
                     e_idx = next_match.start()
                 else:
                    print(f"Warning: Next marker for {filename} not found. Using end of text.")

        section_content = content[s_idx:e_idx].strip()

        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as out:
            out.write(section_content)

        print(f"Written {filename} ({len(section_content)} chars)")

if __name__ == "__main__":
    main()
