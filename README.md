# AI Study Assistant

**A smart learning companion powered by AI!** 📚✨

An intelligent study assistant built with Streamlit and Ollama that helps students learn effectively through summarization, quiz generation, flashcards, and topic explanations.

---

## 🌟 Features

### 📝 **Notes Summarizer**
- Quickly summarize lengthy study notes
- Extract key points automatically
- Identify important concepts
- Perfect for exam preparation

### ❓ **Quiz Generator**
- Generate 5 challenging multiple-choice questions
- Test your understanding of topics
- Get explanations for each answer
- Adaptive difficulty levels

### 🎴 **Flashcard Generator**
- Create 10+ interactive flashcards
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
- **Ollama** (LLM runtime)
- **Mistral Model** (or any Ollama-compatible model)

### Installation

#### 1. Install Ollama

Download and install Ollama from: https://ollama.ai

#### 2. Pull Mistral Model

Open your terminal and run:

```bash
ollama pull mistral
```

#### 3. Start Ollama Server

```bash
ollama serve
```

Keep this terminal running. The server will start on `http://localhost:11434`

#### 4. Set Up the Application

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

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage

### 1. **Using the Summarizer**

1. Select "📝 Summarizer" from the sidebar
2. Paste your study notes in the text area
3. Click "✨ Generate Summary"
4. View the summary, key points, and important concepts

**Example:**
```
Input: Long chapter notes on photosynthesis
Output: 
  - Summary of the process
  - Key points about light and dark reactions
  - Important concepts like chlorophyll, ATP, etc.
```

### 2. **Using the Quiz Generator**

1. Select "❓ Quiz Generator" from the sidebar
2. Paste your study notes
3. Click "🎯 Generate Quiz"
4. Review questions with multiple options
5. Check the correct answer and explanation

**Output Format:**
```
Question 1: Which organelle is responsible for photosynthesis?
A) Mitochondria
B) Chloroplast
C) Nucleus
D) Ribosome

Correct Answer: B
Explanation: Chloroplasts contain chlorophyll...
```

### 3. **Using Flashcard Generator**

1. Select "🎴 Flashcard Generator" from the sidebar
2. Paste your study notes
3. Click "🚀 Generate Flashcards"
4. Click on "📖 Answer" to reveal the back of each card
5. Study the cards repeatedly for better retention

**Card Format:**
```
Front: What is photosynthesis?
Back: The process by which plants convert light energy into chemical energy...
```

### 4. **Using Topic Explainer**

1. Select "🎓 Topic Explainer" from the sidebar
2. Enter any topic you want to learn about
3. Click "💡 Explain Topic"
4. Get comprehensive explanation with:
   - Clear definition
   - Key concepts
   - Examples
   - Important points
   - Real-world applications

**Example:**
```
Input: "Newton's Laws of Motion"
Output: Complete explanation with examples and applications
```

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
│   ├── __init__.py                # Module initialization
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
    └── ollama_client.py           # Ollama API client
```

---

## ⚙️ Configuration

### Ollama Settings

The application connects to Ollama on `http://localhost:11434` by default.

To change the settings, edit the `app.py` file:

```python
client = OllamaClient(
    base_url="http://localhost:11434",  # Change if needed
    model="mistral",                      # Change model name
    timeout=120                           # Adjust timeout (seconds)
)
```

### Supported Models

While the project uses Mistral by default, you can use any Ollama-compatible model:

```bash
# Other popular models:
ollama pull llama2
ollama pull neural-chat
ollama pull dolphin-mixtral
```

---

## 🔧 How It Works

### Architecture

```
User Input (Streamlit UI)
        ↓
    Prompt Template
        ↓
    Ollama Client
        ↓
    Mistral LLM
        ↓
    Response Parser
        ↓
    Formatted Output
```

### Key Components

1. **OllamaClient** (`utils/ollama_client.py`)
   - Manages API communication with Ollama
   - Handles errors and timeouts
   - Supports temperature and sampling parameters

2. **Modules** (`modules/`)
   - **Summarizer**: Extracts key information from notes
   - **QuizGenerator**: Creates questions with multiple options
   - **FlashcardGenerator**: Generates flashcards for learning
   - **Explainer**: Provides comprehensive topic explanations

3. **Prompts** (`prompts/`)
   - Carefully crafted templates to guide the LLM
   - Structured output formats
   - Educational focus

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

**Solution:**
1. Ensure Ollama is installed: https://ollama.ai
2. Run `ollama serve` in a terminal
3. Check if Mistral is pulled: `ollama list`
4. If not, run: `ollama pull mistral`

### "Request timeout"

**Solution:**
- The model is taking too long to respond
- Increase timeout in `app.py`: `timeout=300`
- Ensure your system has enough RAM
- Try with a smaller model

### "No response from model"

**Solution:**
- Check Ollama server is running
- Verify the model name is correct
- Check your internet connection (if using remote Ollama)

### Slow Response Times

**Solution:**
- Increase your system RAM
- Use a GPU for faster processing (check Ollama GPU docs)
- Try a smaller model like `neural-chat`

---

## 📊 Performance Tips

1. **Use GPU Acceleration**
   - Ollama supports GPU acceleration on NVIDIA, AMD, and Apple Silicon
   - Check: https://ollama.ai/docs#gpu

2. **Optimize System Resources**
   - Close unnecessary applications
   - Allocate more RAM if possible
   - Use SSD for better performance

3. **Experiment with Models**
   - Smaller models (neural-chat, dolphin) are faster
   - Larger models (mistral, llama2) are more accurate

---

## 🔮 Future Enhancements (Version 2 & 3)

### Version 2.0
- 📄 PDF file upload support
- 📥 PDF text extraction
- 💾 Save and load study notes
- 📥 Download results (PDF, CSV, JSON)

### Version 3.0
- 🧠 RAG (Retrieval Augmented Generation)
- 🔍 Semantic search across notes
- 💬 Chat with your notes
- 📈 Study progress tracking
- 🎯 Personalized learning recommendations

---

## 📝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM infrastructure
- **Mistral** - Powerful open-source LLM
- **Streamlit** - Easy-to-use web framework
- **Python Community** - Excellent tools and libraries

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the **Troubleshooting** section
2. Review **Ollama documentation**: https://ollama.ai/docs
3. Check Streamlit docs: https://docs.streamlit.io

---

## 🎯 Tips for Effective Learning

1. **Use Summarizer First** - Get an overview of the material
2. **Test with Quizzes** - Identify weak areas
3. **Study with Flashcards** - Build long-term memory
4. **Use Explainer for Concepts** - Deep understanding
5. **Review Regularly** - Spaced repetition for retention

---

**Happy Learning! 🚀📚**

Last Updated: June 2026
Version: 1.0
