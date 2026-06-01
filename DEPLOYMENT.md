# Deployment Guide

## Quick Start: Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run with Local Ollama
```bash
# In terminal 1: Start Ollama server
ollama run mistral

# In terminal 2: Run the Streamlit app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account with the repo pushed
- Streamlit Cloud account (free tier available)

### Step 1: Deploy the App
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repo: `Niru-re/AI-Study-Assistant`
4. Select branch: `main`
5. Select file: `app.py`
6. Click "Deploy"

### Step 2: Configure LLM Provider

Since Streamlit Cloud cannot access your local Ollama instance, you **must** use a cloud LLM provider.

#### Option A: Groq (Recommended - Free & Fast)

1. Sign up at https://console.groq.com
2. Get your free API key
3. In your Streamlit Cloud deployment:
   - Click the **Settings** gear icon (top right)
   - Go to **Secrets**
   - Add:
     ```toml
     LLM_PROVIDER = "groq"
     GROQ_API_KEY = "your-api-key-here"
     GROQ_MODEL = "mixtral-8x7b-32768"
     ```
   - Click "Save"
4. The app will automatically rerun with Groq configured

#### Option B: OpenAI

1. Get API key from https://platform.openai.com/account/api-keys
2. In Streamlit Secrets, add:
   ```toml
   LLM_PROVIDER = "openai"
   OPENAI_API_KEY = "your-api-key-here"
   OPENAI_MODEL = "gpt-4-turbo"
   ```
3. The app will automatically rerun with OpenAI configured

#### Option C: Anthropic Claude

1. Get API key from https://console.anthropic.com/
2. In Streamlit Secrets, add:
   ```toml
   LLM_PROVIDER = "anthropic"
   ANTHROPIC_API_KEY = "your-api-key-here"
   ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
   ```
3. The app will automatically rerun with Anthropic configured

#### Option D: Remote Ollama Server

If you have a publicly accessible Ollama instance, you can use it:

```toml
LLM_PROVIDER = "ollama"
OLLAMA_BASE_URL = "https://your-ollama-server.com"
OLLAMA_MODEL = "mistral:latest"
```

---

## Environment Variables

The app respects the following environment variables (for local development):

```bash
# LLM Provider
LLM_PROVIDER=groq            # Options: groq, openai, anthropic, ollama

# Groq
GROQ_API_KEY=your-key
GROQ_MODEL=mixtral-8x7b-32768

# OpenAI
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4-turbo

# Anthropic
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Ollama (local or remote)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:latest
OLLAMA_TIMEOUT=300
```

### For Local Development

Create a `.env` file in the project root:

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:latest
```

Then run:
```bash
streamlit run app.py
```

---

## Troubleshooting

### "No LLM provider configured"

This means no environment variables or secrets are set. Follow the deployment guide above for your chosen provider.

### "Connection refused" on Streamlit Cloud

Streamlit Cloud apps cannot reach `localhost`. Use a cloud LLM provider instead:
- Groq (free)
- OpenAI
- Anthropic
- Or deploy Ollama on a publicly accessible server

### "ModuleNotFoundError: No module named 'groq'"

The optional dependencies aren't installed. Streamlit Cloud will automatically install packages from `requirements.txt`. If needed, explicitly add to Streamlit settings:

```toml
# .streamlit/config.toml
[python]
installPackages = true
```

---

## Deployment Status

Your app is deployed at:
https://ai-study-assistant-kvobtvwgxrvnh5pa5wbngp.streamlit.app/

### Next Steps

1. Go to Streamlit Cloud dashboard
2. Click your app
3. Click Settings → Secrets
4. Add your LLM provider configuration
5. The app will rerun automatically

---

## Support

For issues or questions:
- Check the sidebar "Setup Required" tab for inline setup instructions
- Review this guide
- Check Streamlit documentation: https://docs.streamlit.io/deploy/streamlit-cloud
