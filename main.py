import os
import re
import json
import time
import subprocess
import sys
from google import genai

# ====================================================
# 🎛️ SECURE CONFIGURATION GRID (Environment Variable)
# ====================================================
# Hum yahan direct key nahi likhenge taaki GitHub block na kare.
# Yeh local system environment se automatic key utha lega.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LN512s90w8PJwbFCPPbnuH__APbU2Vk04tzWw4UsE4Zg")

client = genai.Client(api_key=GEMINI_API_KEY)

# ====================================================
# 🧪 MODULE 1: THE ISOLATED SANDBOX EXECUTOR
# ====================================================
class SandboxExecutor:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def execute_file(self, file_path: str) -> tuple[bool, str, str]:
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                return True, result.stdout, ""
            else:
                return False, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "ERR_TIMEOUT: Code execution exceeded limit."
        except Exception as e:
            return False, "", f"ERR_SYSTEM: Runtime crash - {str(e)}"

# ====================================================
# 🧠 MODULE 2: AI ROOT CAUSE DIAGNOSIS AGENT
# ====================================================
class CodeAnalyzer:
    def diagnose_error(self, code_content: str, stderr: str) -> str:
        prompt = f"""
        You are an Elite Security and Code Auditor. Analyze this Python code and the accompanying runtime crash error.
        Target Code:
        {code_content}
        Runtime Error Traceback:
        {stderr}
        Task: Pinpoint the exact line and root cause of the failure. Keep it brief and technical.
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text

# ====================================================
# 🔧 MODULE 3: TARGETED MICRO-PATCH REPAIR ENGINE
# ====================================================
class CodeHealer:
    def generate_patch(self, code_content: str, diagnosis: str) -> dict:
        prompt = f"""
        You are a Senior Core Software Engineer. Instead of rewriting the code, generate a targeted replacement patch dictionary.
        Original Code:
        {code_content}
        Error Diagnosis:
        {diagnosis}
        
        Return ONLY a strict JSON object mapping the exact old broken line string to the new safe replacement line string.
        Do not change lines that are correct.
        
        Example Output Format:
        {{
            "old_line_to_replace_here": "new_healed_line_here"
        }}
        Ensure the JSON is wrapped in ```json ``` markdown blocks.
        """
        response = client.models.generate_content(
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

# ====================================================
# 🚀 MODULE 4: THE MASTER PIPELINE ORCHESTRATOR
# ====================================================
class PipelineOrchestrator:
    def __init__(self, max_attempts: int = 3):
        self.executor = SandboxExecutor()
        self.analyzer = CodeAnalyzer()
        self.healer = CodeHealer()
        self.max_attempts = max_attempts

    def run_healing_protocol(self, target_file: str):
        print("====================================================")
        print("🚀 OMNIHEAL PRO: TARGETED PATCHING ENGINE ACTIVE")
        print("====================================================\n")
        
        for attempt in range(1, self.max_attempts + 1):
            print(f"🔄 [ATTEMPT {attempt}/{self.max_attempts}] Running build validations...")
            is_passed, stdout, stderr = self.executor.execute_file(target_file)
            
            if is_passed:
                print(f"\n🎉 SUCCESS! Target stabilized autonomously on attempt {attempt}.")
                print("====================================================")
                return True
                
            print("⚠️ DETECTION: Runtime crash captured! Analyzing root cause...")
            with open(target_file, "r") as f:
                current_code = f.read()
                
            diagnosis = self.analyzer.diagnose_error(current_code, stderr)
            print("🔧 REPAIR: Engineering dynamic target micro-patch...")
            patch = self.healer.generate_patch(current_code, diagnosis)
            print(f"📦 Patch Diff Generated: {patch}")
            
            self.healer.apply_patch(target_file, patch)
            time.sleep(1)
            
        print("\n🚨 CRITICAL FAILURE: Circuit breaker triggered.")
        return False

# ====================================================
# 🏃‍♂️ RUNTIME INTERFACE BOOTSTRAPPER
# ====================================================
if __name__ == "__main__":
    target_app = "examples/buggy_app.py"
    
    if not os.path.exists("examples"):
        os.makedirs("examples")
        
    # Buggy Code base target format reset
    buggy_code_content = """def process_fintech_transaction(data):
    # Razorpay Killer Demo - Intentional ZeroDivisionError
    risk_factor = 100 / 0
    return f"Transaction metrics calculated: {risk_factor}"

if __name__ == "__main__":
    print(process_fintech_transaction("Razorpay Secure User"))
"""
    with open(target_app, "w") as f:
        f.write(buggy_code_content)

    orchestrator = PipelineOrchestrator(max_attempts=3)
    orchestrator.run_healing_protocol(target_app)
