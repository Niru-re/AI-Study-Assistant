"""
AI Study Assistant Main Application

A Streamlit-based application that uses Ollama and Mistral to help students
with note summarization, quiz generation, flashcard creation, and topic explanation.
"""

import streamlit as st
from pathlib import Path
import logging
from typing import Optional
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.ollama_client import OllamaClient
from modules.summarizer import Summarizer
from modules.quiz_generator import QuizGenerator
from modules.flashcard_generator import FlashcardGenerator
from modules.explainer import Explainer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_css() -> None:
    css_path = project_root / "assets" / "styles.css"
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error("Missing CSS file: assets/styles.css")

load_css()


@st.cache_resource
def get_ollama_client() -> OllamaClient:
    """Get cached Ollama client instance."""
    return OllamaClient(model="mistral:latest")


@st.cache_resource
def load_prompt_template(prompt_file: str) -> str:
    """Load prompt template from file."""
    try:
        prompt_path = project_root / "prompts" / prompt_file
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt file not found: {prompt_file}")
        raise st.error(f"Prompt template not found: {prompt_file}")


def check_ollama_connection() -> dict:
    """Run detailed health checks and return a dict of results."""
    client = get_ollama_client()
    try:
        results = client.health_check()
        return {"ok": True, "results": results}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def display_summary_results(result: dict) -> None:
    """Display summarizer results."""
    st.markdown("<div class='glass-card result-panel'>", unsafe_allow_html=True)
    st.markdown("### 📋 Summary Results")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Summary")
        st.write(result.get("summary", "No summary available"))

    with col2:
        st.markdown("### Key Points")
        key_points = result.get("key_points", [])
        if key_points:
            for point in key_points:
                st.write(f"• {point}")
        else:
            st.info("No key points extracted")

    st.markdown("### Important Concepts")
    st.write(result.get("important_concepts", "No concepts available"))
    st.markdown("</div>", unsafe_allow_html=True)


