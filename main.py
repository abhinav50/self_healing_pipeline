import os
import re
import subprocess
import sys
from google import genai

# Hamara free Gemini Setup bina kisi terminal command ya environment variables ke lafde ke!
# ⚠️ NICHE APNI APNI REAL GEMINI KEY DALEN (Jo AIzaSy... se shuru hoti hai)
GEMINI_API_KEY = "AQ.Ab8RN6KdskGAibVsGdpTROT1FhS48mHALIsHqNNFmkI68xTDdg"

client = genai.Client(api_key=GEMINI_API_KEY)

def extract_clean_code(ai_output):
    """AI ke response se pure Python code extract karne ke liye helper"""
    code_match = re.search(r"```python(.*?)```", ai_output, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    return ai_output.strip()

def run_automated_sandbox_test(file_path):
    """Subprocess sandbox runtime testing engine"""
    print(f"🧪 Running automated sandbox tests on {file_path}...")
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("🚀 Sandbox Status: ALL TESTS PASSED SUCCESSFULLY!")
            return True, None
        else:
            print("⚠️ Sandbox Status: RUNTIME CRASH DETECTED!")
            combined_error = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            return False, combined_error
    except Exception as e:
        return False, f"Execution failed pipeline crash: {str(e)}"

def ask_ai_to_heal_code(code_content, error_feedback=None):
    """Gemini API se direct code heal karwane ka function"""
    feedback_str = ""
    if error_feedback:
        feedback_str = f"\n\nCRITICAL: Previous patch attempt FAILED with this runtime error. Fix this too:\n{error_feedback}"

    prompt = f"""
    You are a Senior Software Engineer. Analyze the following Python code for any hidden bugs, potential crashes, or unexpected runtime failures. 
    Rewrite the entire Python code to be completely safe, resilient, and handle all edge cases.
    
    Target Code:
    {code_content}
    {feedback_str}
    
    Return ONLY the complete updated python code wrapped inside a markdown block starting with ```python and ending with ```. Do not include any extra text.
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )
    return response.text

def start_self_healing_pipeline():
    target_file = "sandbox/app.py"
    max_attempts = 3
    error_feedback = None
    
    print("====================================================")
    print("🤖 STARTING AUTONOMOUS SELF-HEALING ENGINE (Gemini) 🤖")
    print("====================================================\n")

    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 [ATTEMPT {attempt}/{max_attempts}] Reading codebase file...")
        with open(target_file, "r") as f:
            current_code = f.read()

        print("🧠 AI is analyzing and designing the healing patch...")
        ai_response = ask_ai_to_heal_code(current_code, error_feedback)
        healed_code = extract_clean_code(ai_response)

        with open(target_file, "w") as f:
            f.write(healed_code)

        is_success, runtime_error = run_automated_sandbox_test(target_file)

        if is_success:
            print(f"\n🎉 SUCCESS! Codebase successfully healed on attempt {attempt}.")
            print("====================================================")
            return
        else:
            print(f"❌ Attempt {attempt} failed. Feedback loop triggered.")
            error_feedback = runtime_error

    print("\n🚨 PIPELINE ALERT: Unable to heal code automatically within max attempts.")
    print("====================================================")

if __name__ == "__main__":
    start_self_healing_pipeline()
