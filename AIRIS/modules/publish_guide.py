"""
publish_guide.py — Where to Publish & Citation Tools
======================================================
Helps students find the right journal/conference for their paper.
Includes:
  - Venue recommendation engine (filtered by experience level)
  - Citation generator (APA, IEEE, MLA, BibTeX)
  - Publishing checklist (what to do before submission)
"""

import streamlit as st
from modules.citation_utils import recommend_venues, render_citation_panel


CHECKLIST_ITEMS = [
    ("📝 Paper Writing", [
        ("Title is specific and includes your method + domain", False),
        ("Abstract is 150–250 words covering: problem, method, results, conclusion", False),
        ("Introduction explains the gap clearly", False),
        ("Literature review cites ≥15 related papers", False),
        ("Methodology is reproducible (someone can replicate it)", False),
        ("Results include quantitative comparison with baseline(s)", False),
        ("Conclusion summarizes contributions + future work", False),
    ]),
    ("🔬 Technical Quality", [
        ("Code is available on GitHub (or will be)", False),
        ("Dataset is publicly available or clearly described", False),
        ("Used cross-validation (not just single train/test split)", False),
        ("Reported standard deviation / confidence intervals", False),
        ("Compared against at least 2 baseline methods", False),
        ("Ablation study conducted (tested removing each component)", False),
    ]),
    ("📋 Submission Readiness", [
        ("Paper formatted in required template (IEEE/Springer/etc.)", False),
        ("Word count within venue limits (usually 6-8 pages)", False),
        ("All figures have captions and are referenced in text", False),
        ("All tables labeled and referenced", False),
        ("References formatted correctly in required style", False),
        ("Plagiarism check done (<15% similarity, use iThenticate or Turnitin)", False),
        ("Guide/advisor has reviewed and approved", False),
    ]),
]


