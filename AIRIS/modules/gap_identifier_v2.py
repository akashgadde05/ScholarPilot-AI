"""
gap_identifier_v2.py — Enhanced Research Gap Identifier UI
===========================================================
Replaces the basic gap_identifier.py with:
  - sklearn TF-IDF vectorization (bigrams, proper IDF)
  - LDA topic discovery
  - Cosine similarity paper clustering
  - Visual similarity heatmap
  - Richer gap cards with "Why it matters" + "How to address it"
"""

import streamlit as st
import numpy as np


def render_keyword_cloud(keywords: list):
    """Render keywords as a visual word cloud using CSS font-size scaling."""
    if not keywords:
        return
    max_score = keywords[0][1] if keywords else 1

    html = '<div style="display:flex; flex-wrap:wrap; gap:0.5rem; padding:0.5rem 0;">'
    for word, score in keywords[:18]:
        # Scale font size from 0.75rem to 1.3rem based on score
        ratio = score / max_score
        size = 0.75 + ratio * 0.55
        opacity = 0.6 + ratio * 0.4
        html += f"""
        <span style="
            font-size:{size:.2f}rem;
            opacity:{opacity:.2f};
            background: rgba(45,212,191,0.1);
            border: 1px solid rgba(45,212,191,{opacity:.2f});
            border-radius: 20px;
            padding: 0.2rem 0.7rem;
            color: #2dd4bf;
            font-weight: {600 if ratio > 0.6 else 400};
        ">{word}</span>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_similarity_heatmap(sim_matrix: list, papers: list):
    """Render a small cosine similarity heatmap using pure HTML/CSS."""
    n = len(sim_matrix)
    if n < 2:
        return

    st.markdown("**📐 Paper Similarity Matrix** (how similar the selected papers are to each other)")
    st.caption("Darker teal = more similar. Papers in the same cluster share research themes.")

    cell_size = max(24, min(40, 360 // n))  # adaptive cell size
    html = f'<div style="overflow-x:auto;"><table style="border-collapse:collapse; font-size:0.65rem;">'

    # Header row
    html += '<tr><td style="width:{cell_size}px;"></td>'
    for i in range(n):
        html += f'<td style="width:{cell_size}px; text-align:center; color:#8b949e; padding:2px;">P{i+1}</td>'
    html += '</tr>'

    # Data rows
    for i in range(n):
        title_short = papers[i]["title"][:20] + "…" if len(papers[i]["title"]) > 20 else papers[i]["title"]
        html += f'<td style="color:#8b949e; padding:2px 6px; white-space:nowrap;">P{i+1}: {title_short}</td>'
        for j in range(n):
            val = sim_matrix[i][j]
            if i == j:
                bg = "#2dd4bf"
                color = "#000"
            else:
                intensity = int(val * 180)
                bg = f"rgb({13}, {42 + intensity}, {39 + intensity})"
                color = "#e6edf3" if val < 0.5 else "#000"
            html += f'<td style="background:{bg}; color:{color}; text-align:center; width:{cell_size}px; height:{cell_size}px; border:1px solid #30363d;" title="P{i+1} vs P{j+1}: {val:.2f}">{val:.1f}</td>'
        html += '</tr>'

    html += '</table></div>'
    st.markdown(html, unsafe_allow_html=True)


def render_topic_cards(topics: list, papers: list):
    """Render LDA-discovered topics."""
    if not topics:
        return

    st.markdown('<div class="section-header">🧭 Auto-Discovered Research Topics (LDA)</div>', unsafe_allow_html=True)
    st.caption("These topics were discovered automatically from your papers using Latent Dirichlet Allocation — no manual input needed.")

    cols = st.columns(min(len(topics), 4))
    colors = ["#2dd4bf", "#fbbf24", "#fb7185", "#a78bfa"]
    for i, (topic, col) in enumerate(zip(topics, cols)):
        color = colors[i % len(colors)]
        words_html = " · ".join(f'<span style="color:{color};">{w}</span>' for w in topic["words"][:6])
        with col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border);
                        border-top:3px solid {color}; border-radius:8px; padding:0.8rem;">
                <div style="font-size:0.7rem; font-weight:700; color:{color};
                             text-transform:uppercase; letter-spacing:1px; margin-bottom:0.4rem;">
                    Topic {topic['id']}
                </div>
                <div style="font-size:0.75rem; line-height:1.6;">{words_html}</div>
            </div>
            """, unsafe_allow_html=True)


