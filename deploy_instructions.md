# Deployment Instructions

## Quick Start - Streamlit Community Cloud

1. **Install dependencies locally (if not done):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test locally:**
   ```bash
   python -m streamlit run app.py
   ```

3. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "USYD EIHWAM Calculator"
   git branch -M main
   git remote add origin https://github.com/YOURUSERNAME/usyd-eihwam-calculator.git
   git push -u origin main
   ```

4. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repo
   - Main file: `app.py`
   - Click "Deploy"

## Alternative - Hugging Face Spaces

1. **Create account at [huggingface.co](https://huggingface.co)**

2. **Create new Space:**
   - SDK: Streamlit
   - Hardware: CPU basic (free)

3. **Upload files or use git:**
   ```bash
   git clone https://huggingface.co/spaces/YOURUSERNAME/usyd-eihwam-calculator
   cd usyd-eihwam-calculator
   # Copy all files here
   git add .
   git commit -m "Add EIHWAM calculator"
   git push
   ```

## What Your Friends Will Get

- A public URL they can bookmark
- Upload their USYD transcripts securely
- Get instant EIHWAM and WAM calculations
- Download results as CSV/JSON
- Mobile-friendly interface

## Privacy & Security

- No transcripts are stored
- All processing happens in memory
- Files are automatically deleted after processing
- HTTPS encryption by default on both platforms

## Sharing with Friends

Once deployed, just share the URL! Example:
- Streamlit: `https://yourusername-usyd-eihwam-calculator-app-xyz123.streamlit.app`
- HuggingFace: `https://huggingface.co/spaces/yourusername/usyd-eihwam-calculator`
