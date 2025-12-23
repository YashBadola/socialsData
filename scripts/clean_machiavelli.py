import os

PERSONALITY_ID = "niccolo_machiavelli"
RAW_DIR = f"socials_data/personalities/{PERSONALITY_ID}/raw"

BOOKS = {
    "the_prince.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***",
        "secondary_start": "CHAPTER I"
    },
    "discourses_on_livy.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK DISCOURSES ON THE FIRST DECADE OF TITUS LIVIUS ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK DISCOURSES ON THE FIRST DECADE OF TITUS LIVIUS ***",
        "secondary_start": "CHAPTER I."
    },
    "art_of_war.txt": {
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK MACHIAVELLI, VOLUME I ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK MACHIAVELLI, VOLUME I ***",
        "secondary_start": "THE ART OF WAR"
    }
}

def clean_file(filename, config):
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pass 1: Cut off main headers
    start_idx = content.find(config["start"])
    end_idx = content.find(config["end"])

    if start_idx == -1:
        print(f"Warning: Start marker not found for {filename}")
        # Try to find a reasonable fallback if standard marker is missing?
        # For now, just warn.
    else:
        start_idx += len(config["start"])

    if end_idx == -1:
        print(f"Warning: End marker not found for {filename}. Using end of file.")
        end_idx = len(content)

    content = content[start_idx:end_idx]

    # Pass 2: Secondary start to remove intros
    if "secondary_start" in config:
        sec_idx = content.find(config["secondary_start"])
        if sec_idx != -1:
            content = content[sec_idx:]
        else:
             print(f"Warning: Secondary start marker '{config['secondary_start']}' not found for {filename}")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"Cleaned {filename}")

def main():
    if not os.path.exists(RAW_DIR):
        print(f"Directory {RAW_DIR} does not exist.")
        return

    for filename, config in BOOKS.items():
        clean_file(filename, config)

if __name__ == "__main__":
    main()
