import requests
import os

def fetch_tractatus():
    url = "https://raw.githubusercontent.com/wittgenstein-project/wittgenstein-published-works/main/markdown/english/Tractatus%20Logico-Philosophicus%20(English)/Tractatus%20Logico-Philosophicus%20(English).md"
    output_path = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt"

    print(f"Fetching from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Successfully wrote to {output_path}")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_tractatus()
