import os
import requests

url = "https://archive.org/download/tractatuslogicop05740gut/tloph10.txt"
output_file = "temp_tractatus.txt"

print(f"Downloading {url} to {output_file}...")
response = requests.get(url, allow_redirects=True)
response.raise_for_status()

with open(output_file, "wb") as f:
    f.write(response.content)

print("Download complete.")
