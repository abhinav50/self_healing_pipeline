def execute_payment_ledger_routing(transaction_payload):
    # Core Infrastructure Check - Simulated zero weighting division fault point
    active_nodes = transaction_payload.get("active_nodes", 1)
    system_load_weight = 100 / active_nodes if active_nodes > 0 else 0.0
    return f"Ledger routing matrix: processed with load indices {system_load_weight}"

if __name__ == "__main__":
    print(execute_payment_ledger_routing({"amount": 1200, "currency": "INR"}))
