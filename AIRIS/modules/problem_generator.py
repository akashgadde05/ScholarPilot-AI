"""
problem_generator.py — Problem Statement Generator
====================================================
Converts research gaps into concrete, student-friendly problem statements.

Strategy:
- Takes each gap identified from the papers
- Applies a structured template:
    "Despite X existing, there is a lack of Y, which causes Z.
     This project proposes to A using B to achieve C."
- Templates are parameterized by: topic, gap area, suggested method

No AI model needed here — pure rule-based generation that produces
professional, publishable-quality problem statements.
"""

import streamlit as st
import re


# ── Problem statement templates ────────────────────────────────────────────────
# Each template has placeholders: {topic}, {gap_area}, {method}
PROBLEM_TEMPLATES = [
    # Template 1: The Classic Gap Statement
    (
        "Classic Gap Statement",
        """Despite significant progress in {topic}, existing research lacks sufficient focus on {gap_area}. 
Current approaches are primarily designed for controlled, laboratory conditions and do not adequately address 
real-world constraints. This gap limits the practical applicability and adoption of AI systems in this domain. 
This project proposes to develop a {method} that explicitly addresses {gap_area}, making the solution more 
reliable, transparent, and deployable in real-world environments."""
    ),

    # Template 2: The Data-Driven Problem
    (
        "Data-Driven Problem",
        """While numerous machine learning models have been applied to {topic}, there remains a critical shortage 
of approaches that effectively handle {gap_area}. Existing datasets and methodologies assume ideal conditions 
that rarely exist in practice. As a result, model performance significantly degrades when deployed outside 
research settings. This study proposes to investigate and implement a {method} specifically designed to tackle 
{gap_area}, with validation on real-world, noisy, and heterogeneous data sources."""
    ),

    # Template 3: The User-Centric Problem
    (
        "Human-Centered Approach",
        """The growing adoption of AI in {topic} has created an urgent need to address {gap_area}, yet this 
remains largely unexplored in academic literature. End-users—including non-technical stakeholders such as 
doctors, farmers, or educators—require systems that are not only accurate but also trustworthy, efficient, 
and understandable. This project proposes a {method} centered on {gap_area} to bridge the gap between 
state-of-the-art research performance and practical, human-centered deployment."""
    ),

    # Template 4: The Comparative Problem
    (
        "Comparative Benchmark Study",
        """Existing literature on {topic} presents conflicting evidence regarding the best approaches for 
{gap_area}, with most studies being narrow in scope and lacking comprehensive comparison. There is no 
established benchmark that evaluates models specifically under {gap_area} constraints. This project addresses 
this gap by designing, implementing, and benchmarking a {method}, establishing a reproducible evaluation 
framework that future researchers can build upon."""
    ),

    # Template 5: The Scalability Problem
    (
        "Scalability & Efficiency",
        """Current AI solutions for {topic} achieve high accuracy but at a significant computational cost, 
making {gap_area} a persistent unresolved challenge. Deploying such systems in resource-constrained 
environments—including mobile devices, edge nodes, or rural infrastructure—remains infeasible. This research 
proposes a lightweight {method} that maintains competitive performance while specifically addressing {gap_area}, 
enabling wider adoption in low-resource and real-world settings."""
    ),
]


# ── Method suggestions per gap area ───────────────────────────────────────────
GAP_TO_METHOD = {
    "explainability / XAI":              "SHAP-integrated deep learning model with explainability dashboards",
    "real-time processing":              "optimized ONNX/TensorFlow Lite pipeline with edge deployment",
    "privacy / federated learning":      "federated learning framework with differential privacy guarantees",
    "small datasets / low-resource":     "transfer learning + data augmentation framework for limited data",
    "multi-modal data":                  "multi-modal fusion model combining text, image, and tabular data",
    "generalization / robustness":       "domain-adaptive model with adversarial training for robustness",
    "clinical / real-world deployment":  "end-to-end deployable system with a live API and UI dashboard",
    "fairness / bias":                   "bias-aware training pipeline with fairness evaluation metrics",
    "energy efficiency":                 "model compression pipeline using pruning and quantization techniques",
    "longitudinal / temporal":           "temporal attention-based model for sequential/time-series data",
}

