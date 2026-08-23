import os
import json
import re
from google import genai

class CodeHealer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY context environment layer is missing.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_patch(self, code_content: str, diagnosis: str) -> dict:
        """Generates a targeted replacement patch dictionary string replacement."""
        prompt = f"""
        You are a Senior Core Software Engineer. Instead of rewriting the code, generate a targeted replacement patch dictionary string replacement.
        Original Code: {code_content}
        Error Diagnosis: {diagnosis}
        Return ONLY a strict JSON object mapping the exact old broken line string to the new safe replacement line string wrapped in ```json ``` markdown blocks.
        """
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        json_match = re.search(r"```json(.*?)```", response.text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except:
                return {}
        return {}

    def apply_patch(self, file_path: str, patch_dict: dict) -> None:
        if not patch_dict:
            return
        with open(file_path, "r") as f:
            content = f.read()
        for old_line, new_line in patch_dict.items():
            if old_line.strip() in content:
                content = content.replace(old_line, new_line)
        with open(file_path, "w") as f:
            f.write(content)
