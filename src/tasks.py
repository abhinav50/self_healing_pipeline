from crewai import Task
from src.agents import scanner_agent, patch_agent

def create_tasks(file_content, pipeline_error_feedback=None):
    # Agar pehla run crash hua hoga, toh AI ko runtime error ka feedback denge
    feedback_str = ""
    if pipeline_error_feedback:
        feedback_str = f"\n\nCRITICAL: Previous patch attempt FAILED with this runtime error. You MUST fix this error too:\n{pipeline_error_feedback}"

    # Task 1: Code ko check karne ka kaam
    scan_description = f"Analyze the following Python code and list all hidden bugs, potential crashes, and unexpected runtime failures:\n\n{file_content}{feedback_str}"
    
    scan_task = Task(
        description=scan_description,
        expected_output="A structured report highlighting the lines, issues found, and why it breaks structural logic.",
        agent=scanner_agent
    )

    # Task 2: Code ko automatic theek karne ka kaam
    heal_task = Task(
        description="Take the report from the scanner agent and rewrite the entire Python code to be resilient. Wrap the complete updated python script inside a code block starting with ```python and ending with ```. Do not output anything else.",
        expected_output="The entire updated and clean Python source code inside a single valid markdown code block.",
        agent=patch_agent
    )

    return [scan_task, heal_task]
