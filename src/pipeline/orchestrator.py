import time
import json
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
        print("🛰️ OMNIHEAL V10: DISTRIBUTED SELF-OPTIMIZING ENGINE")
        print("====================================================\n")
        execution_history = []
        for attempt in range(1, self.max_attempts + 1):
            print(f"🔄 [V10 CYCLE {attempt}/{self.max_attempts}] Performing structural telemetry analysis...")
            is_success, stdout, stderr = self.executor.execute_file(target_file)
            if is_success:
                print(f"\n🚀 CORE STATUS METRIC: SUCCESS! Distributed nodes stabilized.")
                print(f"✨ Output Payload Stream:\n{stdout.strip()}")
                self.print_v10_observability_matrix("STABILIZED", attempt, execution_history)
                return True
            print("⚠️ FAULT DETECTION: Controlled runtime boundary trapped a process exception.")
            with open(target_file, "r") as f: backup_state = f.read()
            diagnosis = self.analyzer.diagnose_error(backup_state, stderr)
            print("🔧 REPAIR LAYER: Engineering dynamic token configuration mapping...")
            patch = self.healer.generate_patch(backup_state, diagnosis)
            print(f"📦 Active Patch Metrics: {patch}")
            is_applied, validation_msg = self.healer.apply_patch_safely(target_file, patch)
            if not is_applied:
                execution_history.append({"attempt": attempt, "state": "VALIDATION_FAILED", "patch": patch})
                continue
            post_check_success, _, post_err = self.executor.execute_file(target_file)
            if post_check_success:
                execution_history.append({"attempt": attempt, "state": "PATCH_VERIFIED_SUCCESS", "patch": patch})
            else:
                print("❌ RUNTIME REJECTION: Build verification failed post-patch. Rolling back changes...")
                with open(target_file, "w") as f: f.write(backup_state)
                print("⏪ FAULT DEACTIVATED: Local state rolled back safely to baseline benchmarks.")
                execution_history.append({"attempt": attempt, "state": "FAILED_ROLLBACK_SAFE", "patch": patch, "trace": post_err})
            time.sleep(1)
        self.print_v10_observability_matrix("CIRCUIT_BREAKER_ACTIVE", self.max_attempts, execution_history)
        return False

    def print_v10_observability_matrix(self, status: str, attempts: int, telemetry_logs: list):
        print("\n====================================================")
        print("📊 VERSION 10 ABSOLUTE OBSERVABILITY METRICS REPORT:")
        print("====================================================")
        print(f" Framework Strategy: Non-Destructive Grammatical Diff Replacements")
        print(f" Rollback Integrity: Native Active Backups Vector Tracking")
        print(f" Trace Logs Summary: {json.dumps(telemetry_logs, indent=2)}")
        print(f" Runtime Iterations: Total {attempts} complete automation cycles run")
        print(f" Final Machine Node: State [{status}] Operational Protocol Complete.")
        print("====================================================")