DEFAULT_METHOD = "hybrid deep learning framework combining state-of-the-art techniques"


def generate_problem_statements(topic: str, gaps: list[dict]) -> list[dict]:
    """
    Generate problem statements by combining gaps with templates.
    Returns a list of {title, text, gap_area, method} dicts.
    """
    if not gaps:
        return []

    problem_statements = []
    # Use top 5 gaps (or all if fewer)
    top_gaps = gaps[:5]

    for i, (gap, (template_name, template_text)) in enumerate(
        zip(top_gaps, PROBLEM_TEMPLATES[:len(top_gaps)])
    ):
        gap_area = gap["area"]
        method   = GAP_TO_METHOD.get(gap_area, DEFAULT_METHOD)

        # Fill in the template
        text = template_text.format(
            topic    = topic or "this domain",
            gap_area = gap_area,
            method   = method,
        )

        problem_statements.append({
            "number":    i + 1,
            "title":     template_name,
            "text":      text.strip(),
            "gap_area":  gap_area,
            "method":    method,
            "severity":  gap.get("severity", ""),
        })

    return problem_statements


def render_problem_generator():
    """Main UI renderer for the Problem Statement Generator page."""

    st.markdown("""
    <div class="page-header">
        <h1>💡 Problem Statement Generator</h1>
        <p>Converts your identified research gaps into concrete, publishable problem statements.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Guards ─────────────────────────────────────────────────────────────────
    if not st.session_state.get("gaps"):
        st.warning("⚠️ Please complete the **Gap Identifier** step first.")
        return

    topic = st.session_state.get("topic", "")
    gaps  = st.session_state.gaps

    # Topic override input
    col1, col2 = st.columns([3, 1])
    with col1:
        topic_input = st.text_input(
            "Research topic (confirm or refine)",
            value=topic,
            placeholder="e.g. Machine Learning for Crop Disease Detection",
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_clicked = st.button("✨ Generate Statements", use_container_width=True)

    if generate_clicked or st.session_state.get("problem_statements"):
        if generate_clicked:
            with st.spinner("Generating problem statements…"):
                stmts = generate_problem_statements(topic_input or topic, gaps)
                st.session_state.problem_statements = stmts

        stmts = st.session_state.problem_statements

        if not stmts:
            st.error("Could not generate statements. Please ensure gaps were identified first.")
            return

        st.markdown(f"""
        <div class="section-header">📋 {len(stmts)} Problem Statements Generated</div>
        """, unsafe_allow_html=True)

        st.info("💡 **Tip:** Each statement follows the research writing format: Background → Gap → Impact → Proposed Solution. You can pick the one that best fits your project and refine it.")

        for stmt in stmts:
            st.markdown(f"""
            <div class="ps-card">
                <div class="ps-number">Problem Statement #{stmt['number']} · {stmt['title']}</div>
                <div class="ps-text">{stmt['text']}</div>
                <div style="margin-top:0.6rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
                    <span class="badge">Gap: {stmt['gap_area']}</span>
                    <span class="badge badge-amber">Method: {stmt['method'][:40]}…</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Export section ─────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("**📋 Export All Problem Statements**")
        all_text = "\n\n".join([
            f"PROBLEM STATEMENT #{s['number']}: {s['title']}\n{'='*60}\n{s['text']}"
            for s in stmts
        ])
        st.download_button(
            "⬇️ Download as .txt",
            data=all_text,
            file_name="problem_statements.txt",
            mime="text/plain",
        )

        st.success("✅ Problem statements ready. Navigate to **AI Tutor** to explore papers deeper, or jump to **Draft Generator**.")