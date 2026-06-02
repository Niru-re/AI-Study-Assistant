# Deployment Guide

## Quick Start: Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key
Create a `.streamlit/secrets.toml` file in the project root:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### 3. Run the App
```bash
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
3. Select your GitHub repo
4. Select branch: `main`
5. Select file: `app.py`
6. Click "Deploy"

### Step 2: Configure Google Gemini

1. Sign up at [Google AI Studio](https://aistudio.google.com/apikey)
2. Get your free API key
3. In your Streamlit Cloud deployment:
   - Click the **Settings** gear icon (top right)
   - Go to **Secrets**
   - Add:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - Click "Save"
4. The app will automatically rerun with Gemini configured

---

## Configuration Options

The app respects the following secrets/environment variables:

```toml
# Required
GEMINI_API_KEY = "your-key"

# Optional
GEMINI_MODEL = "gemini-2.5-flash"  # Default model
```

## Troubleshooting

### API Key Errors
Ensure your `GEMINI_API_KEY` is correctly set in Streamlit Secrets (for cloud) or `.streamlit/secrets.toml` (for local).

### Dependency Errors
If you see missing package errors, ensure `google-generativeai` is in your `requirements.txt` and has been installed.
