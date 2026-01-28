import os

input_file = "temp_tractatus.txt"
output_file = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt"

start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK, TRACTATUS LOGICO-PHILOSOPHICUS ***"
end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK, TRACTATUS LOGICO-PHILOSOPHICUS ***"

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

start_index = -1
end_index = -1

for i, line in enumerate(lines):
    if start_marker in line:
        start_index = i
    if end_marker in line:
        end_index = i

if start_index != -1 and end_index != -1:
    # Extract text between markers
    cleaned_lines = lines[start_index + 1 : end_index]
    # Remove leading/trailing whitespace lines
    content = "".join(cleaned_lines).strip()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Cleaned text written to {output_file}")
else:
    print("Markers not found!")
