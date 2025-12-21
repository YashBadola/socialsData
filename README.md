# socialsData

A unified methodology and library to store, process, and access datasets of public figures, famous people, and well-known personalities. The primary goal is to facilitate the training and fine-tuning of language models to adopt the persona of selected individuals.

## Methodology

To ensure consistency and ease of use across different personalities, `socialsData` enforces a strict structure and data lifecycle.

### 1. Structure

Every personality is a subdirectory within `socials_data/personalities/`. The directory name should be the `snake_case` version of the person's name (e.g., `nick_land`, `slavoj_zizek`).

Each personality directory must contain:

*   **`metadata.json`**: A configuration file defining the personality.
*   **`raw/`**: A folder containing raw data sources. This can include:
    *   Text files (`.txt`, `.md`)
    *   Audio files (`.mp3`, `.wav`) - *To be transcribed*
    *   Video files (`.mp4`) - *To be transcribed*
    *   PDFs/EPUBs - *To be converted to text*
*   **`processed/`**: A folder containing the cleaned, machine-readable dataset.
    *   **`data.jsonl`**: The canonical dataset file. Each line is a JSON object containing at least a `"text"` field.

### 2. Metadata Schema (`metadata.json`)

```json
{
  "name": "Full Name",
  "id": "snake_case_id",
  "description": "Short bio or description.",
  "sources": [
    {
      "type": "book",
      "title": "Title of the work",
      "url": "optional_link"
    }
  ],
  "license": "License of the collected data"
}
```

### 3. Data Lifecycle

1.  **Ingestion**: Raw files are placed manually or via scripts into `raw/`.
2.  **Processing**: The `socials-data process <name>` command runs.
    *   It iterates through `raw/`.
    *   It converts different formats (currently Text) into a unified text stream.
    *   It performs cleaning (whitespace normalization, removal of artifacts).
    *   It appends the result to `processed/data.jsonl`.
3.  **Access**: Users load the data using the Python API.

## Usage

### Installation

```bash
pip install -e .
```

### CLI

**List all personalities:**
```bash
socials-data list
```

**Add a new personality:**
```bash
socials-data add "Elon Musk"
```
*This creates `socials_data/personalities/elon_musk/` with the required structure.*

**Process data:**
```bash
socials-data process elon_musk
```
*This reads from `raw/` and compiles `processed/data.jsonl`.*

### Python API

Loading a dataset for training (compatible with Hugging Face):

```python
from socials_data import load_dataset

# Returns a Hugging Face Dataset object
dataset = load_dataset("nick_land")

print(dataset[0]['text'])
```
