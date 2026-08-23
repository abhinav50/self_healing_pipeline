import os
from google import genai

class CodeAnalyzer:
    def __init__(self):
        # ⚠️ YAHAN APNI REAL GEMINI KEY DALEN (Jo AIzaSy... se shuru hoti hai)
        self.api_key = "AQ.Ab8RN6LN512s90w8PJwbFCPPbnuH__APbU2Vk04tzWw4UsE4Zg"
        self.client = "AQ.Ab8RN6LN512s90w8PJwbFCPPbnuH__APbU2Vk04tzWw4UsE4Zg"

    def diagnose_error(self, code_content: str, stderr: str) -> str:
        prompt = f"""
        You are an Elite Security and Code Auditor. Analyze this Python code and the accompanying runtime crash error.
        Target Code: {code_content}
        Runtime Error Traceback: {stderr}
        Task: Pinpoint the exact line of failure and root cause. Keep it brief.
        """
        response = self.client.models.generate_content(
            model='gemini-2.5-flash', # standard stable user model
            contents=prompt
        )
        return response.text
