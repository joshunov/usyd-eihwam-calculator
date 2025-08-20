# Deploy to Streamlit Community Cloud

## Steps:

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "USYD EIHWAM Calculator"
   git branch -M main
   ```

2. **Create repo on GitHub.com:**
   - Go to github.com
   - Click "New repository"
   - Name: `usyd-eihwam-calculator`
   - Public repository
   - Click "Create repository"

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/usyd-eihwam-calculator.git
   git push -u origin main
   ```

4. **Deploy to Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/usyd-eihwam-calculator`
   - Main file path: `app.py`
   - Click "Deploy!"

5. **Share with friends:**
   - You'll get a URL like: `https://your-username-usyd-eihwam-calculator-app-xyz.streamlit.app`
   - Send this URL to your friends
   - They can bookmark it and use it anytime

## What your friends will see:
- Professional web app with USYD branding
- Upload their transcript PDFs
- Get instant EIHWAM and WAM calculations
- Download results as CSV/JSON
- Mobile-friendly interface

## Security:
- All processing happens in the cloud
- No transcript data is stored
- Files are processed in memory only
- HTTPS encryption by default