def display_quiz_results(questions: list) -> None:
    """Display quiz results with interactive elements."""
    st.markdown("<div class='glass-card result-panel'>", unsafe_allow_html=True)
    st.markdown("### ❓ Quiz Questions")
    
    if not questions or len(questions) == 0:
        st.warning("No questions generated. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Create tabs for each question
    tabs = st.tabs([f"Q{i+1}" for i in range(len(questions))])
    
    for tab_idx, tab in enumerate(tabs):
        with tab:
            q = questions[tab_idx]
            
            # Display question
            st.markdown(f"**Question {tab_idx + 1}:**")
            st.write(q.get("question", "Question not available"))
            
            # Display options
            st.markdown("**Options:**")
            options = q.get("options", {})
            for option_key in ["A", "B", "C", "D"]:
                option_text = options.get(option_key, "")
                if option_text:
                    st.write(f"{option_key}) {option_text}")
            
            # Display answer and explanation
            st.markdown("---")
            st.markdown("**Correct Answer:**")
            correct = q.get("correct_answer", "Not available")
            st.success(f"Answer: {correct}")
            
            explanation = q.get("explanation", "")
            if explanation:
                st.markdown("**Explanation:**")
                st.info(explanation)
    st.markdown("</div>", unsafe_allow_html=True)


def display_flashcards(flashcards: list) -> None:
    """Display flashcards with flip animation."""
    st.subheader("🎴 Flashcards")
    
    if not flashcards:
        st.warning("No flashcards generated. Please try again.")
        return
    
    # Create columns for flashcard grid
    cols = st.columns(2)
    
    for idx, card in enumerate(flashcards):
        with cols[idx % 2]:
            st.markdown("<div class='flashcard-card'>", unsafe_allow_html=True)
            st.markdown(f"### Flashcard {idx + 1}")
            st.markdown(f"<div style='margin-top:12px; color: var(--muted);'>{card.get('front', 'Question')}</div>", unsafe_allow_html=True)
            with st.expander("📖 Show answer"):
                st.markdown(f"<div style='padding: 18px; border-radius: 20px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.08);'>{card.get('back', 'Answer')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def display_explanation_results(result: dict) -> None:
    """Display explanation results."""
    st.markdown("<div class='glass-card result-panel'>", unsafe_allow_html=True)
    st.markdown("### 🎓 Topic Explanation")
    
    # Definition
    st.markdown("### Definition")
    st.write(result.get("definition", "No definition available"))
    
    # Key Concepts
    concepts = result.get("key_concepts", [])
    if concepts:
        st.markdown("### Key Concepts")
        for concept in concepts:
            st.write(f"• {concept}")
    
    # Examples
    examples = result.get("examples", [])
    if examples:
        st.markdown("### Examples")
        for example in examples:
            st.write(f"• {example}")
    
    # Important Points
    points = result.get("important_points", [])
    if points:
        st.markdown("### Important Points")
        for point in points:
            st.write(f"• {point}")
    
    # Real-world Applications
    applications = result.get("real_world_applications", [])
    if applications:
        st.markdown("### Real-World Applications")
        for app in applications:
            st.write(f"• {app}")

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    """Modern dashboard-style main application function."""

    client = get_ollama_client()
    load_css()

    st.markdown("<div class='orb orb-one'></div><div class='orb orb-two'></div>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand'>
          <div class='sidebar-icon'>AI</div>
          <div>
            <h2>Study AI</h2>
            <p class='muted'>Glassmorphism dashboard</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-panel'>Optimized for notes, quizzes, flashcards, and topic breakdowns.</div>", unsafe_allow_html=True)
        st.markdown("---")

        feature = st.radio("", [
            "Notes Summarizer",
            "Quiz Generator",
            "Flashcard Generator",
            "Topic Explainer"
        ], index=0)

        st.markdown("---")
        conn = check_ollama_connection()
        if conn.get("ok"):
            st.write("<div class='sidebar-status success'>Connected to Ollama</div>", unsafe_allow_html=True)
        else:
            st.write("<div class='sidebar-status warning'>Ollama unavailable</div>", unsafe_allow_html=True)
            with st.expander("Debug details"):
                st.write(conn.get("error"))

        st.markdown("<div class='sidebar-meta'>Model: <strong>mistral:latest</strong></div>", unsafe_allow_html=True)

    st.markdown("<div class='page-shell'>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='hero-panel'><div><h1>AI Study Assistant</h1><p class='muted'>Premium glassmorphism learning workspace with AI-powered study tools.</p></div><div class='hero-pill'>Live • <span>mistral:latest</span></div></div>", unsafe_allow_html=True)

    if feature == "Notes Summarizer":
        st.markdown("<div class='section-header'><h2>Notes Summarizer</h2><p class='muted'>Paste your notes and generate crisp summaries instantly.</p></div>", unsafe_allow_html=True)
        notes_input = st.text_area("", height=320, placeholder="Paste your study notes here...")
        if st.button("Generate Summary", key="summarize"):
            if not notes_input.strip():
                st.error("Please paste your notes first.")
            else:
                with st.spinner("Generating summary..."):
                    try:
                        prompt_template = load_prompt_template("summary_prompt.txt")
                        summarizer = Summarizer(client, prompt_template)
                        result = summarizer.summarize(notes_input)
                        display_summary_results(result)
                    except Exception as e:
                        st.error(str(e))

    elif feature == "Quiz Generator":
        st.markdown("<div class='section-header'><h2>Quiz Generator</h2><p class='muted'>Turn your notes into multiple-choice questions for active recall.</p></div>", unsafe_allow_html=True)
        notes_input = st.text_area("", height=320, placeholder="Paste your study notes here...")
        if st.button("Generate Quiz", key="quiz"):
            if not notes_input.strip():
                st.error("Please paste your notes first.")
            else:
                with st.spinner("Generating quiz..."):
                    try:
                        prompt_template = load_prompt_template("quiz_prompt.txt")
                        quiz_gen = QuizGenerator(client, prompt_template)
                        questions = quiz_gen.generate_quiz(notes_input)
                        display_quiz_results(questions)
                    except Exception as e:
                        st.error(str(e))

    elif feature == "Flashcard Generator":
        st.markdown("<div class='section-header'><h2>Flashcard Generator</h2><p class='muted'>Build flashcards from your notes for faster review.</p></div>", unsafe_allow_html=True)
        notes_input = st.text_area("", height=320, placeholder="Paste your study notes here...")
        if st.button("Generate Flashcards", key="flashcards"):
            if not notes_input.strip():
                st.error("Please paste your notes first.")
            else:
                with st.spinner("Generating flashcards..."):
                    try:
                        prompt_template = load_prompt_template("flashcard_prompt.txt")
                        fc_gen = FlashcardGenerator(client, prompt_template)
                        flashcards = fc_gen.generate_flashcards(notes_input)
                        display_flashcards(flashcards)
                    except Exception as e:
                        st.error(str(e))

    elif feature == "Topic Explainer":
        st.markdown("<div class='section-header'><h2>Topic Explainer</h2><p class='muted'>Ask a topic and get a clear, structured explanation.</p></div>", unsafe_allow_html=True)
        topic_input = st.text_input("", placeholder="e.g. Quantum Entanglement")
        if st.button("Explain Topic", key="explain"):
            if not topic_input.strip():
                st.error("Please enter a topic.")
            else:
                with st.spinner("Generating explanation..."):
                    try:
                        prompt_template = load_prompt_template("explain_prompt.txt")
                        explainer = Explainer(client, prompt_template)
                        result = explainer.explain(topic_input)
                        display_explanation_results(result)
                    except Exception as e:
                        st.error(str(e))

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='footer'>Made with AI • Glassmorphism dashboard</div>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
