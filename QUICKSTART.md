# AI Study Assistant - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Ollama
- Download from: https://ollama.ai
- Install and run: `ollama serve`

### Step 2: Pull Mistral Model
```bash
ollama pull mistral
```

### Step 3: Install Dependencies
```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Run the App
```bash
streamlit run app.py
```

✅ Done! Open http://localhost:8501

---

## 🎯 Feature Demos

### Test Summarizer
```
Input: Copy any textbook chapter or lecture notes
Output: Summary, key points, important concepts
```

### Test Quiz Generator
```
Input: Your study notes
Output: 5 multiple-choice questions with explanations
```

### Test Flashcard Generator
```
Input: Topics you want to learn
Output: 10 interactive flashcards
```

### Test Topic Explainer
```
Input: "Quantum Computing"
Output: Full explanation with examples and applications
```

---

## 📊 System Requirements

- **Minimum**: 4GB RAM, 2GB disk space
- **Recommended**: 8GB+ RAM, GPU support
- **Network**: Internet (for initial model download)

---

## 🔗 Useful Links

- Ollama: https://ollama.ai
- Streamlit: https://streamlit.io
- Mistral: https://mistral.ai
- Python: https://python.org

---

## ❓ Common Issues

| Issue | Solution |
|-------|----------|
| Can't connect to Ollama | Run `ollama serve` in separate terminal |
| Model not found | Run `ollama pull mistral` |
| Slow responses | Check system RAM, close other apps |
| Port 8501 already in use | Change port: `streamlit run app.py --server.port 8502` |

---

For detailed docs, see **README.md**
