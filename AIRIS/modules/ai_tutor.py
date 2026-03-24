"""
ai_tutor.py — AI Mini Research Tutor
=======================================
A chat-based research tutor powered entirely by FREE models.

Model choices (in priority order, all free):
1. google/flan-t5-base      — Fast, runs on CPU, good at Q&A and summarization
2. facebook/bart-large-cnn  — For summarization tasks (if flan fails)
3. Fallback: rule-based responses using paper content

Why flan-t5-base?
- Only ~250MB download
- Runs on CPU in ~5-10 seconds per response
- Instruction-tuned: handles "Explain X", "Summarize Y", "What is Z?" well
- No GPU required

NOTE: First run downloads the model (~250MB). Cached after that.
      The app shows a clear progress message during download.
"""

import streamlit as st
import re


# ── Lazy model loading ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """
    Load flan-t5-base from HuggingFace.
    @st.cache_resource ensures the model is loaded ONCE and reused across sessions.
    This prevents reloading the 250MB model on every interaction.
    """
    try:
        from transformers import pipeline
        # flan-t5-base: instruction-following T5 model by Google
        # task="text2text-generation" = takes text in, generates text out
        pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=200,
            # device=-1 forces CPU (no GPU required)
            device=-1,
        )
        return pipe, "flan-t5-base"
    except Exception as e:
        return None, str(e)


def build_prompt(user_question: str, context: str = "", mode: str = "general") -> str:
    """
    Build a structured prompt for flan-t5.
    flan-t5 responds best to explicit instruction format.
    """
    if mode == "explain" and context:
        return (
            f"You are a research assistant. Explain the following research paper "
            f"in simple language that a student can understand:\n\n"
            f"Paper Abstract: {context[:600]}\n\n"
            f"Question: {user_question}\n\n"
            f"Simple Explanation:"
        )
    elif mode == "limitation" and context:
        return (
            f"Read this research paper abstract and identify its main limitations:\n\n"
            f"Abstract: {context[:600]}\n\n"
            f"List 3 limitations of this research:"
        )
    elif mode == "method" and context:
        return (
            f"Based on this research abstract, suggest an improved or alternative method:\n\n"
            f"Abstract: {context[:600]}\n\n"
            f"Suggestion for improvement:"
        )
    else:
        return (
            f"You are a helpful research assistant for students.\n"
            f"Answer this research question clearly and concisely:\n\n"
            f"Question: {user_question}\n\n"
            f"Answer:"
        )


def detect_intent(message: str) -> str:
    """Detect what the user is asking about."""
    m = message.lower()
    if any(w in m for w in ["explain", "simple", "what is", "tell me", "describe", "understand"]):
        return "explain"
    elif any(w in m for w in ["limit", "weakness", "drawback", "problem with", "disadvantage", "gap in"]):
        return "limitation"
    elif any(w in m for w in ["improve", "better method", "suggest", "alternative", "enhance", "next step"]):
        return "method"
    elif any(w in m for w in ["publish", "journal", "conference", "where to", "submit"]):
        return "publish"
    else:
        return "general"


def rule_based_response(message: str, papers: list, intent: str) -> str:
    """
    Fallback responses when HuggingFace model is unavailable.
    Uses paper content + rule-based logic.
    """
    if intent == "publish":
        return """**Where to Publish Your Research Paper:**

📌 **Free Open-Access Journals:**
- *PLOS ONE* — Multidisciplinary, open access, no paywall
- *IEEE Access* — Engineering/CS, widely indexed
- *arXiv* — Preprint server (not peer-reviewed but widely cited)
- *Frontiers in AI* — AI-focused, open access

📌 **Student-Friendly Conferences:**
- *AAAI Student Abstract* — Competitive but prestigious
- *ACM-W Celebration* — For student research
- *Springer LNCS conferences* — Many accept student papers

📌 **Indian Journals (for BE projects):**
- *IJERT* (International Journal of Engineering Research and Technology)
- *IRJET* — Free to publish, widely accepted by Indian universities
- *JAIR* — Journal of AI Research (high quality, free)

💡 **Tip:** Always check the journal's Impact Factor and whether it's UGC-CARE listed if required by your university."""

    if intent == "explain" and papers:
        paper = papers[0] if papers else None
        if paper:
            return f"""**Simple Explanation of: "{paper['title']}"**

This paper is about: **{paper.get('category', 'AI research')}**

**In simple words:**
{paper.get('summary', 'No abstract available.')[:400]}

**Key takeaway:** This research explores solutions in the area of {paper.get('category', 'machine learning')} published in {paper.get('year', 'recent years')}. The authors propose a novel approach to address a specific challenge in this domain.

💡 Want a deeper explanation? Ask: *"What is the main contribution of this paper?"* or *"What methods did they use?"*"""

    if intent == "limitation":
        return """**Common Limitations in AI Research Papers:**

1. **Dataset Bias** — Most papers use benchmark datasets that may not reflect real-world diversity
2. **Computational Cost** — Many proposed models require expensive GPU infrastructure
3. **Generalizability** — Results often don't transfer to different domains or languages
4. **Lack of XAI** — Most models are black boxes with no explanation for their predictions
5. **Small Sample Size** — Limited data makes it hard to draw strong conclusions
6. **No Real-World Validation** — Many papers test only in lab conditions, not production environments

