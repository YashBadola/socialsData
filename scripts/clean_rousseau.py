import os

def clean_file(filepath, start_marker, end_marker, actual_start_marker=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
            break

    # Refine start if there's an actual start marker (like title page end)
    if actual_start_marker:
        for i in range(start_idx, len(lines)):
            if actual_start_marker in line:
                start_idx = i
                break

    for i, line in enumerate(lines):
        if end_marker in line:
            end_idx = i
            break

    cleaned_lines = lines[start_idx:end_idx]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    print(f"Cleaned {filepath}")

def main():
    base_path = "socials_data/personalities/jean_jacques_rousseau/raw"

    # Social Contract
    # Start: *** START OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***
    # End: *** END OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***
    clean_file(
        os.path.join(base_path, "the_social_contract.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE SOCIAL CONTRACT & DISCOURSES ***"
    )

    # Emile
    # Start: *** START OF THE PROJECT GUTENBERG EBOOK EMILE ***
    # End: *** END OF THE PROJECT GUTENBERG EBOOK EMILE ***
    clean_file(
        os.path.join(base_path, "emile.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK EMILE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK EMILE ***"
    )

    # Confessions
    # Start: *** START OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***
    # End: *** END OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***
    clean_file(
        os.path.join(base_path, "the_confessions.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE CONFESSIONS OF JEAN JACQUES ROUSSEAU — COMPLETE ***"
    )

if __name__ == "__main__":
    main()
