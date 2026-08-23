import os
from google import genai

class CodeAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def diagnose_error(self, code_content: str, stderr: str) -> str:
        prompt = f"Analyze this Python code and error to pinpoint the failure line:\n\nCode:\n{code_content}\n\nError:\n{stderr}"
        response = self.client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
        return response.text