def render_cluster_view(clusters: list, papers: list):
    """Show which papers cluster together."""
    if not clusters or len(clusters) <= 1:
        return

    st.markdown('<div class="section-header">🗂️ Paper Clusters (by research theme)</div>', unsafe_allow_html=True)
    st.caption("Papers grouped by semantic similarity. Clusters with 3+ papers = the field is crowded there.")

    for ci, cluster in enumerate(clusters[:5]):
        if len(cluster) == 0:
            continue
        size_label = "🔴 Crowded" if len(cluster) >= 3 else "🟡 Moderate" if len(cluster) == 2 else "🟢 Unique"
        with st.expander(f"Cluster {ci+1} — {len(cluster)} paper(s) {size_label}", expanded=(ci == 0)):
            for pi in cluster:
                if pi < len(papers):
                    p = papers[pi]
                    st.markdown(f"""
                    <div style="padding:0.4rem 0; border-bottom:1px solid var(--border); font-size:0.82rem;">
                        <strong>{p['title'][:80]}{'…' if len(p['title'])>80 else ''}</strong>
                        <span style="color:var(--muted); margin-left:0.5rem;">({p.get('year','?')})</span>
                    </div>
                    """, unsafe_allow_html=True)
            if len(cluster) >= 3:
                st.info("💡 This cluster is well-researched. Consider a gap in a **different** cluster area.")


