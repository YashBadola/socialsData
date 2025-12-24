import os

def clean_file(filepath, start_marker, end_marker, actual_start_marker=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
        if end_marker in line:
            end_idx = i
            break

    content = lines[start_idx:end_idx]

    if actual_start_marker:
        real_start_idx = 0
        for i, line in enumerate(content):
            if actual_start_marker in line:
                real_start_idx = i
                break
        content = content[real_start_idx:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Cleaned {filepath}")

base_path = "socials_data/personalities/jean_jacques_rousseau/raw"

# The Social Contract
clean_file(
    os.path.join(base_path, "the_social_contract.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***",
    "THE SOCIAL CONTRACT & DISCOURSES"
)

# Emile
clean_file(
    os.path.join(base_path, "emile.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK EMILE ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK EMILE ***",
    "EMILE"
)

# The Confessions
clean_file(
    os.path.join(base_path, "the_confessions.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***",
    "THE CONFESSIONS OF JEAN JACQUES ROUSSEAU"
)

# Discourse on Inequality
clean_file(
    os.path.join(base_path, "discourse_on_inequality.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK A DISCOURSE UPON THE ORIGIN AND THE FOUNDATION OF THE INEQUALITY AMONG MANKIND ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK A DISCOURSE UPON THE ORIGIN AND THE FOUNDATION OF THE INEQUALITY AMONG MANKIND ***",
    "A Discourse Upon The Origin And The Foundation Of The Inequality Among"
)
