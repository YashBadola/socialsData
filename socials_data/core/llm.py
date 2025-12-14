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
        Uses a diverse prompting strategy to create varied instruction types (advice, explanation, critique).
        """
        if not self.client:
            return []

        # Diverse instruction generation prompt
        user_message = (
            "You are an expert dataset creator for training Large Language Models (LLMs) to adopt specific personas.\n"
            "Your task is to generate 3-5 high-quality instruction-response pairs based on the provided text chunk.\n"
            "The responses MUST embody the persona defined in the system prompt below.\n\n"
            f"Persona Definition (System Prompt):\n{system_prompt}\n\n"
            f"Source Text:\n{text_chunk}\n\n"
            "Guidelines:\n"
            "1. **Diverse Instructions**: Do not just ask 'What does the text say?'. Generate varied types of instructions, such as:\n"
            "   - **Advice Seeking**: 'I am feeling anxious about the future. What should I do?'\n"
            "   - **Philosophical Inquiry**: 'What is the nature of evil?'\n"
            "   - **Situational**: 'How should one handle an insult from a colleague?'\n"
            "   - **Direct Analysis**: 'Explain your view on...' \n"
            "2. **Persona Alignment**: The 'response' must be written *in the voice* of the persona. It should sound like the character speaking directly to the user.\n"
            "3. **Contextual grounding**: Use the source text as the *knowledge base* for the answers, but expand on it naturally using the persona's logic.\n"
            "4. **Format**: Output a pure JSON array of objects. Each object must have keys: \"instruction\" and \"response\".\n"
            "   Example: [{\"instruction\": \"...\", \"response\": \"...\"}]\n"
        )

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates training data."},
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
