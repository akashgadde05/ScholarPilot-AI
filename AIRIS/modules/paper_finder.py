"""
paper_finder.py — Research Paper Finder using arXiv API
=========================================================
Fetches papers from arXiv (completely free, no API key needed).
arXiv API docs: https://arxiv.org/help/api/

How it works:
1. User types a topic (e.g. "AI in healthcare")
2. We query the arXiv API with that topic
3. Parse the XML response
4. Display papers as interactive cards
5. User selects papers to analyze further
"""

import streamlit as st
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
import time


# ── arXiv namespace (required to parse the XML correctly) ──────────────────────
ARXIV_NS = {
    "atom":    "http://www.w3.org/2005/Atom",
    "arxiv":   "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}


def fetch_arxiv_papers(query: str, max_results: int = 20) -> list[dict]:
    """
    Query the arXiv API and return a list of paper dicts.

    arXiv API endpoint: http://export.arxiv.org/api/query
    Parameters:
      - search_query : keywords (e.g. "all:machine+learning+healthcare")
      - start        : pagination offset
      - max_results  : how many to return (we use 20)
      - sortBy       : relevance | lastUpdatedDate | submittedDate
    """
    # Build the query URL
    # "all:" searches title + abstract + authors + categories
    encoded_query = urllib.parse.quote(query)
    url = (
        f"http://export.arxiv.org/api/query"
        f"?search_query=all:{encoded_query}"
        f"&start=0"
        f"&max_results={max_results}"
        f"&sortBy=relevance"
        f"&sortOrder=descending"
    )

    try:
        # Make the HTTP request (arXiv asks for a 3-second delay between calls)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ResearchAssistantBot/1.0 (educational use)"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read().decode("utf-8")
    except Exception as e:
        return []  # Return empty list on network error

    # Parse the XML response
    papers = []
    try:
        root = ET.fromstring(xml_data)
        entries = root.findall("atom:entry", ARXIV_NS)

        for entry in entries:
            # Title — strip newlines and extra spaces
            title_el = entry.find("atom:title", ARXIV_NS)
            title = " ".join(title_el.text.split()) if title_el is not None else "Unknown Title"

            # Abstract / summary
            summary_el = entry.find("atom:summary", ARXIV_NS)
            summary = summary_el.text.strip() if summary_el is not None else ""
            # Trim to ~300 characters for display
            short_summary = summary[:350] + "..." if len(summary) > 350 else summary

            # Published date → extract year
            published_el = entry.find("atom:published", ARXIV_NS)
            year = "Unknown"
            if published_el is not None:
                try:
                    year = published_el.text[:4]  # "2024-01-15T..." → "2024"
                except:
                    pass

            # arXiv ID and link
            id_el = entry.find("atom:id", ARXIV_NS)
            arxiv_id = id_el.text.strip() if id_el is not None else ""
            link = arxiv_id  # The ID is the full URL e.g. http://arxiv.org/abs/2401.12345

            # Authors (first 3)
            authors = []
            for author_el in entry.findall("atom:author", ARXIV_NS):
                name_el = author_el.find("atom:name", ARXIV_NS)
                if name_el is not None:
                    authors.append(name_el.text.strip())
            author_str = ", ".join(authors[:3])
            if len(authors) > 3:
                author_str += f" +{len(authors)-3} more"

            # Category (research field)
            category_el = entry.find("atom:category", ARXIV_NS)
            category = ""
            if category_el is not None:
                category = category_el.attrib.get("term", "")

            papers.append({
                "title":    title,
                "summary":  summary,         # Full abstract (for AI analysis)
                "preview":  short_summary,   # Short version (for display)
                "year":     year,
                "authors":  author_str,
                "link":     link,
                "category": category,
                "id":       arxiv_id,
            })

    except ET.ParseError:
        return []

    return papers


def render_paper_finder():
    """Main UI renderer for the Paper Finder page."""

    # ── Page header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
        <h1>🔍 Research Paper Finder</h1>
        <p>Search across arXiv's 2M+ open-access papers — no login, no cost, no limits.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Search input ───────────────────────────────────────────────────────────
    col1, col2 = st.columns([4, 1])
    with col1:
        topic = st.text_input(
            "Research topic",
            value=st.session_state.get("topic", ""),
            placeholder='e.g. "federated learning for healthcare privacy"',
            label_visibility="collapsed",
        )
    with col2:
        num_papers = st.selectbox("Results", [10, 15, 20], index=1, label_visibility="collapsed")

    search_clicked = st.button("🔍 Search Papers", use_container_width=True)

    # ── Search logic ───────────────────────────────────────────────────────────
    if search_clicked and topic.strip():
        st.session_state.topic = topic.strip()
        st.session_state.selected_papers = []  # Reset selections

        with st.spinner(f"Searching arXiv for '{topic}'…"):
            papers = fetch_arxiv_papers(topic, max_results=num_papers)

        if papers:
            st.session_state.papers = papers
            st.success(f"✅ Found {len(papers)} papers. Select the ones most relevant to your research.")
        else:
            st.error("No papers found or network error. Try a different query.")
            return

    # ── Display papers ─────────────────────────────────────────────────────────
    if st.session_state.papers:
        papers = st.session_state.papers

        st.markdown(f"""
        <div class="section-header">
            📚 {len(papers)} Papers Found — Select the most relevant ones
        </div>
        """, unsafe_allow_html=True)

        # Quick-select buttons
        c1, c2, c3 = st.columns([1, 1, 3])
        with c1:
            if st.button("Select All"):
                st.session_state.selected_papers = [p["id"] for p in papers]
                st.rerun()
        with c2:
            if st.button("Clear All"):
                st.session_state.selected_papers = []
                st.rerun()

        st.markdown("")  # spacer

        # Render each paper as a card with a checkbox
        for i, paper in enumerate(papers):
            paper_id = paper["id"]
            is_selected = paper_id in st.session_state.selected_papers

            # Card with checkbox
            col_check, col_card = st.columns([0.05, 0.95])
            with col_check:
                checked = st.checkbox("", value=is_selected, key=f"paper_cb_{i}")
            with col_card:
                card_class = "card card-selected" if is_selected else "card"
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="card-title">{paper['title']}</div>
                    <div class="card-meta">
                        <span>👤 {paper['authors'] or 'Unknown'}</span>
                        <span>📅 {paper['year']}</span>
                        <span class="badge">{paper['category'] or 'cs.AI'}</span>
                        <a href="{paper['link']}" target="_blank" style="color:#2dd4bf;font-size:0.7rem;">🔗 arXiv</a>
                    </div>
                    <div class="card-summary">{paper['preview']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Update selected list based on checkbox
            if checked and paper_id not in st.session_state.selected_papers:
                st.session_state.selected_papers.append(paper_id)
            elif not checked and paper_id in st.session_state.selected_papers:
                st.session_state.selected_papers.remove(paper_id)

        # ── Selection summary ──────────────────────────────────────────────────
        n_selected = len(st.session_state.selected_papers)
        if n_selected > 0:
            st.success(f"✅ {n_selected} paper(s) selected. Navigate to **Gap Identifier** to continue.")
        else:
            st.info("☝️ Select at least 3 papers to identify research gaps.")