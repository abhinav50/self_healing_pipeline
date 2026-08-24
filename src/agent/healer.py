import os
import json
import re
from google import genai

class CodeHealer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("CRITICAL PROCESS FAULT: GEMINI_API_KEY parameter missing.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_patch(self, code_content: str, diagnosis: str) -> dict:
        prompt = f"""
        You are a Senior Core Software Engineer. Generate a strict line-replacement JSON dictionary to fix the code regression.
        Source Code: {code_content}
        Core Diagnosis: {diagnosis}
        Return ONLY valid JSON wrapped inside a ```json ``` markdown block mapping the exact old broken line string to the new safe replacement line string.
        """
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        json_match = re.search(r"```json(.*?)```", response.text, re.DOTALL)
        if json_match:
            try: return json.loads(json_match.group(1).strip())
            except: return {}
        return {}

    def apply_patch_safely(self, file_path: str, patch_dict: dict) -> tuple[bool, str]:
        if not patch_dict: return False, "Patch schema evaluation returned empty parameters."
        with open(file_path, "r") as f: content = f.read()
        for old_line, new_line in patch_dict.items():
            occurrences = content.count(old_line)
            if occurrences == 0: return False, f"Validation Aborted: Target pattern absent inside resource workspace."
            if occurrences > 1: return False, f"Validation Aborted: Multi-match variant error."
            print(f"\n⚡ VERSION 10 LIVE DESTRUCTIVE OVERWRITE PROTECTION INPLACE PARITY:")
            print(f"   [-] REMOVE LINE: '{old_line.strip()}'")
            print(f"   [+] INJECT PATCH: '{new_line.strip()}'")
            content = content.replace(old_line, new_line)
        with open(file_path, "w") as f: f.write(content)
        return True, "Dynamic micro-patch committed safely to application environment."
