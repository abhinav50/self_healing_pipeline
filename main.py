import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.pipeline.orchestrator import PipelineOrchestrator

def boot_v10_enterprise_pipeline():
    target_microservice = "examples/buggy_app.py"
    if not os.path.exists("examples"): 
        os.makedirs("examples")
        
    fintech_isolated_logic = """def execute_payment_ledger_routing(transaction_payload):
    system_load_weight = 100 / 0
    return f"Ledger metrics state map: indices synchronized with load parameters {system_load_weight}"

if __name__ == "__main__":
    print(execute_payment_ledger_routing({"amount": 5400, "token": "INR"}))
"""
    with open(target_microservice, "w") as f: 
        f.write(fintech_isolated_logic)
        
    orchestrator = PipelineOrchestrator(max_attempts=3)
    orchestrator.run_healing_protocol(target_microservice)

if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ CRITICAL BOOT BLOCKED: GEMINI_API_KEY parameter missing inside process variables scope.")
        sys.exit(1)
    boot_v10_enterprise_pipeline()
