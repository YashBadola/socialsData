
import os

def clean_plato():
    base_dir = "socials_data/personalities/plato/raw"
    filepath = os.path.join(base_dir, "republic.txt")

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # The file contains a long Introduction and Analysis by Jowett.
    # The actual text starts with "THE REPUBLIC." followed by "BOOK I" around line 8559.

    start_marker = "THE REPUBLIC.\n\nBOOK I"
    end_marker = "THE END."

    start_index = text.find(start_marker)
    if start_index == -1:
         # Fallback search if exact newline matching fails
        start_marker_fallback = "THE REPUBLIC."
        start_index = text.rfind(start_marker_fallback) # Use rfind to get the last occurrence (the actual title page before Book I)

    end_index = text.rfind(end_marker)

    if start_index != -1:
        # Keep the title
        pass
    else:
        print("Could not find start marker.")
        return

    if end_index != -1:
        text = text[start_index:end_index + len(end_marker)]
    else:
        # Fallback if THE END is not found or slightly different
        print("Warning: Could not find end marker, taking till end of file.")
        text = text[start_index:]

    # Clean up whitespace
    text = text.strip()

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print("Successfully cleaned plato/raw/republic.txt")

if __name__ == "__main__":
    clean_plato()
