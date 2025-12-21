import os
import json
import logging
from typing import Optional, List, Dict
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class LLMProcessor:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM Processor.
        If api_key is provided, it uses it. Otherwise checks os.environ.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            self.client = None
            logging.warning("No OPENAI_API_KEY found. LLM features will be disabled.")
        else:
            if OpenAI:
                self.client = OpenAI(api_key=self.api_key)
            else:
                self.client = None
                logging.warning("openai package not installed. LLM features will be disabled.")

    def generate_qa_pairs(self, text_chunk: str, system_prompt: str) -> List[Dict[str, str]]:
        """
        Generates Instruction/Response pairs from a given text chunk using the system prompt.
        """
        if not self.client:
            return []

        # Construct the user prompt to guide the LLM to output valid JSON
        # We want a list of objects with "instruction" and "response" keys.
        user_message = (
            "Analyze the following text and extract relevant questions (instructions) and answers (responses) "
            "that represent the personality defined in the system prompt. "
            "If the text is a narrative, infer potential questions someone might ask to get the response mentioned in the text.\n\n"
            f"Text:\n{text_chunk}\n\n"
            "Output Format:\n"
            "Provide a valid JSON array of objects. Each object must have exactly two keys: \"instruction\" and \"response\".\n"
            "Example: [{\"instruction\": \"Question?\", \"response\": \"Answer.\"}]\n"
            "Do not include any markdown formatting (like ```json), just the raw JSON string."
        )

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",  # or gpt-3.5-turbo, using a capable model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )

            content = completion.choices[0].message.content.strip()

            # Basic cleanup if the model returns markdown code blocks
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

            try:
                data = json.loads(content)
                if isinstance(data, list):
                    # Validate schema
                    valid_items = []
                    for item in data:
                        if isinstance(item, dict) and "instruction" in item and "response" in item:
                            valid_items.append(item)
                    return valid_items
                else:
                    logging.warning(f"LLM output was not a list: {content}")
                    return []
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON from LLM response: {content}")
                return []

        except Exception as e:
            logging.error(f"Error calling OpenAI API: {e}")
            return []