💡 Identifying which limitation applies to YOUR selected papers is a great way to find your research gap!"""

    if intent == "method":
        return """**Methods to Improve Existing Research:**

🔧 **If accuracy is the problem:**
→ Try ensemble models (XGBoost + Neural Network) or pre-trained transformers (BERT, T5)

🔍 **If explainability is missing:**
→ Add SHAP values or LIME to your predictions for feature attribution

🔒 **If privacy is a concern:**
→ Apply Federated Learning so data never leaves local devices

⚡ **If speed/efficiency is lacking:**
→ Use model pruning, knowledge distillation, or ONNX export for faster inference

📊 **If data is limited:**
→ Apply data augmentation, oversampling (SMOTE), or transfer learning from a larger dataset

🌍 **If generalization is weak:**
→ Use domain adaptation, cross-validation across multiple datasets"""

    # Generic fallback
    return """I'm your AI Research Tutor! Here are some things you can ask me:

- *"Explain this paper in simple words"*
- *"What are the limitations of this research?"*
- *"Suggest a better method for this problem"*
- *"Where should I publish my paper?"*
- *"What is federated learning?"*
- *"How do I write an abstract?"*

I'll do my best to help you understand research concepts! 🎓"""


def get_ai_response(message: str, context: str = "", intent: str = "general") -> str:
    """
    Get response from flan-t5 model (or fallback to rule-based).
    """
    pipe, model_name = load_model()

    if pipe is None:
        # Model failed to load — use rule-based fallback
        papers = st.session_state.get("papers", [])
        selected_ids = st.session_state.get("selected_papers", [])
        selected = [p for p in papers if p["id"] in selected_ids]
        return rule_based_response(message, selected, intent)

    # Build appropriate prompt
    prompt = build_prompt(message, context, intent)

    try:
        result = pipe(prompt, max_new_tokens=250, do_sample=False)
        response = result[0]["generated_text"].strip()

        # Clean up the response
        # Remove the prompt if echoed back
        if response.startswith(prompt[:50]):
            response = response[len(prompt):].strip()

        # If response is too short, add context
        if len(response) < 20:
            response += "\n\nFor more details, please refer to the full paper on arXiv."

        return response

    except Exception as e:
        papers = st.session_state.get("papers", [])
        selected_ids = st.session_state.get("selected_papers", [])
        selected = [p for p in papers if p["id"] in selected_ids]
        return rule_based_response(message, selected, intent)


def render_ai_tutor():
    """Main UI renderer for the AI Tutor chat page."""

    st.markdown("""
    <div class="page-header">
        <h1>🤖 AI Research Tutor</h1>
        <p>Ask me anything about your papers, research methods, writing tips, or where to publish.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Model info banner ──────────────────────────────────────────────────────
    with st.expander("ℹ️ About this AI Tutor", expanded=False):
        st.markdown("""
        **Model:** `google/flan-t5-base` (HuggingFace, 100% free)
        
        **What it can do:**
        - Explain research papers in simple language
        - Identify limitations of research methods  
        - Suggest improved approaches
        - Answer general research questions
        - Advise on where to publish
        
        **First run:** Downloads ~250MB model (cached permanently after that).
        
        **Performance:** ~5-15 seconds per response on CPU (no GPU needed).
        """)

    # ── Quick question buttons ─────────────────────────────────────────────────
    st.markdown("**💬 Quick Questions:**")
    quick_questions = [
        "Explain the selected papers in simple words",
        "What are the limitations of this research?",
        "Suggest a better method for this problem",
        "Where should I publish my paper?",
        "How do I write a good abstract?",
    ]

    cols = st.columns(len(quick_questions))
    for i, (col, q) in enumerate(zip(cols, quick_questions)):
        with col:
            if st.button(q[:25] + "…", key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                intent = detect_intent(q)

                # Get context from first selected paper
                selected_ids = st.session_state.get("selected_papers", [])
                papers = st.session_state.get("papers", [])
                selected = [p for p in papers if p["id"] in selected_ids]
                context = selected[0]["summary"] if selected else ""

                with st.spinner("Thinking…"):
                    response = get_ai_response(q, context=context, intent=intent)

                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    st.markdown("---")

    # ── Chat history display ───────────────────────────────────────────────────
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <div class="chat-avatar">👤</div>
                    <div class="chat-text">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-assistant">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-text">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:3rem; color:var(--muted);">
            <div style="font-size:3rem;">🤖</div>
            <div style="font-size:1rem; margin-top:0.5rem;">Ask me anything about your research!</div>
            <div style="font-size:0.8rem; margin-top:0.3rem;">Use the quick buttons above or type below.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Chat input ─────────────────────────────────────────────────────────────
    user_input = st.chat_input("Ask a research question…")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        intent = detect_intent(user_input)
        selected_ids = st.session_state.get("selected_papers", [])
        papers = st.session_state.get("papers", [])
        selected = [p for p in papers if p["id"] in selected_ids]
        context = selected[0]["summary"] if selected else ""

        with st.spinner("🤖 Thinking…"):
            response = get_ai_response(user_input, context=context, intent=intent)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # ── Clear chat ─────────────────────────────────────────────────────────────
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()