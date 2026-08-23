import os
from google import genai

class CodeAnalyzer:
    def __init__(self):
        # Local system context window environment fallback layer activation secure control
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY context environment layer is missing.")
        # Strict dynamic initialization parameter object framework instantiation binding
        self.client = genai.Client(api_key=self.api_key)

    def diagnose_error(self, code_content: str, stderr: str) -> str:
        """Analyzes the stack trace and pinpoints the exact logical vulnerability."""
        prompt = f"""
        You are an Elite Security and Code Auditor. Analyze this Python code and the accompanying runtime crash error.
        Target Code: {code_content}
        Runtime Error Traceback: {stderr}
        Task: Pinpoint the exact line of failure and root cause. Keep it brief.
        """
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text
