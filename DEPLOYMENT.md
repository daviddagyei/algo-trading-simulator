# Streamlit Cloud Deployment Checklist

## ✅ Files Created/Updated for Deployment

### Required Files:
- [x] `streamlit_app.py` - Main application file
- [x] `requirements.txt` - Python dependencies
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `packages.txt` - System dependencies (if needed)

### Optional Files:
- [x] `health_check.py` - Import verification script
- [x] Updated `.gitignore` - Deployment file management

## 🚀 Deployment Steps

### 1. Repository Setup
- [x] Code committed to GitHub repository: `daviddagyei/algo-trading-simulator`
- [x] Repository is public and accessible at: https://github.com/daviddagyei/algo-trading-simulator
- [x] Main branch contains all necessary files
- [x] Latest changes pushed to remote repository

### 2. Streamlit Cloud Deployment

#### Method 1: Direct URL (Recommended)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Enter repository URL: `https://github.com/daviddagyei/algo-trading-simulator`
4. Set branch: `main`
5. Set main file path: `streamlit_app.py`
6. Click "Deploy"

#### Method 2: GitHub Integration
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select repository: `daviddagyei/algo-trading-simulator`
5. Set branch: `main`
6. Set main file path: `streamlit_app.py`
7. Click "Deploy"

### 3. Troubleshooting Common Issues

#### Issue: "Code is not connected to a remote GitHub repository"
**Solutions:**
1. **Make sure repository is public**:
   - Go to https://github.com/daviddagyei/algo-trading-simulator
   - Click Settings → scroll down to "Danger Zone"
   - If repository is private, click "Change visibility" → "Make public"

2. **Use HTTPS URL instead of SSH**:
   - Repository URL: `https://github.com/daviddagyei/algo-trading-simulator`
   - NOT: `git@github.com:daviddagyei/algo-trading-simulator.git`

3. **Ensure latest code is pushed**:
   ```bash
   git add .
   git commit -m "Latest changes for deployment"
   git push origin main
   ```

4. **Try direct repository URL entry**:
   - Instead of connecting GitHub account, manually enter the repository URL
   - Use: `https://github.com/daviddagyei/algo-trading-simulator`

### 3. Post-Deployment
- [ ] Test all strategies work correctly
- [ ] Verify data loading functions properly
- [ ] Check visualizations render correctly
- [ ] Test with different assets and parameters

## 📋 Configuration Details

### `requirements.txt` - Core Dependencies Only
```
streamlit>=1.25.0
pandas>=1.3.0
numpy>=1.21.0
plotly>=5.15.0
yfinance>=0.1.87
pytz>=2021.1
```

### `.streamlit/config.toml` - Deployment Settings
```toml
[general]
email = "your-email@example.com"

[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### `packages.txt` - System Dependencies
```
freeglut3-dev
libgtk-3-dev
```

## 🔧 Deployment Notes

1. **Streamlit Cloud Environment**: 
   - Python 3.9+
   - 1GB RAM
   - 1 CPU core
   - 800MB disk space

2. **Performance Considerations**:
   - Use caching with `@st.cache_data` for expensive operations
   - Limit data fetching to necessary date ranges
   - Consider using session state for large computations

3. **Known Limitations**:
   - 10-minute timeout for long-running operations
   - Limited memory for very large datasets
   - Yahoo Finance rate limiting may affect data fetching

## 🐛 Troubleshooting

### Common Issues:
1. **Import Errors**: Check `requirements.txt` has all dependencies
2. **Memory Issues**: Reduce data size or add caching
3. **Timeout Issues**: Optimize data loading and computations
4. **Yahoo Finance Errors**: Add error handling for API failures

### Health Check:
Run `python health_check.py` locally to verify all imports work before deployment.

## 📱 Expected URL Format
After deployment: `https://daviddagyei-algo-trading-simulator-streamlit-app-[hash].streamlit.app`
