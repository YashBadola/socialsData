import os

def clean_file(filepath, start_markers, end_markers):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    start_idx = -1
    for marker in start_markers:
        idx = content.find(marker)
        if idx != -1:
            start_idx = idx + len(marker)
            break

    if start_idx == -1:
        print(f"Warning: Start marker not found for {filepath}")
        # Fallback to general Gutenberg start
        start_idx = content.find("*** START OF THE PROJECT GUTENBERG EBOOK")
        if start_idx != -1:
            start_idx = content.find("***", start_idx + 3) + 3

    end_idx = -1
    for marker in end_markers:
        idx = content.find(marker)
        if idx != -1:
            end_idx = idx
            break

    if end_idx == -1:
         print(f"Warning: End marker not found for {filepath}")
         # Fallback to general Gutenberg end
         end_idx = content.find("*** END OF THE PROJECT GUTENBERG EBOOK")

    if start_idx != -1 and end_idx != -1:
        content = content[start_idx:end_idx].strip()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {filepath}")
    else:
        print(f"Failed to clean {filepath} properly. Start: {start_idx}, End: {end_idx}")

base_dir = "socials_data/personalities/niccolo_machiavelli/raw"

# The Prince
clean_file(
    os.path.join(base_dir, "the_prince.txt"),
    ["*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"],
    ["*** END OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"]
)

# Discourses
clean_file(
    os.path.join(base_dir, "discourses.txt"),
    ["*** START OF THE PROJECT GUTENBERG EBOOK DISCOURSES ON THE FIRST DECADE OF TITUS LIVIUS ***", "*** START OF THE PROJECT GUTENBERG EBOOK DISCOURSES ***"],
    ["*** END OF THE PROJECT GUTENBERG EBOOK DISCOURSES ON THE FIRST DECADE OF TITUS LIVIUS ***"]
)

# Art of War (Volume I)
# This one is tricky as it is "Machiavelli, Volume I". The marker might be generic.
# Let's use generic markers for now or look for "THE ART OF WAR" in the content?
# It seems pg15772 title is "Machiavelli, Volume I".
clean_file(
    os.path.join(base_dir, "art_of_war.txt"),
    ["*** START OF THE PROJECT GUTENBERG EBOOK MACHIAVELLI, VOLUME I ***"],
    ["*** END OF THE PROJECT GUTENBERG EBOOK MACHIAVELLI, VOLUME I ***"]
)
