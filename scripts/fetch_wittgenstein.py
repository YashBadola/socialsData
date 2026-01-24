import requests
import re

base_url = "https://en.wikisource.org/wiki/Tractatus_Logico-Philosophicus/"
chapters = ["1", "2", "3", "4", "5", "6", "7"]
output_path = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt"

full_text = ""

for i in chapters:
    url = base_url + i
    print(f"Fetching {url}...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.text

        # Remove scripts and styles
        content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)

        # Replace block tags with newlines
        content = re.sub(r'<(div|p|h\d|br|li|tr)[^>]*>', '\n', content, flags=re.IGNORECASE)

        # Remove tags
        text = re.sub(r'<[^>]+>', ' ', content)

        # Unescape HTML entities (basic ones)
        text = text.replace("&nbsp;", " ").replace("&#160;", " ")

        # Split into lines
        lines = text.split('\n')

        relevant_lines = []
        capture = False

        # Regex for the start of the chapter text
        # Chapter 1 starts with "1 The world..."
        # Other chapters start with "{i} ..."

        start_pattern = None
        if i == "1":
            start_pattern = re.compile(r'^\s*1\s+The world')
        elif i == "7":
            start_pattern = re.compile(r'7\s+Whereof one cannot speak')
        else:
            start_pattern = re.compile(rf'^\s*{i}\s+')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if not capture:
                if (i == "7" and start_pattern.search(line)) or (i != "7" and start_pattern.match(line)):
                    capture = True
                    # For Chapter 7, we might want to extract just the relevant part if it's mixed
                    if i == "7":
                        # Attempt to clean up the line if it has garbage before "7"
                        match = start_pattern.search(line)
                        if match:
                            start_idx = match.start()
                            line = line[start_idx:]
                    relevant_lines.append(line)
            else:
                # Stop if we hit "References" or "Retrieved from" or navigation links
                if "Retrieved from" in line or "References" == line or line.startswith("Visible links:"):
                    capture = False
                    break

                # Filter out obvious UI elements if any slipped through
                if line in ["Navigation", "Search", "Appearance"]:
                    continue

                relevant_lines.append(line)

        print(f"Captured {len(relevant_lines)} lines for Chapter {i}")
        if len(relevant_lines) == 0:
            print(f"WARNING: No text captured for Chapter {i}")
            if i == "7":
                print("Dumping lines for debugging Chapter 7:")
                for l in lines:
                    if "7" in l:
                        print(f"[{l.strip()}]")

        chapter_text = "\n".join(relevant_lines)
        full_text += f"\n\n--- Chapter {i} ---\n\n" + chapter_text

    except Exception as e:
        print(f"Error fetching {url}: {e}")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Saved to {output_path}")
