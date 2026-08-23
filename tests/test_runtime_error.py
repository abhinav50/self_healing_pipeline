import pytest
import os
from src.sandbox.executor import SandboxExecutor

def test_controlled_runtime_execution_engine():
    """Validates if our sandbox core execution hooks capture infrastructure failures deterministically."""
    executor = SandboxExecutor(timeout=2)
    
    # Create a dynamic mock runtime file for testing configuration scopes safely
    mock_file = "tests/mock_demo_app.py"
    with open(mock_file, "w") as f:
        f.write("import sys\nprint('Build initialization setup')\nsys.exit(1)\n")
        
    is_success, stdout, stderr = executor.execute_file(mock_file)
    
    # Assert validation thresholds metrics (Should capture exit code 1 as False)
    assert is_success is False
    
    # Cleanup storage system allocations safely
    if os.path.exists(mock_file):
        os.remove(mock_file)
