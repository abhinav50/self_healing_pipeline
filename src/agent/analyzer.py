import os
from google import genai

class CodeAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("CRITICAL PROCESS FAULT: GEMINI_API_KEY parameter missing.")
        self.client = genai.Client(api_key=self.api_key)

    def diagnose_error(self, code_content: str, stderr: str) -> str:
        prompt = f"""
        You are an Elite Security and Code Auditor. Analyze this Python code and the accompanying runtime crash error.
        Target Code: {code_content}
        Traceback Stream: {stderr}
        Task: Pinpoint the exact failure node line and state the required correction pattern. No chat preamble.
        """
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text
