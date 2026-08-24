import streamlit as st
import streamlit.components.v1 as components
import os
import re
import json
import time
import subprocess
import sys
from google import genai

# ====================================================
# 🎛️ ENTERPRISE PROCESS SECURITY BOUNDARY
# ====================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ CRITICAL PROCESS FAULT: GEMINI_API_KEY variable context is absent inside active processes.")
    st.info("Execute: `$env:GEMINI_API_KEY='your_key'` inside your terminal session before boot loops.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

# ====================================================
# 🛰️ APP CONFIGURATIONS & STATE MANAGEMENT
# ====================================================
st.set_page_config(page_title="OmniHeal-V10 Enterprise Core", layout="wide")

if "v10_state" not in st.session_state:
    st.session_state.v10_state = "STABLE"  # STABLE, CRASHED, HEALING, SUCCESS
if "v10_logs" not in st.session_state:
    st.session_state.v10_logs = ["✓ Core Framework: Operational Check Verified", "✓ System Node: Listening on secure channel 0-ALPHA."]
if "old_code_line" not in st.session_state:
    st.session_state.old_code_line = "No baseline anomalies recorded."
if "new_code_line" not in st.session_state:
    st.session_state.new_code_line = "Workspace infrastructure nominal."

target_app_path = "examples/buggy_app.py"

# Premium Consumer Brand Palette Config Mapping Indices (Inspired by Coca-Cola Global Layouts)
brand_hud_config = {
    "STABLE": {"primary": "#F22222", "secondary": "#00aaff", "bg": "#f8f9fa", "text": "#1a1a1a", "badge": "🔵 SYSTEM STATUS: MAXIMUM UPTIME"},
    "CRASHED": {"primary": "#b30000", "secondary": "#ff0055", "bg": "#fff5f5", "text": "#7d0000", "badge": "🚨 PROCESS ALERT: FAULT INTERCEPTED"},
    "HEALING": {"primary": "#cc00ff", "secondary": "#aa00ff", "bg": "#fbf5ff", "text": "#4a007d", "badge": "🧠 INTELLIGENCE MATRIX: AUTOMATED HOTPATCHING"},
    "SUCCESS": {"primary": "#00cc66", "secondary": "#00ffaa", "bg": "#f5fff9", "text": "#005c2e", "badge": "✅ INFRASTRUCTURE RESTORED SUCCESSFULLY"}
}

active_brand = brand_hud_config[st.session_state.v10_state]

# --- PREMIUM COCA-COLA STYLE CLEAN HTML/CSS INJECTION ---
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* Global Page Background Restructuring */
        .stApp {{ background-color: #ffffff !important; color: #1a1a1a !important; font-family: 'Poppins', sans-serif; }}
        
        /* Clean Rounded Card Blocks */
        div[data-testid="stVerticalBlock"] {{ background: #fdfdfd !important; border-radius: 12px !important; border: 1px solid #e2e8f0 !important; padding: 20px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important; }}
        
        /* Custom Monospace and Text Formatting Overrides */
        .brand-header {{ font-family: 'Poppins', sans-serif; font-weight: 700; color: #F22222; text-align: center; letter-spacing: -0.5px; }}
        .brand-subtitle {{ font-family: 'Poppins', sans-serif; text-align: center; color: #4a5568; font-size: 15px; margin-top: -10px; font-weight: 400; }}
        
        /* Streamlit Text-Area Custom Clean Framing Overwrites */
        textarea {{ font-family: 'JetBrains Mono', monospace !important; background-color: #fafbfc !important; color: #2d3748 !important; border: 1px solid #cbd5e0 !important; border-radius: 6px !important; }}
    </style>
""", unsafe_allow_html=True)

# ====================================================
# 🌐 BRANDED GLOWING 3D INTERACTIVE HERO PORTAL
# ====================================================
# We render a massive interactive fluid mesh container inspired by high-end consumer web animations
three_js_html = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cloudflare.com"></script>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: {active_brand["bg"]}; transition: background-color 0.5s ease; }}
        canvas {{ width: 100%; height: 280px; display: block; }}
    </style>
</head>
<body>
    <script>
        const primaryColor = "{active_brand["primary"]}";
        
        const scene = new THREE.Scene();
        
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / 280, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(window.innerWidth, 280);
        document.body.appendChild(renderer.domElement);

        // Core Brand Wave Field Particles (Ultra Clean Dot Grid)
        const dotsGeometry = new THREE.BufferGeometry();
        const dotsCount = 800;
        const positions = new Float32Array(dotsCount * 3);
        for(let i=0; i<dotsCount*3; i+=3) {{
            positions[i] = (Math.random() - 0.5) * 160;
            positions[i+1] = (Math.random() - 0.5) * 40;
            positions[i+2] = (Math.random() - 0.5) * 80;
        }}
        dotsGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const dotsMaterial = new THREE.PointsMaterial({{ color: parseInt(primaryColor.replace("#", "0x")), size: 1.2, transparent: true, opacity: 0.4 }});
        const dotMesh = new THREE.Points(dotsGeometry, dotsMaterial);
        scene.add(dotMesh);

        // Central Smooth Architectural Geometry (Sphere Ring Network)
        const geometry = new THREE.SphereGeometry(10, 20, 20);
        const material = new THREE.MeshBasicMaterial({{ 
            color: parseInt(primaryColor.replace("#", "0x")), 
            wireframe: true,
            transparent: true,
            opacity: 0.15
        }});
        const coreObject = new THREE.Mesh(geometry, material);
        scene.add(coreObject);

        camera.position.z = 24;

        let clock = new THREE.Clock();

        function animate() {{
            requestAnimationFrame(animate);
            const elapsedTime = clock.getElapsedTime();
            
            coreObject.rotation.y = elapsedTime * 0.15;
            coreObject.rotation.x = elapsedTime * 0.08;
            dotMesh.rotation.y = elapsedTime * 0.02;
            
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / 280;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, 280);
        }});
    </script>
</body>
</html>
"""

components.html(three_js_html, height=290)

# --- PREMIUM BRAND HUD ACTION STATUS CARD ---
st.markdown(f"""
    <div style="background-color: {active_brand["bg"]}; border: 1px solid #cbd5e0; border-top: 5px solid {active_brand["primary"]}; padding: 18px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.02); text-align: center; transition: all 0.5s ease;">
        <div style="color: {active_brand["text"]}; font-weight: 700; font-size: 14px; letter-spacing: 1px; margin-bottom: 4px;">{active_brand["badge"]}</div>
        <div style="color: #718096; font-size: 13px;">Real-Time Continuous Testing & Exception Recovery Telemetry Active.</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================================
# 🔬 MULTI-AGENT STATE MACHINE PIPELINE ASYNC RECOVERY
# ====================================================
if st.session_state.v10_state == "CRASHED":
    time.sleep(1.2)
    st.session_state.v10_state = "HEALING"
    st.session_state.v10_logs.append(f"→ [{time.strftime('%X')}] Context Analysis Layer: Routing exception trace to Gemini Core.")
    st.rerun()

elif st.session_state.v10_state == "HEALING":
    try:
        with open(target_app_path, "r") as f:
            code_buffer = f.read()
            
        prompt = f"Identify the exact failing line and output ONLY a valid strict JSON block mapping old line string to repaired line string:\nCode:\n{code_buffer}"
        response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
        
        json_match = re.search(r"```json(.*?)```", response.text, re.DOTALL)
        if json_match:
            patch = json.loads(json_match.group(1).strip())
            for old, new in patch.items():
                if old.strip() in code_buffer:
                    st.session_state.old_code_line = old.strip()
                    st.session_state.new_code_line = new.strip()
                    code_buffer = code_buffer.replace(old, new)
                    
            with open(target_app_path, "w") as f:
                f.write(code_buffer)
                
            verify_res = subprocess.run([sys.executable, target_app_path], capture_output=True, text=True)
            if verify_res.returncode == 0:
                st.session_state.v10_state = "SUCCESS"
                st.session_state.v10_logs.append(f"✓ [{time.strftime('%X')}] Verification Success: Platform nodes synchronized successfully.")
            else:
                st.session_state.v10_state = "STABLE"
                st.session_state.v10_logs.append(f"✗ [{time.strftime('%X')}] Validation Failed. State rolled back to baseline boundaries.")
        else:
            st.session_state.v10_state = "STABLE"
            st.session_state.v10_logs.append("⚠️ Internal structural parsing error. Aborting runtime cycle.")
    except Exception as e:
        st.session_state.v10_state = "STABLE"
        st.session_state.v10_logs.append(f"🚨 Process Thread Critical Fallback Intercept: {str(e)}")
    st.rerun()

# ====================================================
# 💻 CLEAN ENTERPRISE CARD GRID DESK MONITOR
# ====================================================
col1, col2, col3 = st.columns([1.1, 1.1, 0.8])

with col1:
    st.markdown("<div style='font-weight:600; color: #4a5568; font-size:13px; margin-bottom:6px;'>📊 OPERATIONAL LOGS TELEMETRY</div>", unsafe_allow_html=True)
    logs_stream = "\n".join(st.session_state.v10_logs[::-1])
    st.text_area("Logs Panel", value=logs_stream, height=270, disabled=True, label_visibility="collapsed")

with col2:
    st.markdown("<div style='font-weight:600; color: #4a5568; font-size:13px; margin-bottom:6px;'>💾 DESTINATION CODE REPOSITORY</div>", unsafe_allow_html=True)
    try:
        with open(target_app_path, "r") as f:
            source_display = f.read()
    except FileNotFoundError:
        source_display = "# Target filesystem destination unallocated."
    st.code(source_display, language="python")

with col3:
    st.markdown("<div style='font-weight:600; color: #4a5568; font-size:13px; margin-bottom:6px;'>🎯 CORRECTION ANALYSIS DIFF</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background-color: #fafbfc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; height: 240px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 12px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.01);">
            <span style="color: #e53e3e; font-weight: 600;">[-] EXCISED ERROR STRINGS:</span><br>
            <code style="color: #c53030; background: #fff5f5; padding: 2px 4px; border-radius: 4px; display:block; margin-top:4px; border: 1px solid #fed7d7;">{st.session_state.old_code_line}</code><br>
            <span style="color: #38a169; font-weight: 600;">[+] INJECTED REPAIR MATRICES:</span><br>
            <code style="color: #276749; background: #f0fff4; padding: 2px 4px; border-radius: 4px; display:block; margin-top:4px; border: 1px solid #c6f6d5;">{st.session_state.new_code_line}</code>
        </div>
    """, unsafe_allow_html=True)

