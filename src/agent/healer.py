import os
from google import genai
from google.genai import types

class CodeHealer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY context layer is missing.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_validated_patch(self, code_content: str, diagnosis: str) -> dict:
        """Generates a strict targeted replacement patch schema using strict structural typing."""
        prompt = f"""
        Analyze the codebase source and diagnosis metrics. Generate a key-value mapping configuration.
        Source Code:
        {code_content}
        Core Diagnosis:
        {diagnosis}
        """
        
        # Enforcing strict JSON layout constraints via the SDK schema design model types
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "old_line_string": types.Schema(type=types.Type.STRING),
                            "new_line_string": types.Schema(type=types.Type.STRING),
                        },
                        required=["old_line_string", "new_line_string"],
                    ),
                ),
            )
            
            # Direct parsing with 0% markdown extraction latency dependencies
            import json
            data = json.loads(response.text)
            return {data["old_line_string"]: data["new_line_string"]}
        except Exception:
            return {}

    def apply_patch_safely(self, file_path: str, patch_dict: dict) -> tuple[bool, str]:
        if not patch_dict:
            return False, "Patch schema evaluation mapped empty values."
            
        with open(file_path, "r") as f:
            content = f.read()

        for old_line, new_line in patch_dict.items():
            occurrences = content.count(old_line)
            if occurrences == 0:
                return False, f"Target parameters '{old_line}' not found inside destination workspace."
            if occurrences > 1:
                return False, f"Ambiguity Anomaly: Target pattern matched multiple configuration boundaries."

            print(f"\n⚡ INPLACE SOURCE MUTATION PATTERN APPLIED:")
            print(f"   [-] OUT: '{old_line.strip()}'")
            print(f"   [+] IN : '{new_line.strip()}'")
            content = content.replace(old_line, new_line)

        with open(file_path, "w") as f:
            f.write(content)
        return True, "Code execution workspace mutated safely."
