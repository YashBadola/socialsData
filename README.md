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
    *   **`qa.jsonl`**: (Optional) Synthetic Q&A pairs for instruction tuning.

### 2. Metadata Schema (`metadata.json`)

```json
{
  "name": "Full Name",
  "id": "snake_case_id",
  "description": "Short bio or description.",
  "system_prompt": "Optional. A definition of the persona used for generating synthetic Q&A pairs.",
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
    *   It converts different formats (currently Text) into a unified text stream (`processed/data.jsonl`).
    *   If `OPENAI_API_KEY` is set and a `system_prompt` is defined, it generates **synthetic Instruction/Response pairs** (`processed/qa.jsonl`) using an LLM.
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

**Process data (with Q&A generation):**
```bash
export OPENAI_API_KEY="sk-..."
socials-data process elon_musk
```
*This reads from `raw/`, compiles `processed/data.jsonl`, and generates `processed/qa.jsonl`.*

**Process data (skip Q&A generation):**
```bash
socials-data process elon_musk --skip-qa
```
*Useful for saving API costs or when only raw text is needed.*

**Generate Q&A only:**
```bash
socials-data generate-qa elon_musk
```
*Generates Q&A pairs from existing `processed/data.jsonl`.*

### Database Generation

You can aggregate all processed personalities into a single SQLite database:

```bash
python scripts/build_database.py
```

This creates `philosophers.db` with tables `personalities` and `content`.

### Python API

Loading a dataset for training (compatible with Hugging Face):

```python
from socials_data import load_dataset

# Returns a Hugging Face Dataset object
dataset = load_dataset("nick_land")

print(dataset[0]['text'])

# Load Q&A data (if available)
# (Note: load_dataset currently defaults to 'text', updates pending for 'qa' split support)
```

## Instruction Tuning

`socialsData` supports **Instruction Tuning** by automatically converting raw texts into Q&A pairs. This accelerates the fine-tuning of Small Language Models (SLMs) by providing rich, persona-aligned interactions (Advice, Philosophy, Chat) rather than just raw text prediction.

**Example Generated Q&A:**
```json
{
  "instruction": "I am feeling anxious about the future. What should I do?",
  "response": "Do not disturb yourself by picturing your life as a whole; do not assemble in your mind the many and varied troubles which have come to you in the past... but ask yourself with regard to every present difficulty: 'What is there in this that is unbearable and beyond endurance?'"
}
```
