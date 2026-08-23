import os
import json
import re
from google import genai

class CodeHealer:
    def __init__(self):
        # ⚠️ YAHAN BHI APNI REAL GEMINI KEY DALEN (Jo AIzaSy... se shuru hoti hai)
        self.api_key = "AQ.Ab8RN6LN512s90w8PJwbFCPPbnuH__APbU2Vk04tzWw4UsE4Zg"
        self.client = "AQ.Ab8RN6LN512s90w8PJwbFCPPbnuH__APbU2Vk04tzWw4UsE4Zg"

    def generate_patch(self, code_content: str, diagnosis: str) -> dict:
        prompt = f"""
        You are a Senior Core Software Engineer. Generate a targeted replacement patch dictionary.
        Original Code: {code_content}
        Error Diagnosis: {diagnosis}
        Return ONLY a strict JSON object mapping the exact old broken line string to the new safe replacement line string wrapped in ```json ``` blocks.
        """
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        json_match = re.search(r"```json(.*?)```", response.text, re.DOTALL)
        if json_match:
            try: return json.loads(json_match.group(1).strip())
            except: return {}
        return {}

    def apply_patch(self, file_path: str, patch_dict: dict) -> None:
        if not patch_dict: return
        with open(file_path, "r") as f: content = f.read()
        for old_line, new_line in patch_dict.items():
            if old_line.strip() in content: content = content.replace(old_line, new_line)
        with open(file_path, "w") as f: f.write(content)
