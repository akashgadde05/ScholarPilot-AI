"""
ui_styles.py — Global CSS for AI Research Assistant
Aesthetic: Academic-dark with teal accents. Clean, focused, scholarly.
"""

import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

    /* ── Root variables ── */
    :root {
        --bg:       #0d1117;
        --surface:  #161b22;
        --surface2: #1c2333;
        --border:   #30363d;
        --teal:     #2dd4bf;
        --teal-dim: #0d9488;
        --amber:    #fbbf24;
        --rose:     #fb7185;
        --text:     #e6edf3;
        --muted:    #8b949e;
        --radius:   10px;
    }

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 2rem 4rem; max-width: 1100px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    /* ── Sidebar logo ── */
    .sidebar-logo {
        display: flex; align-items: center; gap: 0.75rem;
        padding: 0.5rem 0 0.25rem;
    }
    .logo-icon { font-size: 2rem; }
    .logo-title { font-size: 1.1rem; font-weight: 700; color: var(--teal) !important; }
    .logo-sub   { font-size: 0.7rem; color: var(--muted) !important; }

    /* ── Page header ── */
    .page-header {
        background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
        border: 1px solid var(--border);
        border-left: 4px solid var(--teal);
        border-radius: var(--radius);
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .page-header h1 { font-size: 1.6rem; font-weight: 700; margin: 0; }
    .page-header p  { color: var(--muted); margin: 0.3rem 0 0; font-size: 0.9rem; }

    /* ── Cards ── */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.9rem;
        transition: border-color 0.2s, transform 0.2s;
    }
    .card:hover { border-color: var(--teal-dim); transform: translateY(-1px); }
    .card-selected { border-color: var(--teal) !important; background: #0d2a27 !important; }

    .card-title { font-size: 0.95rem; font-weight: 600; color: var(--text); margin-bottom: 0.35rem; }
    .card-meta  { font-size: 0.75rem; color: var(--muted); margin-bottom: 0.5rem; display:flex; gap:1rem; }
    .card-summary { font-size: 0.82rem; color: #c9d1d9; line-height: 1.55; }

    .badge {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #0d2a27;
        color: var(--teal);
        border: 1px solid var(--teal-dim);
    }
    .badge-amber { background: #2a1f0d; color: var(--amber); border-color: #b45309; }
    .badge-rose  { background: #2a0d15; color: var(--rose);  border-color: #9f1239; }

    /* ── Gap cards ── */
    .gap-card {
        background: linear-gradient(135deg, #0d1f1d, #0d1722);
        border: 1px solid var(--teal-dim);
        border-radius: var(--radius);
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }
    .gap-card-title { font-size: 0.9rem; font-weight: 600; color: var(--teal); margin-bottom:0.3rem; }
    .gap-card-body  { font-size: 0.82rem; color: #c9d1d9; line-height:1.5; }

    /* ── Problem statement cards ── */
    .ps-card {
        background: var(--surface2);
        border: 1px solid var(--border);
        border-left: 4px solid var(--amber);
        border-radius: var(--radius);
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
    }
    .ps-number { font-size: 0.7rem; color: var(--amber); font-weight:700; margin-bottom:0.3rem; text-transform:uppercase; letter-spacing:1px; }
    .ps-text   { font-size: 0.88rem; color: var(--text); line-height:1.6; font-family:'Lora',serif; }

    /* ── Chat ── */
    .chat-user {
        background: var(--surface2);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display:flex; gap:0.7rem; align-items:flex-start;
    }
    .chat-assistant {
        background: #0d2219;
        border: 1px solid var(--teal-dim);
        border-radius: var(--radius);
        padding: 0.75rem 1rem;
        margin-bottom: 0.9rem;
        display:flex; gap:0.7rem; align-items:flex-start;
    }
    .chat-avatar { font-size: 1.2rem; flex-shrink:0; }
    .chat-text   { font-size: 0.85rem; line-height:1.6; }

    /* ── Draft output ── */
    .draft-section {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .draft-section-title {
        font-size: 0.75rem; font-weight:700; text-transform:uppercase;
        letter-spacing:1.5px; color: var(--teal); margin-bottom:0.6rem;
    }
    .draft-section-body {
        font-size: 0.88rem; line-height:1.75; color: #e0e6ee;
        font-family: 'Lora', serif;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: var(--radius) !important;
        font-family: 'Sora', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.15) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--teal-dim), #0a7a70) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius) !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.4rem !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: var(--teal) !important; }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; }

    /* ── Multiselect ── */
    .stMultiSelect [data-baseweb="tag"] {
        background: var(--teal-dim) !important;
        color: white !important;
    }

    /* ── Info/Warning boxes ── */
    .stAlert { border-radius: var(--radius) !important; }

    /* ── Code ── */
    code { font-family: 'JetBrains Mono', monospace !important; }

    /* ── Step indicator ── */
    .step-indicator {
        display: flex; align-items: center; gap: 0.5rem;
        font-size: 0.78rem; color: var(--muted);
        margin-bottom: 1.2rem;
    }
    .step-dot { width:8px; height:8px; border-radius:50%; background: var(--teal); }

    /* ── Section header ── */
    .section-header {
        font-size: 1rem; font-weight: 600;
        margin: 1.2rem 0 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--border);
        color: var(--text);
    }
    </style>
    """, unsafe_allow_html=True)