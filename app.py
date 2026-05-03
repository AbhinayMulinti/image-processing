import streamlit as st
import cv2
import numpy as np
import pathlib
import base64
from landing_page import show_landing_page

# ── Setup ─────────────────────────────────────────────────────────────────────
CSS_PATH  = pathlib.Path(__file__).parent / "style.css"
CSS       = CSS_PATH.read_text()
try:
    LOGO_PATH = pathlib.Path(__file__).parent / "image.png"
    LOGO_B64  = base64.b64encode(LOGO_PATH.read_bytes()).decode()
except:
    LOGO_B64  = ""

st.set_page_config(
    page_title="Image Proc",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global State ──
if "app_started" not in st.session_state:
    st.session_state.app_started = False

# ── Phase 1: Cinematic Landing Page ──
if not st.session_state.app_started:
    st.markdown(f"""
<style>
{CSS}
[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="stHeader"] {{ display: none !important; }}
</style>
    """, unsafe_allow_html=True)
    show_landing_page(LOGO_B64)
    st.stop()

# ── Phase 2: Editor Workspace ──
st.markdown(f"""
<style>
{CSS}
[data-testid="stSidebar"] {{ transform: none !important; visibility: visible !important; display: block !important; opacity: 1 !important; pointer-events: auto !important; }}
[data-testid="stHeader"], [data-testid="stFileUploader"], .main-header-wrapper, .main-footer {{ opacity: 1 !important; pointer-events: auto !important; visibility: visible !important; animation: none !important; }}
[data-testid="collapsedControl"] {{ display: block !important; }}
</style>
""", unsafe_allow_html=True)

if "rc" not in st.session_state: st.session_state.rc = 0
if "logs" not in st.session_state: st.session_state.logs = []

# ── Image Upload Logic ──
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Sidebar is always visible but uploader position changes
uploaded_file = st.session_state.uploaded_file

if uploaded_file is None:
    # ── MAIN PAGE UPLOADER (RETAINING ORIGINAL UI) ──
    st.markdown(f"""
<div style="width: 100%; max-width: 1200px; margin: 0 auto; padding: 4rem 2rem; text-align: center;">
    <div class="uplink-placeholder" style="background:var(--bg-card); border: 1px solid var(--glass-border); padding: 80px 40px; border-radius: 40px; backdrop-filter: blur(30px); position: relative; overflow: hidden;">
        <div class="pulse-circle" style="width: 80px; height: 80px; background: rgba(0, 242, 255, 0.1); border-radius: 50%; margin: 0 auto 30px; display: flex; align-items: center; justify-content: center; border: 1px solid var(--accent-cyan);">
            <div style="font-size: 2.5rem; color: var(--accent-cyan); animation: pulse 2s infinite;">✦</div>
        </div>
        <h2 style="font-size: 1.5rem; color: #fff; letter-spacing: 4px; text-transform: uppercase; font-weight: 800; margin-bottom: 20px;">SYSTEM STATUS: READY FOR UPLINK</h2>
        <p style="font-size: 1.1rem; color: var(--text-dim); line-height: 1.6; max-width: 600px; margin: 0 auto 40px;">upload image to process the image</p>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    # The actual uploader
    new_file = st.file_uploader("Drop Image Here", type=["jpg", "jpeg", "png"], key="main_uploader", label_visibility="collapsed")
    if new_file:
        st.session_state.uploaded_file = new_file
        st.rerun()
    
    st.markdown(f"""
<div style="text-align: center; margin-top: 50px;">
    <img src="data:image/png;base64,{LOGO_B64}" style="width: 80px; height: auto; margin: 0 auto; animation: rotate 30s linear infinite; opacity: 0.6;">
</div>
    """, unsafe_allow_html=True)
    st.stop()

# ── IMAGE EDITING PAGE ──
st.sidebar.markdown('<p class="sidebar-header">Controls</p>', unsafe_allow_html=True)
if st.sidebar.button("UPLOAD NEW IMAGE"):
    st.session_state.uploaded_file = None
    st.rerun()

file_bytes = np.asarray(bytearray(uploaded_file.getvalue()), dtype=np.uint8)
original_bgr = cv2.imdecode(file_bytes, 1)

if original_bgr is None:
    st.error("Engine failure: Could not decode visual data stream. Please upload a valid image file.")
    st.stop()

# ── Filter State Initialization ──
if "filters" not in st.session_state:
    st.session_state.filters = {
        "blur": 1, "sharp": 0.0, "bright": 0, "contrast": 1.0, 
        "edges": False, "gray": False
    }

# Reset Button
if st.sidebar.button("RESET ALL FILTERS", width='stretch'):
    st.session_state.filters = {
        "blur": 1, "sharp": 0.0, "bright": 0, "contrast": 1.0, 
        "edges": False, "gray": False
    }
    st.session_state.logs.append("LOG: All filters reset to default")
    st.rerun()

st.sidebar.markdown("---")
blur_ksize = st.sidebar.slider("Gaussian Blur", 1, 31, st.session_state.filters["blur"], 2)
sharpness_alpha = st.sidebar.slider("Sharpness", 0.0, 3.0, st.session_state.filters["sharp"], 0.1)
brightness_beta = st.sidebar.slider("Brightness", -100, 100, st.session_state.filters["bright"])
contrast_alpha = st.sidebar.slider("Contrast", 0.5, 3.0, st.session_state.filters["contrast"], 0.1)
edge_detect = st.sidebar.checkbox("Edge Detection (Canny)", value=st.session_state.filters["edges"])
grayscale = st.sidebar.checkbox("Grayscale", value=st.session_state.filters["gray"])

# Update session state with current values (to persist between other interactions)
st.session_state.filters.update({
    "blur": blur_ksize, "sharp": sharpness_alpha, "bright": brightness_beta,
    "contrast": contrast_alpha, "edges": edge_detect, "gray": grayscale
})

# ── Change Tracking & Logging ──
current_vals = {
    "Blur": blur_ksize, "Sharp": sharpness_alpha, 
    "Bright": brightness_beta, "Contrast": contrast_alpha,
    "Edges": edge_detect, "Gray": grayscale
}

if "prev_vals" not in st.session_state:
    st.session_state.prev_vals = current_vals.copy()

for k, v in current_vals.items():
    if v != st.session_state.prev_vals.get(k):
        st.session_state.logs.append(f"LOG: {k} modified to {v}")
        st.session_state.prev_vals[k] = v

# Sidebar Logs
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="sidebar-header" style="font-size:0.8rem; opacity:0.6;">System Logs</p>', unsafe_allow_html=True)
log_container = st.sidebar.container()
with log_container:
    for log in reversed(st.session_state.logs[-5:]):
        st.markdown(f'<p style="font-size:0.7rem; color:var(--accent-cyan); font-family:monospace; margin:0;">{log}</p>', unsafe_allow_html=True)

# Processing
processed_bgr = original_bgr.copy()
if blur_ksize > 1:
    processed_bgr = cv2.GaussianBlur(processed_bgr, (blur_ksize, blur_ksize), 0)
if sharpness_alpha > 0:
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharp = cv2.filter2D(processed_bgr, -1, kernel)
    processed_bgr = cv2.addWeighted(processed_bgr, 1-sharpness_alpha, sharp, sharpness_alpha, 0)
if brightness_beta != 0 or contrast_alpha != 1.0:
    processed_bgr = cv2.convertScaleAbs(processed_bgr, alpha=contrast_alpha, beta=brightness_beta)
if edge_detect:
    gray = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    processed_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
if grayscale and not edge_detect:
    gray = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2GRAY)
    processed_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# HUD Telemetry
h, w = original_bgr.shape[:2]
active_count = sum([blur_ksize>1, sharpness_alpha>0, brightness_beta!=0, contrast_alpha!=1.0, edge_detect, grayscale])
file_ext = uploaded_file.name.rsplit(".", 1)[-1].upper()

st.markdown(f"""
<div class="hud-container">
    <div class="hud-tile">
        <div class="hud-icon">⛶</div>
        <div class="hud-data"><span class="hud-label">RESOLUTION</span><span class="hud-value">{w}×{h}</span></div>
    </div>
    <div class="hud-tile accent">
        <div class="hud-icon">⚡</div>
        <div class="hud-data"><span class="hud-label">ACTIVE PIPELINE</span><span class="hud-value">{active_count} STAGES</span></div>
    </div>
    <div class="hud-tile">
        <div class="hud-icon">📁</div>
        <div class="hud-data"><span class="hud-label">DATA LOAD</span><span class="hud-value">{uploaded_file.size//1024} KB</span></div>
    </div>
    <div class="hud-tile">
        <div class="hud-icon">◈</div>
        <div class="hud-data"><span class="hud-label">FORMAT</span><span class="hud-value">{file_ext}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Display
def bgr_to_rgb(img): return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown('<div class="image-container"><div class="image-label">Before</div>', unsafe_allow_html=True)
    st.image(bgr_to_rgb(original_bgr), width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="image-container"><div class="image-label">After</div>', unsafe_allow_html=True)
    st.image(bgr_to_rgb(processed_bgr), width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

# Actions
st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    is_success, buffer = cv2.imencode(f".{file_ext.lower()}", processed_bgr)
    if is_success:
        st.download_button(
            label="DOWNLOAD PROCESSED ASSET",
            data=buffer.tobytes(),
            file_name=f"pixelforge_{uploaded_file.name}",
            mime=f"image/{file_ext.lower()}",
            width='stretch'
        )


