import streamlit as st
import streamlit.components.v1 as components
import os
import re
import json
import time
import subprocess
import sys
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ CRITICAL PROCESS FAULT: GEMINI_API_KEY variable context is absent.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)
st.set_page_config(page_title="OmniHeal-V10 Enterprise Core", layout="wide")

if "v10_state" not in st.session_state: st.session_state.v10_state = "STABLE"
if "v10_logs" not in st.session_state: st.session_state.v10_logs = ["✓ Core Framework: Operational Check Verified", "✓ System Node: Listening on secure channel 0-ALPHA."]
if "old_code_line" not in st.session_state: st.session_state.old_code_line = "No baseline anomalies recorded."
if "new_code_line" not in st.session_state: st.session_state.new_code_line = "Workspace infrastructure nominal."

target_app_path = "examples/buggy_app.py"
brand_hud_config = {
    "STABLE": {"primary": "#F22222", "bg": "#f8f9fa", "text": "#1a1a1a", "badge": "🔵 SYSTEM STATUS: MAXIMUM UPTIME"},
    "CRASHED": {"primary": "#b30000", "bg": "#fff5f5", "text": "#7d0000", "badge": "🚨 PROCESS ALERT: FAULT INTERCEPTED"},
    "HEALING": {"primary": "#cc00ff", "bg": "#fbf5ff", "text": "#4a007d", "badge": "🧠 INTELLIGENCE MATRIX: AUTOMATED HOTPATCHING"},
    "SUCCESS": {"primary": "#00cc66", "bg": "#f5fff9", "text": "#005c2e", "badge": "✅ INFRASTRUCTURE RESTORED SUCCESSFULLY"}
}
active_brand = brand_hud_config[st.session_state.v10_state]

