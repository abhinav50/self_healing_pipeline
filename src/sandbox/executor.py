import subprocess
import sys

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
            return False, "", "ERR_TIMEOUT: Limit exceeded."
        except Exception as e:
            return False, "", f"ERR_SYSTEM: {str(e)}"
