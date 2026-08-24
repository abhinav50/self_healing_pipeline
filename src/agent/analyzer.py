import os
import ast
from google import genai

class CodeAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("CRITICAL PROCESS FAULT: GEMINI_API_KEY parameter missing.")
        self.client = genai.Client(api_key=self.api_key)

    def verify_syntax_tree(self, code_content: str) -> tuple[bool, str]:
        """Parses destination files into Abstract Syntax Trees to pre-screen validation integrity."""
        try:
            ast.parse(code_content)
            return True, "AST Structural Integrity Nominal."
        except SyntaxError as se:
            return False, f"AST_COMPILE_FAULT: Line {se.lineno} - {se.msg}"

    def diagnose_error(self, code_content: str, stderr: str) -> str:
        """Parses tracebacks to calculate root cause matrix parameters securely."""
        prompt = f"""
        [ENTERPRISE RESEARCH PARADIGM: RUNTIME FAULT ISOLATION]
        Analyze the Abstract Syntax Tree structural failure and runtime telemetry data.
        Target Script Code base:
        {code_content}
        Traceback Error Logs:
        {stderr}
        Task: Pinpoint the algorithmic failure node line. Output purely technical diagnosis records. No chat preamble.
        """
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text
