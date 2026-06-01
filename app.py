"""
AI Study Assistant Main Application

A Streamlit-based application that uses Ollama and Mistral to help students
with note summarization, quiz generation, flashcard creation, and topic explanation.
"""

import os
import streamlit as st
from pathlib import Path
import logging
from typing import Optional
from utils.llm_factory import BaseLLMClient
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.llm_factory import get_llm_client, BaseLLMClient
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


def _is_streamlit_cloud() -> bool:
    """Check if running on Streamlit Cloud."""
    return os.environ.get("STREAMLIT_SERVER_HEADLESS") == "true" and os.environ.get("STREAMLIT_SERVER_RUN_ON_SAVE") is None

@st.cache_resource
def get_llm_client_cached() -> Optional[BaseLLMClient]:
    """Get cached LLM client instance."""
    return get_llm_client()


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


def check_llm_connection() -> dict:
    """Run health checks on LLM client."""
    client = get_llm_client_cached()
    if client is None:
        return {
            "ok": False,
            "error": "No LLM provider configured. Please set up Streamlit secrets or environment variables.",
            "provider": None,
        }
    try:
        results = client.health_check()
        # For Ollama, check if generate test passed
        if "generate" in results:
            if "error" in results["generate"]:
                return {
                    "ok": False,
                    "error": f"Ollama generation test failed: {results['generate']['error']}",
                    "provider": "ollama",
                    "results": results,
                }
        return {"ok": True, "results": results, "provider": os.environ.get("LLM_PROVIDER", "ollama")}
    except Exception as e:
        return {"ok": False, "error": str(e), "provider": os.environ.get("LLM_PROVIDER", "ollama")}


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


def show_setup_required() -> None:
    """Show setup instructions when LLM is not configured."""
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("""
    <div class='section-header'>
      <h2>⚙️ Setup Required</h2>
      <p class='muted'>No LLM provider configured. Please set up one of the following:</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Option 1: Groq (Recommended - Free & Fast)")
    st.markdown("""
    1. Go to https://console.groq.com/keys
    2. Create a free account and get your API key
    3. On Streamlit Cloud:
       - Go to **Settings → Secrets**
       - Add:
         ```
         LLM_PROVIDER = "groq"
         GROQ_API_KEY = "your-api-key"
         GROQ_MODEL = "mixtral-8x7b-32768"
         ```
    4. Rerun the app
    """)

    st.markdown("### Option 2: Local Ollama (Requires local deployment)")
    st.markdown("""
    1. Install Ollama: https://ollama.ai
    2. Run: `ollama run mistral`
    3. Set environment variables:
       ```
       LLM_PROVIDER=ollama
       OLLAMA_BASE_URL=http://localhost:11434
       OLLAMA_MODEL=mistral:latest
       ```
    4. Run locally: `streamlit run app.py`
    """)

    st.markdown("### Option 3: OpenAI")
    st.markdown("""
    1. Get API key from https://platform.openai.com/account/api-keys
    2. Add to Streamlit Secrets:
       ```
       LLM_PROVIDER = "openai"
       OPENAI_API_KEY = "your-api-key"
       OPENAI_MODEL = "gpt-4-turbo"
       ```
    """)

    st.markdown("### Option 4: Anthropic Claude")
    st.markdown("""
    1. Get API key from https://console.anthropic.com/
    2. Add to Streamlit Secrets:
       ```
       LLM_PROVIDER = "anthropic"
       ANTHROPIC_API_KEY = "your-api-key"
       ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
       ```
    """)

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    """Modern dashboard-style main application function."""

    client = get_llm_client_cached()
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
        conn = check_llm_connection()
        provider = conn.get("provider", "unknown").upper()
        if conn.get("ok"):
            st.write(f"<div class='sidebar-status success'>✓ {provider} Ready</div>", unsafe_allow_html=True)
        else:
            st.write(f"<div class='sidebar-status warning'>✗ {provider} Not Ready</div>", unsafe_allow_html=True)
            with st.expander("Debug info"):
                error_msg = conn.get("error", "Unknown error")
                st.error(error_msg)
                if "Ollama" in error_msg.upper():
                    st.info("💡 Ollama not running. Start it with: `ollama run mistral`")

        st.markdown(f"<div class='sidebar-meta'>Provider: <strong>{provider}</strong></div>", unsafe_allow_html=True)

    st.markdown("<div class='page-shell'>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='hero-panel'><div><h1>AI Study Assistant</h1><p class='muted'>Premium glassmorphism learning workspace with AI-powered study tools.</p></div><div class='hero-pill'>Live • <span>mistral:latest</span></div></div>", unsafe_allow_html=True)

    if feature == "Notes Summarizer":
        if client is None:
            show_setup_required()
            return
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
        if client is None:
            show_setup_required()
            return
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
        if client is None:
            show_setup_required()
            return
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
        if client is None:
            show_setup_required()
            return
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
