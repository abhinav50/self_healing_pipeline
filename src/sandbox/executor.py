import subprocess
import sys
import time

class SandboxExecutor:
    """
    Implements a highly stable controlled execution environment equipped with explicit 
    thread timeout boundaries and native capture buffers tracking process latency.
    """
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def execute_file(self, file_path: str) -> tuple[bool, str, str, float]:
        """Runs the destination script inside isolated execution constraints."""
        start_time = time.perf_counter()
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            duration = time.perf_counter() - start_time
            if result.returncode == 0:
                return True, result.stdout, "", duration
            else:
                return False, result.stdout, result.stderr, duration
        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - start_time
            return False, "", "ERR_TIMEOUT: Sandbox process threads bounds exceeded time-to-live thresholds.", duration
        except Exception as e:
            duration = time.perf_counter() - start_time
            return False, "", f"ERR_COMPILATION_CRASH: Base executor runtime crash - {str(e)}", duration
