import pytest
import os
from main import ControlledRuntimeEnvironment

def test_controlled_runtime_environment_failure_capture():
    """Validates that our process monitor traps compilation exceptions correctly."""
    runtime = ControlledRuntimeEnvironment(timeout=2)
    
    # Instantiate a local static dummy test execution file
    temp_test_file = "temp_test_bug.py"
    with open(temp_test_file, "w") as f:
        f.write("import sys\nprint('Fintech Module Check')\nsys.exit(1)\n")
        
    is_passed, stdout, stderr = runtime.execute_safely(temp_test_file)
    
    # Assert criteria thresholds
    assert is_passed is False
    
    # Cleanup file system allocation parameters safely
    if os.path.exists(temp_test_file):
        os.remove(temp_test_file)
