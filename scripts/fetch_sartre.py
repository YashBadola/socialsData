import urllib.request
import re
import os
import html as html_lib

url = "https://www.marxists.org/reference/archive/sartre/works/exist/sartre.htm"
output_path = "socials_data/personalities/jean_paul_sartre/raw/existentialism_is_a_humanism.txt"

def fetch_and_clean():
    print(f"Fetching {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')

    print("Cleaning text...")

    # Pre-process some tags for formatting
    html = html.replace("</p>", "\n\n")
    html = html.replace("<br>", "\n")
    html = html.replace("<br/>", "\n")
    html = html.replace("</div>", "\n")

    # Strip HTML tags
    clean_text = re.sub(r'<[^>]+>', '', html)

    # Decode HTML entities (numeric and named)
    clean_text = html_lib.unescape(clean_text)

    # Remove excessive blank lines
    lines = [line.strip() for line in clean_text.splitlines()]
    clean_text = "\n".join([line for line in lines if line])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print(f"Saved to {output_path}")
    print(f"Length: {len(clean_text)} chars")

if __name__ == "__main__":
    fetch_and_clean()
