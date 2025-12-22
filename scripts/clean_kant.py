import os

def clean_kant():
    filepath = "socials_data/personalities/immanuel_kant/raw/critique_of_pure_reason.txt"

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
            start_index = i
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end_index = i

    if start_index == -1 or end_index == -1:
        print("Could not find start or end markers.")
        return

    # Keep content between markers, excluding the markers themselves
    # And maybe skipping some initial blank lines/title/author lines if they appear immediately after start

    # Let's inspect what is after start_index
    # Based on previous `head` output:
    # 25:*** START ... ***
    # 26:
    # 27:[Illustration]
    # 28:
    # 29:
    # 30:The Critique of Pure Reason
    # 31:
    # 32:By Immanuel Kant

    # We can just cut from start_index + 1 to end_index
    cleaned_lines = lines[start_index + 1 : end_index]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"Cleaned {filepath}. Kept lines {start_index+2} to {end_index}.")

if __name__ == "__main__":
    clean_kant()
