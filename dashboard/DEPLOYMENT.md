# Dashboard Deployment & Sharing Guide

## 🚀 Getting Started Quickly

### Windows Users
Simply double-click:
1. `setup.bat` — Installs all required packages
2. `start_dashboard.bat` — Launches the dashboard

### Mac/Linux Users
Open Terminal in the dashboard folder:
```bash
# Install dependencies
pip install -r requirements.txt

# Start dashboard
streamlit run app.py
```

## 📦 Sharing the Dashboard Locally

### Via USB Drive
1. Copy the entire `dashboard/` folder to USB
2. Recipients run: `setup.bat` then `start_dashboard.bat`
3. Dashboard opens locally in their browser

### Via Network Share
1. Place `dashboard/` folder on shared network drive
2. Others access from their computer:
   ```bash
   cd \\network\share\dashboard
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```

### Via Zip File
1. Zip the entire `dashboard/` folder
2. Send the `.zip` file
3. Recipients extract and run `setup.bat`

## ☁️ Cloud Deployment

### Option 1: Streamlit Cloud (Recommended for GitHub users)

**Pros**: Free, simple, auto-deploys from GitHub  
**Cons**: Requires GitHub account, data stored remotely

Steps:
1. Push your dashboard to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and main file
5. Your dashboard is live!

### Option 2: Heroku (Free tier discontinued)

Alternative platforms with free tiers:
- **Railway.app** (easy, free tier)
- **Render.com** (free tier available)
- **PythonAnywhere** (for Python apps)

### Option 3: Docker + Any Cloud Provider

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

**Build and run:**
```bash
docker build -t dashboard .
docker run -p 8501:8501 dashboard
```

Deploy to:
- AWS (ECS/Fargate)
- Google Cloud (Cloud Run)
- Azure (Container Instances)
- DigitalOcean (App Platform)

## 🔧 Customization Before Sharing

### Update Your Data
1. Run your notebook to completion
2. Update `extract_data.py` to parse YOUR results
3. Run: `python extract_data.py`
4. Commit to version control

### Customize Branding
Edit `app.py` to:
- Change colors in the CSS section
- Update the title and description
- Add your institution/project logo

### Add Your Own Content
1. Edit page content directly in Python files
2. Add new pages by creating files in `pages/`
3. Add new visualizations to `extract_data.py`

## 📊 Updating Results

When you have new model results:

1. **Run your notebook** to completion
2. **Update `extract_data.py`** to read your new outputs
3. **Run extraction again**:
   ```bash
   python extract_data.py
   ```
4. **Refresh the browser** — Streamlit auto-reloads
5. **Commit and push** (if using version control)

## 🔐 Security Considerations

### Before Sharing Publicly
- ⚠️ Remove sensitive student data (use anonymized IDs)
- ⚠️ Don't commit `.env` files with API keys
- ⚠️ Check that data files don't contain PII
- ⚠️ Use HTTPS if deploying to production

### Local/Institutional Sharing
- Safe to share as-is
- Ensure recipients have appropriate access rights
- Consider using `.gitignore` for sensitive data

## 📈 Performance Optimization

For large datasets:

1. **Cache data**:
   ```python
   @st.cache_data
   def load_data():
       return pd.read_csv("data.csv")
   ```

2. **Lazy load visualizations**:
   Only load images when tab is clicked

3. **Compress images**:
   Store PNG files at lower DPI or as WebP

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with verbose output
streamlit run app.py --logger.level=debug
```

### Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Data files not found
Check that `data/` folder has all CSV and PNG files:
```bash
ls -la data/
```

## 📚 Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/deploy)
- [Docker Documentation](https://docs.docker.com)
- [Railway.app Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)

## 🎯 Next Steps

1. ✅ Test locally: `start_dashboard.bat`
2. ✅ Verify all pages load correctly
3. ✅ Choose deployment method
4. ✅ Share the dashboard!

---

**Need Help?** Check the main `README.md` or Streamlit documentation.
