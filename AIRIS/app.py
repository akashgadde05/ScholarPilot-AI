"""
AI Research Assistant for Students — Enhanced v2
=================================================
New in v2:
  - Semantic gap analysis (sklearn TF-IDF + LDA + cosine similarity)
  - Citation generator (APA / IEEE / MLA / BibTeX)
  - Journal recommendation engine
  - Pre-submission checklist
  - Paper similarity heatmap
  - Topic clustering view
  - Enhanced dark academic UI

Tech: Streamlit + HuggingFace + sklearn + arXiv API (all free)
"""

import streamlit as st
import sys, os

sys.path.append(os.path.dirname(__file__))

# ── Page config — MUST be first Streamlit call ────────────────────────────────
st.set_page_config(
    page_title="ResearchAI — Student Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import modules ─────────────────────────────────────────────────────────────
from modules.ui_styles import inject_css
from modules.paper_finder import render_paper_finder
from modules.gap_identifier_v2 import render_gap_identifier
from modules.problem_generator import render_problem_generator
from modules.ai_tutor import render_ai_tutor
from modules.draft_generator import render_draft_generator
from modules.publish_guide import render_publish_guide

# ── Inject CSS ─────────────────────────────────────────────────────────────────
inject_css()

# ── Session state defaults ─────────────────────────────────────────────────────
defaults = {
    "papers": [],
    "selected_papers": [],
    "gaps": [],
    "analysis_results": None,
    "problem_statements": [],
    "draft": "",
    "topic": "",
    "chat_history": [],
    "checklist_state": {},
    "_top_keywords": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🔬</span>
        <div>
            <div class="logo-title">ResearchAI</div>
            <div class="logo-sub">Student Research Companion v2</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    pages = {
        "🔍  Paper Finder":        "finder",
        "🕳️  Gap Identifier":      "gap",
        "💡  Problem Generator":   "problem",
        "🤖  AI Tutor":            "tutor",
        "📝  Draft Generator":     "draft",
        "📤  Publish & Citations": "publish",
    }

    # Progress tracker
    st.markdown("### 📊 Your Progress")
    steps = [
        ("Papers Found",       bool(st.session_state.papers)),
        ("Papers Selected",    bool(st.session_state.selected_papers)),
        ("Gaps Identified",    bool(st.session_state.gaps)),
        ("Problems Generated", bool(st.session_state.problem_statements)),
        ("Draft Created",      bool(st.session_state.draft)),
    ]
    for label, done in steps:
        color = "#2dd4bf" if done else "#30363d"
        icon  = "✅" if done else "⬜"
        st.markdown(f"<span style='color:{color};'>{icon} {label}</span>", unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio("Navigate", list(pages.keys()), label_visibility="collapsed")
    active = pages[page]

    # Topic display
    if st.session_state.topic:
        st.markdown("---")
        st.markdown(f"""
        <div style="background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:0.6rem 0.8rem;">
            <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px;">Current Topic</div>
            <div style="font-size:0.82rem; color:var(--teal); font-weight:600; margin-top:0.2rem;">{st.session_state.topic}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#666; text-align:center; line-height:1.6;'>
        🆓 100% Free · No API Keys<br>
        arXiv · HuggingFace · scikit-learn<br>
        <span style='color:#444;'>BE Data Science Final Year Project</span>
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ───────────────────────────────────────────────────────────────
if active == "finder":
    render_paper_finder()
elif active == "gap":
    render_gap_identifier()
elif active == "problem":
    render_problem_generator()
elif active == "tutor":
    render_ai_tutor()
elif active == "draft":
    render_draft_generator()
elif active == "publish":
    render_publish_guide()