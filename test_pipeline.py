import pytest
import os
from main import SandboxExecutor

def test_controlled_runtime_environment_failure_capture():
    executor = SandboxExecutor(timeout=2)
    temp_test_file = "temp_test_bug.py"
    with open(temp_test_file, "w") as f:
        f.write("import sys\nprint('Fintech Module Check')\nsys.exit(1)\n")
    is_passed, stdout, stderr = executor.execute_file(temp_test_file)
    assert is_passed is False
    if os.path.exists(temp_test_file): os.remove(temp_test_file)
