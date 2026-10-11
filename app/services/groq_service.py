import json
import logging
from typing import List
from groq import Groq
from pydantic import ValidationError

from app.models.analysis_models import UserInput, SearchResult, PlacementReport
from app.prompts.placement_prompt import generate_placement_prompt

class GroqService:
    def __init__(self, api_key: str, model_name: str):
        self.client = Groq(api_key=api_key)
        self.model = model_name

    def _extract_json_from_markdown(self, text: str) -> str:
        """Safely extract JSON if wrapped in markdown code blocks."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()

    def generate_report(self, user_input: UserInput, search_results: List[SearchResult]) -> PlacementReport:
        """Send data to Groq and return a validated Pydantic model."""
        prompt = generate_placement_prompt(user_input, search_results)
        
        system_msg = {
            "role": "system",
            "content": "You are an expert AI career coach and placement strategist. You output ONLY valid JSON without any markdown wrapping or conversational text."
        }
        
        user_msg = {
            "role": "user",
            "content": prompt
        }
        
        messages = [system_msg, user_msg]
        
        # Initial Attempt
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
            )
            
            raw_text = response.choices[0].message.content
            cleaned_text = self._extract_json_from_markdown(raw_text)
            
            data = json.loads(cleaned_text)
            return PlacementReport(**data)
            
        except (json.JSONDecodeError, ValidationError) as e:
            logging.debug(f"First attempt failed: {e}. Retrying...")
            # Retry Once
            return self._retry_generation(messages, str(e), raw_text if 'raw_text' in locals() else "")
            
    def _retry_generation(self, original_messages: list, error_msg: str, previous_output: str) -> PlacementReport:
        """Retry generation asking Groq to fix the JSON."""
        retry_messages = original_messages.copy()
        if previous_output:
            retry_messages.append({
                "role": "assistant",
                "content": previous_output
            })
            retry_messages.append({
                "role": "user",
                "content": f"Your previous output caused a validation error:\n{error_msg}\n\nPlease provide ONLY valid JSON satisfying the schema. Do not include markdown codeblocks."
            })
        else:
            retry_messages.append({
                "role": "user",
                "content": "Ensure you return strictly valid JSON matching the requested schema."
            })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=retry_messages,
            temperature=0.1,
        )
        
        raw_text = response.choices[0].message.content
        cleaned_text = self._extract_json_from_markdown(raw_text)
        
        data = json.loads(cleaned_text)
        return PlacementReport(**data)
