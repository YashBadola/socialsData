import re
import json
import os

def generate_qa(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    propositions = []
    current_number = None
    current_text = []

    # Regex for proposition number: starts with digit, contains dots/digits, ends with space
    # e.g. "1 ", "1.1 ", "6.36111 "
    prop_pattern = re.compile(r"^(\d+(\.\d+)*)\s+(.*)")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = prop_pattern.match(line)
        if match:
            # Save previous proposition
            if current_number:
                propositions.append({
                    "number": current_number,
                    "text": " ".join(current_text)
                })

            # Start new proposition
            current_number = match.group(1)
            current_text = [match.group(3)]
        else:
            # Continue previous proposition
            if current_number:
                current_text.append(line)

    # Save last proposition
    if current_number:
        propositions.append({
            "number": current_number,
            "text": " ".join(current_text)
        })

    print(f"Found {len(propositions)} propositions.")

    # Generate QA pairs
    qa_pairs = []
    for prop in propositions:
        # QA 1: Recite
        qa_pairs.append({
            "instruction": f"Recite proposition {prop['number']} of the Tractatus.",
            "response": prop['text']
        })
        # QA 2: What does it say
        qa_pairs.append({
            "instruction": f"What does proposition {prop['number']} state?",
            "response": prop['text']
        })

    # Write to jsonl
    with open(output_path, 'w', encoding='utf-8') as f:
        for qa in qa_pairs:
            f.write(json.dumps(qa) + "\n")

    print(f"Generated {len(qa_pairs)} QA pairs to {output_path}")

if __name__ == "__main__":
    input_file = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus_cleaned.txt"
    output_file = "socials_data/personalities/ludwig_wittgenstein/processed/qa.jsonl"

    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    generate_qa(input_file, output_file)
