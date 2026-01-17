import re
import json
import os

def generate_qa():
    input_path = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt"
    output_path = "socials_data/personalities/ludwig_wittgenstein/processed/qa.jsonl"

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    propositions = {}
    current_number = None
    current_text = []

    # Regex to match proposition numbers at the start of a line
    # Examples: 1, 1.1, 2.01, 6.54
    # Note: Sometimes there might be whitespace
    prop_pattern = re.compile(r"^\s*(\d+(\.\d+)*)\s+(.*)")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = prop_pattern.match(line)
        if match:
            # Save previous proposition
            if current_number:
                propositions[current_number] = " ".join(current_text)

            # Start new proposition
            current_number = match.group(1)
            current_text = [match.group(3)]
        else:
            # Append to current proposition
            if current_number:
                current_text.append(line)

    # Save last proposition
    if current_number:
        propositions[current_number] = " ".join(current_text)

    print(f"Found {len(propositions)} propositions.")

    with open(output_path, 'w', encoding='utf-8') as f:
        for number, text in propositions.items():
            # Create QA pairs

            # Type 1: Lookup by number
            qa1 = {
                "instruction": f"What is proposition {number} in the Tractatus Logico-Philosophicus?",
                "response": text
            }
            f.write(json.dumps(qa1) + "\n")

            # Type 2: Recite by number
            qa2 = {
                "instruction": f"Recite proposition {number}.",
                "response": text
            }
            f.write(json.dumps(qa2) + "\n")

            # Type 3: Contextual (simple)
            qa3 = {
                "instruction": f"In the Tractatus, what corresponds to the number {number}?",
                "response": f"Proposition {number} states: {text}"
            }
            f.write(json.dumps(qa3) + "\n")

    print(f"Generated QA pairs to {output_path}")

if __name__ == "__main__":
    generate_qa()
