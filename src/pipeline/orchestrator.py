import time
from src.sandbox.executor import SandboxExecutor
from src.agent.analyzer import CodeAnalyzer
from src.agent.healer import CodeHealer

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
            
            # Step 1: Execute file and check for errors
            is_passed, stdout, stderr = self.executor.execute_file(target_file)
            
            if is_passed:
                print(f"\n🎉 SUCCESS! Target stabilized on attempt {attempt}.")
                print("====================================================")
                return True
                
            print("⚠️ DETECTION: Runtime crash captured! Analyzing root cause...")
            
            # Read current broken code
            with open(target_file, "r") as f:
                current_code = f.read()
                
            # Step 2: AI Diagnoses the issue
            diagnosis = self.analyzer.diagnose_error(current_code, stderr)
            
            # Step 3: AI generates micro-patch instead of full rewrite
            print("🔧 REPAIR: Engineering dynamic target micro-patch...")
            patch = self.healer.generate_patch(current_code, diagnosis)
            print(f"📦 Patch Diff Generated: {patch}")
            
            # Step 4: Apply target patch
            self.healer.apply_patch(target_file, patch)
            time.sleep(1)
            
        print("\n🚨 CRITICAL FAILURE: Circuit breaker triggered.")
        return False
