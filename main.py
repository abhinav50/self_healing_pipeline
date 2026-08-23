import os
import re
import json
import time
import subprocess
import sys

# ====================================================
# 🎛️ SECURITY LAYER: EXPLICIT ENVIRONMENT CHECK
# ====================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "CRITICAL PROCESS ERROR: GEMINI_API_KEY process variable context is absent.\n"
        "Execution blocked. Please run: $env:GEMINI_API_KEY='your_key' inside shell configuration gates."
    )

from google import genai
client = genai.Client(api_key=GEMINI_API_KEY)

# ====================================================
# 🧪 MODULE 1: CONTROLLED RUNTIME ENVIRONMENT ENVELOPE
# ====================================================
class ControlledRuntimeEnvironment:
    """
    Implements a controlled subprocess-based execution wrapper with resource boundaries 
    and explicit timeout limits instead of naked shell injection.
    """
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def execute_safely(self, file_path: str) -> tuple[bool, str, str]:
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
            return False, "", "ERR_TIMEOUT: Thread execution exceeded absolute timeout limits."
        except Exception as e:
            return False, "", f"ERR_SYSTEM_CORE_FAIL: Compilation structural crash - {str(e)}"

# ====================================================
# 🧠 MODULE 2: AI REASONING DIAGNOSIS LAYER
# ====================================================
class IntelligenceCore:
    def diagnose_fault(self, code_content: str, stderr: str) -> str:
        prompt = f"""
        You are an Elite Security and Code Auditor. Analyze this Python fintech microservice and its runtime crash traceback.
        
        Target Code:
        {code_content}
        
        Traceback:
        {stderr}
        
        Task: Pinpoint the exact line of failure and the fix. Keep it brief and technical. No pleasantries.
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text

# ====================================================
# 🔧 MODULE 3: VERIFIED PATCH & ROLLBACK ENGINE (DIFF)
# ====================================================
class PatchManager:
    def generate_validated_patch(self, code_content: str, diagnosis: str) -> dict:
        prompt = f"""
        You are a Senior Core Software Engineer. Instead of rewriting the code, generate a targeted replacement patch dictionary.
        
        Source Code:
        {code_content}
        
        Diagnosis:
        {diagnosis}
        
        Return ONLY a strict JSON object mapping the exact old broken line string to the new safe replacement line string wrapped in ```json ``` blocks.
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        json_match = re.search(r"```json(.*?)```", response.text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except json.JSONDecodeError:
                return {}
        return {}

    def apply_patch_safely(self, file_path: str, patch_dict: dict) -> tuple[bool, str]:
        """Applies a micro-patch with unique matching constraints to prevent global corruption."""
        if not patch_dict:
            return False, "Empty or invalid patch structure generated."
            
        with open(file_path, "r") as f:
            content = f.read()

        for old_line, new_line in patch_dict.items():
            occurrences = content.count(old_line)
            if occurrences == 0:
                return False, f"Validation Failed: Target line variant '{old_line}' absent in codebase."
            if occurrences > 1:
                return False, f"Validation Failed: Multi-match anomaly. Target line is not unique."

            print(f"\n⚡ INPLACE PATCH DIFF PARITY:")
            print(f"   [-] REMOVE: '{old_line.strip()}'")
            print(f"   [+] INSERT: '{new_line.strip()}'")
            content = content.replace(old_line, new_line)

        with open(file_path, "w") as f:
            f.write(content)
        return True, "Patch state committed to file system."

# ====================================================
# 🚀 MODULE 4: ARCHITECTURAL PIPELINE ORCHESTRATOR
# ====================================================
class PipelineOrchestrator:
    def __init__(self, max_attempts: int = 3):
        self.runtime = ControlledRuntimeEnvironment()
        self.intelligence = IntelligenceCore()
        self.patcher = PatchManager()
        self.max_attempts = max_attempts

    def orchestrate_healing(self, target_file: str):
        print("====================================================")
        print("🛰️ OMNIHEAL V5: AUTONOMOUS SELF-HEALING ARCHITECTURE")
        print("====================================================\n")
        
        patch_history = []

        for attempt in range(1, self.max_attempts + 1):
            print(f"🔄 [CYCLE LOOP {attempt}/{self.max_attempts}] Verifying build telemetry checkpoints...")
            
            # Step 1: Run controlled execution environment
            is_success, stdout, stderr = self.runtime.execute_safely(target_file)
            
            if is_success:
                print(f"\n🚀 PRO-METRIC STATUS: SUCCESS! Codebase runtime fully stabilized.")
                print(f"✨ Output Stream Metric:\n{stdout.strip()}")
                self.print_observability_summary("COMPLETED", attempt, patch_history)
                return True
                
            print("⚠️ TELEMETRY MONITOR: Intercepted process exception. Capturing state buffers...")
            
            # Save backup state for potential rollback handling
            with open(target_file, "r") as f:
                backup_state = f.read()

            # Step 2: Request Diagnosis
            diagnosis = self.intelligence.diagnose_fault(backup_state, stderr)
            
            # Step 3: Compute Target Micro-Patch
            patch = self.patcher.generate_validated_patch(backup_state, diagnosis)
            print(f"📦 Delta Configuration Map: {patch}")
            
            # Step 4: Validate and Inject Patch
            is_valid, validation_msg = self.patcher.apply_patch_safely(target_file, patch)
            
            if not is_valid:
                print(f"❌ REPAIR REJECTED: {validation_msg} Advancing loop cycles.")
                patch_history.append({"cycle": attempt, "status": "VALIDATION_FAILED", "meta": patch})
                continue

            # Step 5: Test Verification Check Layer
            post_patch_success, _, post_err = self.runtime.execute_safely(target_file)
            
            if post_patch_success:
                patch_history.append({"cycle": attempt, "status": "PATCH_SUCCESS", "meta": patch})
            else:
                # ROLLBACK MECHANISM: Restore file back if compilation validation fails
                print("❌ RUNTIME TEST FAILED: Verification benchmark rejected the patch. Rolling back change...")
                with open(target_file, "w") as f:
                    f.write(backup_state)
                print("⏪ ROLLBACK COMPLETED: Codebase state returned to baseline safety index.")
                patch_history.append({"cycle": attempt, "status": "FAILED_ROLLBACK", "meta": patch, "trace": post_err})

        self.print_observability_summary("CIRCUIT_BREAKER_TRIGGERED", self.max_attempts, patch_history)
        return False

    def print_observability_summary(self, status: str, cycles: int, history: list):
        print("\n====================================================")
        print("📊 PIPELINE OBSERVABILITY INSIGHT MATRIX SUMMARY:")
        print("====================================================")
        print(f" Root Cause Check : Dynamic Traceback Analysis Logging")
        print(f" Safety Protocols : Patch Validation & Unique Match Logic")
        print(f" Execution History: {json.dumps(history, indent=2)}")
        print(f" Loop Diagnostics : Total {cycles} state cycles processed")
        print(f" Final System Node: State [{status}] Operational.")
        print("====================================================")

# ====================================================
# 🏃‍♂️ PLATFORM ENTRY BOOTSTRAPPER (Clean Flow Fixed)
# ====================================================
if __name__ == "__main__":
    target_app = "examples/buggy_app.py"
    
    if not os.path.exists("examples"):
        os.makedirs("examples")
        
    # Standard Fintech Mock Application initialization fixture
    fintech_mock_code = """def execute_payment_ledger_routing(transaction_payload):
    # Core Infrastructure Check - Simulated zero weighting division fault point
    system_load_weight = 100 / 0
    return f"Ledger routing matrix: processed with load indices {system_load_weight}"

if __name__ == "__main__":
    print(execute_payment_ledger_routing({"amount": 1200, "currency": "INR"}))
"""
    with open(target_app, "w") as f:
        f.write(fintech_mock_code)

    orchestrator = PipelineOrchestrator(max_attempts=3)
    orchestrator.orchestrate_healing(target_app)