def render_gap_cards_enhanced(gaps: list, topic: str):
    """Render enhanced gap cards with why-it-matters and how-to-address."""
    if not gaps:
        st.success("Surprisingly, the selected papers cover most key research dimensions. Try more specific papers.")
        return

    st.markdown(f'<div class="section-header">🕳️ {len(gaps)} Research Gaps Identified</div>', unsafe_allow_html=True)

    # How-to-address suggestions per dimension
    HOW_TO_ADDRESS = {
        "Explainability & XAI": f"Add SHAP value computation after your model predicts. Use `shap.TreeExplainer` (for tree models) or `shap.DeepExplainer` (for neural nets). Display feature importance bar charts. Add LIME as a secondary explanation method. Your paper title: *'An Explainable {topic.title()} Framework Using SHAP and LIME'*",
        "Privacy & Federated Learning": f"Implement federated averaging (FedAvg) using `PySyft` or `Flower` library (both free). Train sub-models on simulated local datasets, aggregate weights centrally without sharing raw data. Add differential privacy with `Opacus` (PyTorch). Paper title: *'Privacy-Preserving {topic.title()} via Federated Learning'*",
        "Real-Time & Edge Deployment": f"Export your PyTorch/TF model to ONNX format (free). Run inference via `onnxruntime` which is 3-5x faster on CPU. Test on Raspberry Pi 4 (₹4000) or use Google Colab for benchmarking. Target: <100ms inference. Paper title: *'Lightweight Real-Time {topic.title()} for Edge Devices'*",
        "Low-Resource & Few-Shot Learning": f"Use `timm` or HuggingFace pretrained models and fine-tune on only 100-500 samples. Apply data augmentation (rotation, flipping, mixup). Try prototypical networks for few-shot learning. Compare: baseline (needs 10K samples) vs your method (needs 500). Paper: *'Few-Shot {topic.title()} with Transfer Learning'*",
        "Fairness, Bias & Ethics": f"Use `Fairlearn` library (Microsoft, free) to measure demographic parity and equalized odds. Run your model on subgroups (gender, age, region) and compare F1 scores. If disparity > 5%, apply reweighting or adversarial debiasing. Paper: *'Bias Auditing in {topic.title()}: A Fairness-Aware Approach'*",
        "Multi-Modal Fusion": f"Combine 2 data sources: e.g., image + text metadata, or sensor + EHR records. Use late fusion (train separate models, average predictions) as baseline. Then implement early fusion (concatenate features). Compare both. This alone is novel in most domains. Paper: *'Multi-Modal {topic.title()} via Feature Fusion'*",
        "Robustness & Generalization": f"Test your model on 3 different datasets (train on A, test on B and C). Report performance drop. Then apply domain adaptation (CORAL or MMD loss) to reduce the drop. Report how much robustness improves. Paper: *'Domain-Robust {topic.title()} via Adversarial Training'*",
        "Clinical / Production Deployment": f"Build a simple FastAPI endpoint that serves your model predictions. Create a Streamlit UI that a non-technical user can use. Do a user study: give 10 students/users the tool and collect feedback (SUS questionnaire). Paper: *'From Prototype to Practice: Deploying {topic.title()} in Real-World Settings'*",
        "Temporal & Sequential Modeling": f"If your data has timestamps, reshape it as sequences. Use LSTM or Transformer (time-series variant like Informer or PatchTST from HuggingFace). Compare: static model vs temporal model on the same data. The temporal model almost always wins. Paper: *'Temporal-Aware {topic.title()} via Sequential Modeling'*",
        "Efficiency & Sustainability": f"After training, apply knowledge distillation: train a small student model to mimic a large teacher. Or use `torch.quantization` to quantize weights from float32 to int8 (4x memory reduction). Measure: parameters, FLOPs, inference time, accuracy. Paper: *'Efficient {topic.title()}: A Model Compression Study'*",
        "Uncertainty Quantification": f"Add Monte Carlo Dropout to your neural network: enable dropout at test time and run inference 20x. The variance across runs = model uncertainty. High uncertainty = model should defer to human. Paper: *'Uncertainty-Aware {topic.title()} via Bayesian Deep Learning'*",
        "Human-in-the-Loop": f"Add active learning: your model picks the most uncertain samples and asks a human to label them. Use `modAL` library (free). After 3 rounds of active labeling, compare accuracy vs random labeling. Paper: *'Interactive {topic.title()} with Active Learning'*",
    }

    for gap in gaps:
        dim = gap["dimension"]
        cov = gap["coverage_pct"]
        sev = gap["severity"]
        why = gap.get("why_matters", "")
        how = HOW_TO_ADDRESS.get(dim, "Design a study that directly addresses this dimension and compare with baselines that ignore it.")
        importance_badge = {"high": "🔥 High Impact", "medium": "⚡ Medium Impact", "low": "📌 Niche Impact"}[gap.get("importance", "medium")]

        st.markdown(f"""
        <div class="gap-card" style="margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.5rem;">
                <div class="gap-card-title">{sev} — {dim}</div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                    <span class="badge">{importance_badge}</span>
                    <span class="badge badge-rose">Only {cov}% coverage</span>
                    <span class="badge" style="background:#1a1a2e; color:#a78bfa; border-color:#6d28d9;">
                        {gap['papers_count']}/{gap['total_papers']} papers address this
                    </span>
                </div>
            </div>
            <div class="gap-card-body" style="margin-bottom:0.6rem;">
                <strong style="color:#e6edf3;">📌 Why this matters:</strong> {why}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"💡 How to address '{dim}' in your project", expanded=False):
            st.markdown(how)

    # Summary insight
    critical = sum(1 for g in gaps if "Critical" in g["severity"])
    major    = sum(1 for g in gaps if "Major"    in g["severity"])
    st.markdown(f"""
    <div style="background:#0d2219; border:1px solid #2dd4bf; border-radius:8px; padding:1rem; margin-top:1rem;">
        <strong style="color:#2dd4bf;">🎯 Analysis Summary</strong><br>
        <span style="font-size:0.85rem; color:#c9d1d9;">
        Found <strong>{critical} critical</strong> and <strong>{major} major</strong> gaps across {len(gaps)} dimensions.
        The highest-impact gap is <strong>{gaps[0]['dimension']}</strong>.
        Addressing even <strong>one</strong> of these gaps in your project is sufficient for a strong BE dissertation
        and a publishable conference paper.
        </span>
    </div>
    """, unsafe_allow_html=True)


def render_gap_identifier():
    """Main UI for the enhanced Gap Identifier page."""

    st.markdown("""
    <div class="page-header">
        <h1>🕳️ Research Gap Identifier</h1>
        <p>Semantic TF-IDF analysis + LDA topic discovery + cosine similarity clustering — all free, all on CPU.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("papers"):
        st.warning("⚠️ Please search for papers first in the **Paper Finder** tab.")
        return

    selected_ids = st.session_state.get("selected_papers", [])
    all_papers   = st.session_state.papers
    selected     = [p for p in all_papers if p["id"] in selected_ids]

    if len(selected) < 2:
        st.warning("⚠️ Please select at least 2 papers in Paper Finder to enable gap analysis.")
        return

    st.markdown(f"**{len(selected)} papers selected** for analysis.")

    with st.expander(f"📄 Selected Papers", expanded=False):
        for p in selected:
            st.markdown(f"- **{p['title']}** ({p.get('year','?')}) — {p.get('authors','')[:50]}")

    # ── Analysis controls ──────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col2:
        n_topics = st.slider("LDA Topics", 2, 6, min(4, max(2, len(selected) // 2)))
    with col1:
        analyze_clicked = st.button("🔬 Run Full Semantic Analysis", use_container_width=True)

    # ── Run or load cached analysis ────────────────────────────────────────────
    if analyze_clicked or st.session_state.get("analysis_results"):
        if analyze_clicked:
            with st.spinner("Running semantic analysis (TF-IDF → LDA → Cosine Similarity → Gap Detection)…"):
                from modules.semantic_analyzer import run_full_analysis
                results = run_full_analysis(selected)
            if "error" in results:
                st.error(results["error"])
                return
            st.session_state.analysis_results = results
            # Also store gaps for downstream use
            st.session_state.gaps = [
                {
                    "area":         g["dimension"],
                    "coverage_pct": g["coverage_pct"],
                    "severity":     g["severity"],
                    "importance":   g.get("importance","medium"),
                    "why_matters":  g.get("why_matters",""),
                    "papers_count": g.get("papers_count", 0),
                    "total_papers": g.get("total_papers", len(selected)),
                }
                for g in results["gaps"]
            ]

        results = st.session_state.analysis_results
        topic   = st.session_state.get("topic", "this domain")

        # ── Metrics row ────────────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Papers Analyzed", results["n_papers"])
        with m2:
            st.metric("Gaps Found", len(results["gaps"]))
        with m3:
            avg_sim = results.get("avg_similarity", 0)
            st.metric("Avg Paper Similarity", f"{avg_sim:.2f}", help="0=totally different, 1=identical. Low = diverse corpus.")
        with m4:
            st.metric("Topics Discovered", len(results.get("topics", [])))

        st.markdown("---")

        # ── Tab layout for different views ─────────────────────────────────────
        tab1, tab2, tab3, tab4 = st.tabs(["🕳️ Research Gaps", "☁️ Keyword Analysis", "🧭 Topics & Clusters", "📐 Similarity Map"])

        with tab1:
            render_gap_cards_enhanced(results["gaps"], topic)

        with tab2:
            st.markdown('<div class="section-header">☁️ Dominant Keywords (TF-IDF Weighted)</div>', unsafe_allow_html=True)
            st.caption("These are the most distinctive terms across your selected papers — what the field is currently focused on.")
            render_keyword_cloud(results["keywords"])

            # Bar chart using HTML (no matplotlib dependency)
            st.markdown("**Top 10 Keywords by TF-IDF Score:**")
            top10 = results["keywords"][:10]
            if top10:
                max_s = top10[0][1]
                for word, score in top10:
                    pct = int((score / max_s) * 100)
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.3rem;">
                        <div style="width:120px; font-size:0.8rem; color:#e6edf3; text-align:right;">{word}</div>
                        <div style="flex:1; background:var(--border); border-radius:4px; height:18px;">
                            <div style="width:{pct}%; background:linear-gradient(90deg,#0d9488,#2dd4bf);
                                        height:100%; border-radius:4px; display:flex; align-items:center;">
                                <span style="font-size:0.65rem; color:#000; padding-left:4px;">{score:.3f}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab3:
            render_topic_cards(results.get("topics", []), selected)
            st.markdown("")
            render_cluster_view(results.get("clusters", []), selected)

        with tab4:
            sim = results.get("similarity_matrix", [])
            if sim:
                render_similarity_heatmap(sim, selected)
            else:
                st.info("Similarity matrix unavailable.")

        # ── CTA ────────────────────────────────────────────────────────────────
        if results["gaps"]:
            st.success(f"✅ Analysis complete! Navigate to **Problem Generator** to turn these {len(results['gaps'])} gaps into problem statements.")