# AI Study Assistant

**A smart learning companion powered by Google Gemini!** 📚✨

An intelligent study assistant built with Streamlit and Google Gemini that helps students learn effectively through summarization, quiz generation, flashcards, and topic explanations.

---

## 🌟 Features

### 📝 **Notes Summarizer**
- Quickly summarize lengthy study notes
- Extract key points automatically
- Identify important concepts
- Perfect for exam preparation

### ❓ **Quiz Generator**
- Generate challenging multiple-choice questions
- Test your understanding of topics
- Get explanations for each answer
- Powered by high-quality AI models

### 🎴 **Flashcard Generator**
- Create interactive flashcards
- Effective for active recall learning
- Question-answer format
- Perfect for memorization and retention

### 🎓 **Topic Explainer**
- Get comprehensive explanations of any topic
- Learn through real-world examples
- Understand key concepts
- Discover practical applications

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Google Gemini API Key** (Free from [Google AI Studio](https://aistudio.google.com/apikey))

### Installation

#### 1. Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a free API key
3. Copy the key for the next steps

#### 2. Set Up the Application

Clone or download this project, then:

```bash
# Navigate to project directory
cd AI-Study-Assistant

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure API Key

Create a `.streamlit/secrets.toml` file in the project root:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

Alternatively, set an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage

### 1. **Using the Summarizer**

1. Select "📝 Notes Summarizer" from the sidebar
2. Paste your study notes in the text area
3. Click "✨ Generate Summary"
4. View the summary, key points, and important concepts

### 2. **Using the Quiz Generator**

1. Select "❓ Quiz Generator" from the sidebar
2. Paste your study notes
3. Click "🎯 Generate Quiz"
4. Review questions with multiple options
5. Check the correct answer and explanation

### 3. **Using Flashcard Generator**

1. Select "🎴 Flashcard Generator" from the sidebar
2. Paste your study notes
3. Click "🚀 Generate Flashcards"
4. Click on "📖 Show answer" to reveal the back of each card

### 4. **Using Topic Explainer**

1. Select "🎓 Topic Explainer" from the sidebar
2. Enter any topic you want to learn about
3. Click "💡 Explain Topic"
4. Get a comprehensive explanation with definition, concepts, examples, and real-world applications

---

## 📁 Project Structure

```
AI-Study-Assistant/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── modules/
│   ├── summarizer.py              # Notes summarization logic
│   ├── quiz_generator.py          # Quiz generation logic
│   ├── flashcard_generator.py     # Flashcard generation logic
│   └── explainer.py               # Topic explanation logic
│
├── prompts/
│   ├── summary_prompt.txt         # Prompt for summarization
│   ├── quiz_prompt.txt            # Prompt for quiz generation
│   ├── flashcard_prompt.txt       # Prompt for flashcards
│   └── explain_prompt.txt         # Prompt for topic explanation
│
└── utils/
    ├── llm_factory.py             # LLM Factory for Gemini
    └── __init__.py                # Utils package init
```

---

## ⚙️ Configuration

The application uses **Gemini 2.5 Flash** by default for fast and accurate responses. You can change the model by setting the `GEMINI_MODEL` environment variable.

Made with Google Gemini • AI Study Assistant
