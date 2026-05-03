import streamlit as st
import base64
import pathlib

def get_base64(file_path):
    try:
        path = pathlib.Path(file_path)
        if not path.exists():
            return ""
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return ""

def show_landing_page(logo_b64):
    # Use the provided logo for showcase if others aren't found
    # In a real app, these would be specific showcase assets
    showcase_img = logo_b64 

    # ── Corner Logo ──
    st.markdown(f"""
        <div class="top-right-logo">
            <img src="data:image/png;base64,{logo_b64}" class="corner-logo-img">
        </div>
    """, unsafe_allow_html=True)

    # ── Hero Section ──
    st.markdown(f"""
        <div class="hero-section">
            <div class="hero-content">
                <div class="badge">IMAGE PROCESSING USING OPENCV AND STREAMLIT</div>
                <h1 class="hero-title">REDEFINING <span class="accent-text">VISION</span></h1>
                <p class="hero-subtitle">This project demonstrates advanced image processing capabilities developed using Python and OpenCV. Explore real-time filters, edge detection, and sophisticated visual enhancements.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Use columns to center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ENTER WORKSPACE", key="start_editing_btn", width='stretch'):
            st.session_state.app_started = True
            st.rerun()

    # ── Feature Grid ──
    st.markdown("""
        <div class="features-container">
            <div class="section-header">
                <span class="section-tag">CAPABILITIES</span>
                <h2 class="section-title">ENGINE CORE</h2>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">✦</div>
                    <h3>NEURAL CLARITY</h3>
                    <p>Advanced sharpening algorithms that restore high-frequency details without introducing artifacts.</p>
                </div>
                <div class="feature-card accent">
                    <div class="feature-icon">⚡</div>
                    <h3>REAL-TIME ENGINE</h3>
                    <p>Zero-latency processing pipeline optimized for high-resolution assets and complex filters.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⬡</div>
                    <h3>BOUNDARY ANALYSIS</h3>
                    <p>Precision Canny edge detection and structural extraction for mathematical image decomposition.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Showcase Section ──
    st.markdown(f"""
        <div class="showcase-section">
            <div class="showcase-text">
                <span class="section-tag">PRECISION</span>
                <h2 class="section-title">PROJECT ARCHITECTURE</h2>
                <p>This application utilizes the Python OpenCV library to implement complex computer vision algorithms in a user-friendly Streamlit interface. From contrast optimization to structural edge detection, each component is designed to show the potential of programmatic image manipulation.</p>
            </div>
            <div class="showcase-visual">
                <div class="visual-frame">
                    <img src="data:image/png;base64,{showcase_img}" class="showcase-img">
                    <div class="scan-line"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer-simple">
            <p>© 2026 PIXELFORGE CORE // ALL SYSTEMS OPERATIONAL</p>
        </div>
    """, unsafe_allow_html=True)