def render_publish_guide():
    """Main UI for the Publish & Citations page."""

    st.markdown("""
    <div class="page-header">
        <h1>📤 Where to Publish</h1>
        <p>Journal recommendations, citation generator, and a submission checklist — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏛️ Venue Finder", "📚 Citation Generator", "✅ Submission Checklist"])

    # ── Tab 1: Venue Finder ────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">🏛️ Find the Right Journal or Conference</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            experience = st.selectbox(
                "Your experience level",
                ["First paper (student)", "Intermediate", "Advanced / with guide"],
                help="This filters venues to only show appropriate ones for you."
            )
        with col2:
            topic = st.session_state.get("topic", "")
            topic_input = st.text_input("Your research topic (optional filter)", value=topic, placeholder="e.g. AI in agriculture")

        venues = recommend_venues(topic_input, experience)

        st.markdown(f"**{len(venues)} venues recommended for your level:**")

        # Group by type
        types = ["Preprint", "Journal", "Conference", "Repository"]
        for vtype in types:
            group = [v for v in venues if v["type"] == vtype]
            if not group:
                continue

            st.markdown(f"#### {'📄' if vtype=='Preprint' else '📗' if vtype=='Journal' else '🎤' if vtype=='Conference' else '🗂️'} {vtype}s")
            for v in group:
                cost_color = "#2dd4bf" if "Free" in v["cost"] else "#fbbf24"
                st.markdown(f"""
                <div class="card" style="border-left:3px solid {cost_color};">
                    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:0.3rem;">
                        <div class="card-title"><a href="{v['url']}" target="_blank" style="color:#e6edf3; text-decoration:none;">🔗 {v['name']}</a></div>
                        <span class="badge" style="background:#0d2219; color:{cost_color}; border-color:{cost_color};">💰 {v['cost']}</span>
                    </div>
                    <div class="card-meta">
                        <span>📅 Deadline: {v['deadline']}</span>
                        <span>📊 {v['impact']}</span>
                    </div>
                    <div class="card-summary">💡 <em>{v['tip']}</em></div>
                </div>
                """, unsafe_allow_html=True)

        # Publication pathway guide
        st.markdown("---")
        st.markdown("### 🗺️ Recommended Publication Pathway for BE Students")
        st.markdown("""
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:1.2rem;">
            <div style="display:flex; flex-direction:column; gap:0.6rem;">
                <div style="display:flex; gap:1rem; align-items:flex-start;">
                    <div style="background:#2dd4bf; color:#000; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">1</div>
                    <div><strong style="color:#2dd4bf;">Upload to arXiv</strong> (free, instant)<br><span style="color:#8b949e; font-size:0.82rem;">Establishes your work's date. Takes 2-3 days to appear. No peer review needed.</span></div>
                </div>
                <div style="display:flex; gap:1rem; align-items:flex-start;">
                    <div style="background:#fbbf24; color:#000; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">2</div>
                    <div><strong style="color:#fbbf24;">Submit to IRJET/IJERT</strong> (free, fast)<br><span style="color:#8b949e; font-size:0.82rem;">3-4 week review. Certificate + publication. Accepted by most Indian universities for BE projects.</span></div>
                </div>
                <div style="display:flex; gap:1rem; align-items:flex-start;">
                    <div style="background:#fb7185; color:#000; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">3</div>
                    <div><strong style="color:#fb7185;">Submit to Springer LNCS Conference</strong> (Scopus)<br><span style="color:#8b949e; font-size:0.82rem;">With your guide's support. More competitive but gives Scopus indexing. Excellent for placement.</span></div>
                </div>
                <div style="display:flex; gap:1rem; align-items:flex-start;">
                    <div style="background:#a78bfa; color:#000; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">4</div>
                    <div><strong style="color:#a78bfa;">Extended version → IEEE Access or JAIR</strong><br><span style="color:#8b949e; font-size:0.82rem;">After your project is complete. Add more experiments. Target IF > 3.5 journals.</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 2: Citation Generator ──────────────────────────────────────────────
    with tab2:
        papers = st.session_state.get("papers", [])
        selected_ids = st.session_state.get("selected_papers", [])
        selected = [p for p in papers if p["id"] in selected_ids]

        if selected:
            render_citation_panel(selected)
        else:
            st.info("📄 Select papers in the **Paper Finder** tab first, then come back here to generate citations.")

            # Show sample citation preview
            st.markdown("**Preview (sample APA citation):**")
            sample = {
                "authors": "LeCun Yann, Bengio Yoshua, Hinton Geoffrey",
                "year": "2015",
                "title": "Deep learning",
                "link": "https://arxiv.org/abs/1206.5538"
            }
            from modules.citation_utils import format_apa, format_ieee, generate_bibtex
            st.code(format_apa(sample), language=None)
            st.code(format_ieee(sample, 1), language=None)
            st.code(generate_bibtex(sample), language="bibtex")

    # ── Tab 3: Submission Checklist ────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">✅ Pre-Submission Checklist</div>', unsafe_allow_html=True)
        st.caption("Check off each item before submitting your paper. All items should be ✅ before submission.")

        total_items = sum(len(items) for _, items in CHECKLIST_ITEMS)
        # Track checked state
        if "checklist_state" not in st.session_state:
            st.session_state.checklist_state = {}

        checked_count = sum(1 for v in st.session_state.checklist_state.values() if v)

        # Progress bar
        progress = checked_count / total_items if total_items > 0 else 0
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                <span style="font-size:0.85rem; color:#e6edf3;">Submission Readiness</span>
                <span style="font-size:0.85rem; color:#2dd4bf;">{checked_count}/{total_items} complete</span>
            </div>
            <div style="background:var(--border); border-radius:4px; height:8px;">
                <div style="width:{int(progress*100)}%; background:linear-gradient(90deg,#0d9488,#2dd4bf);
                            height:100%; border-radius:4px; transition:width 0.3s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for section_name, items in CHECKLIST_ITEMS:
            st.markdown(f"**{section_name}**")
            for item_text, _ in items:
                key = f"check_{hash(item_text)}"
                current = st.session_state.checklist_state.get(key, False)
                checked = st.checkbox(item_text, value=current, key=f"cb_{key}")
                st.session_state.checklist_state[key] = checked
            st.markdown("")

        if progress == 1.0:
            st.balloons()
            st.success("🎉 Your paper is submission-ready! Go publish it!")
        elif progress >= 0.7:
            st.info(f"📌 Almost there! {total_items - checked_count} items remaining.")