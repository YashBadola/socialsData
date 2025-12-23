
def clean_file(filepath, start_marker, end_marker, actual_start_marker=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # First pass: find Gutenberg markers
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
        if end_marker in line:
            end_idx = i
            break

    # Refine start if actual_start_marker is provided
    # We will search for the marker *within* the valid range
    if actual_start_marker:
        found = False
        for i in range(start_idx, end_idx):
            if actual_start_marker in lines[i]:
                start_idx = i
                found = True
                break
        if not found:
            print(f"Warning: Actual start marker '{actual_start_marker}' not found in {filepath}")

    content = lines[start_idx:end_idx]
    cleaned_content = "".join(content).strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

# Republic
# Starting exactly at the famous opening line to avoid Jowett's intros
clean_file(
    'socials_data/personalities/plato/raw/republic.txt',
    '*** START OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC ***',
    '*** END OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC ***',
    actual_start_marker='I went down yesterday to the Piraeus'
)

# Symposium
# Starting at the Persons of the Dialogue
clean_file(
    'socials_data/personalities/plato/raw/symposium.txt',
    '*** START OF THE PROJECT GUTENBERG EBOOK SYMPOSIUM ***',
    '*** END OF THE PROJECT GUTENBERG EBOOK SYMPOSIUM ***',
    actual_start_marker='PERSONS OF THE DIALOGUE: Apollodorus'
)
