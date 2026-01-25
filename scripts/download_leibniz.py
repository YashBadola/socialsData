import requests
import re
import os

def strip_tags(html):
    # Remove scripts and styles
    html = re.sub(r'<script.*?</script>', ' ', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?</style>', ' ', html, flags=re.DOTALL)
    # Remove tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Decode HTML entities (basic ones)
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return text

url = "https://www.marxists.org/reference/subject/philosophy/works/ge/leibniz.htm"
print(f"Downloading from {url}...")
response = requests.get(url)
response.raise_for_status()

# Resplit into paragraphs roughly?
# The stripped text will be one giant line if I replace all whitespace with space.
# Better to preserve newlines from block elements if possible, but regex strip is crude.
# Let's try to be smarter. Replace block tags with newlines first.

html = response.text
html = re.sub(r'</p>', '\n\n', html)
html = re.sub(r'<br\s*/?>', '\n', html)
html = re.sub(r'</div>', '\n', html)

text = strip_tags(html)

# Find start and end
start_marker = "1. The monad"
end_marker = "Further Reading"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1:
    if end_idx != -1:
        content = text[start_idx:end_idx]
    else:
        content = text[start_idx:]
else:
    print("Warning: Start marker not found. Saving whole text.")
    content = text

# Clean up multiple newlines
content = re.sub(r'\n\s*\n', '\n\n', content)
content = content.strip()

output_path = "socials_data/personalities/gottfried_wilhelm_leibniz/raw/monadology.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved {len(content)} characters to {output_path}")
