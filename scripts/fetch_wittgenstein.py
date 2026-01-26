import requests
import os

def main():
    url = "https://raw.githubusercontent.com/wittgenstein-project/wittgenstein-published-works/main/markdown/english/Tractatus%20Logico-Philosophicus%20(English)/Tractatus%20Logico-Philosophicus%20(English).md"
    target_path = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.md"

    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Saved to {target_path}")

if __name__ == "__main__":
    main()