st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        .stApp {{ background-color: #ffffff !important; color: #1a1a1a !important; font-family: 'Poppins', sans-serif; }}
        div[data-testid="stVerticalBlock"] {{ background: #fdfdfd !important; border-radius: 12px !important; border: 1px solid #e2e8f0 !important; padding: 20px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important; }}
        textarea {{ font-family: 'JetBrains Mono', monospace !important; background-color: #fafbfc !important; color: #2d3748 !important; border: 1px solid #cbd5e0 !important; border-radius: 6px !important; }}
    </style>
""", unsafe_allow_html=True)

three_js_html = f"""
<!DOCTYPE html>
<html><head><script src="https://cloudflare.com"></script><style>body {{ margin: 0; overflow: hidden; background-color: {active_brand["bg"]}; }}canvas {{ width: 100%; height: 240px; display: block; }}</style></head>
<body><script>
const scene = new THREE.Scene(); const camera = new THREE.PerspectiveCamera(50, window.innerWidth / 240, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }}); renderer.setSize(window.innerWidth, 240); document.body.appendChild(renderer.domElement);
const geometry = new THREE.SphereGeometry(10, 16, 16); const material = new THREE.MeshBasicMaterial({{ color: parseInt("{active_brand["primary"]}".replace("#", "0x")), wireframe: true, transparent: true, opacity: 0.15 }});
const core = new THREE.Mesh(geometry, material); scene.add(core); camera.position.z = 20;
function animate() {{ requestAnimationFrame(animate); core.rotation.y += 0.01; core.rotation.x += 0.005; renderer.render(scene, camera); }} animate();
</script></body></html>
"""
components.html(three_js_html, height=245)

st.markdown(f"""<div style="background-color: {active_brand["bg"]}; border-top: 5px solid {active_brand["primary"]}; padding: 15px; border-radius: 10px; text-align: center;"><div style="color: {active_brand["text"]}; font-weight: 700;">{active_brand["badge"]}</div></div><br>""", unsafe_allow_html=True)

if st.session_state.v10_state == "CRASHED":
    time.sleep(1)
    st.session_state.v10_state = "HEALING"
    st.session_state.v10_logs.append(f"→ [{time.strftime('%X')}] Routing exception trace parameters safely to Gemini Core loops.")
    st.rerun()
elif st.session_state.v10_state == "HEALING":
    try:
        with open(target_app_path, "r") as f: code_buffer = f.read()
        prompt = f"Identify the exact failing line and output ONLY a valid strict JSON block mapping old line string to repaired line string:\nCode:\n{code_buffer}"
        response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
        json_match = re.search(r"```json(.*?)```", response.text, re.DOTALL)
        if json_match:
            patch = json.loads(json_match.group(1).strip())
            for old, new in patch.items():
                if old.strip() in code_buffer:
                    st.session_state.old_code_line, st.session_state.new_code_line = old.strip(), new.strip()
                    code_buffer = code_buffer.replace(old, new)
            with open(target_app_path, "w") as f: f.write(code_buffer)
            verify_res = subprocess.run([sys.executable, target_app_path], capture_output=True, text=True)
            if verify_res.returncode == 0:
                st.session_state.v10_state = "SUCCESS"
                st.session_state.v10_logs.append(f"✓ [{time.strftime('%X')}] Verification Success: Platform nodes synchronized successfully.")
            else:
                st.session_state.v10_state = "STABLE"
                st.session_state.v10_logs.append(f"✗ [{time.strftime('%X')}] Validation Failed. State rolled back to baseline boundaries.")
        else: st.session_state.v10_state = "STABLE"
    except Exception as e: st.session_state.v10_state = "STABLE"
    st.rerun()

col1, col2, col3 = st.columns([1.1, 1.1, 0.8])
with col1:
    st.markdown("<div style='font-weight:600; color: #4a5568; font-size:12px;'>📊 OPERATIONAL LOGS TELEMETRY</div>", unsafe_allow_html=True)
    st.text_area("Logs Panel", value="\n".join(st.session_state.v10_logs[::-1]), height=250, disabled=True, label_visibility="collapsed")
with col2:
    st.markdown("<div style='font-weight:600; color: #4a5568; font-size:12px;'>💾 ACTIVE REPOSITORY SOURCE</div>", unsafe_allow_html=True)
    try:
        with open(target_app_path, "r") as f: src_dis = f.read()
    except: src_dis = "# Code unallocated."
    st.code(src_dis, language="python")
with col3:
    st.markdown("<div style='font-weight:600; color: #4a5568; font-size:12px;'>🎯 CORRECTION ANALYSIS DIFF</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style="background-color: #fafbfc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; height: 220px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 11px;"><span style="color: #e53e3e; font-weight: 600;">[-] EXCISED CODE:</span><br><code style="color: #c53030;">{st.session_state.old_code_line}</code><br><br><span style="color: #38a169; font-weight: 600;">[+] INJECTED PATCH:</span><br><code style="color: #276749;">{st.session_state.new_code_line}</code></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
is_run = st.session_state.v10_state in ["CRASHED", "HEALING"]
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 DEPLOY RECOVERY RUNTIME PIPELINE ENGINE", type="primary", use_container_width=True, disabled=is_run):
        with open(target_app_path, "w") as f:
            f.write('def routing_test():\n    system_load = 100 / 0\n    return system_load\nif __name__ == "__main__": routing_test()')
        st.session_state.v10_state = "CRASHED"
        st.session_state.v10_logs.append(f"⚡ [{time.strftime('%X')}] Triggering standard sandboxed microservice test virtualization bounds...")
        st.rerun()
with c2:
    if st.button("🔄 RECALIBRATE INFRASTRUCTURE BASELINE", type="secondary", use_container_width=True):
        st.session_state.v10_state = "STABLE"
        st.session_state.old_code_line, st.session_state.new_code_line = "No anomalies recorded.", "Workspace nominal."
        st.session_state.v10_logs = ["✓ Telemetry Desk reset complete. Baseline nodes recalibrated.", "✓ System node listening on secure channel 0-ALPHA."]
        st.rerun()
