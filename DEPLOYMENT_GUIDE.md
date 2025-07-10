# 🚀 WonderBot Deployment Guide

## Quick Deploy Options

### Option 1: Railway (Recommended - Free & Easy)

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your WonderBot repository**
5. **Railway will auto-detect it's a Python app**

#### Environment Variables (Required)
In Railway dashboard → Variables tab, add:
```
OPENAI_API_KEY=your_openai_api_key_here
```

#### Result
- **Live URL**: `https://your-app-name.railway.app`
- **Share this URL** with anyone to test your API

---

### Option 2: Render (Free Tier)

1. **Go to [Render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repository**

#### Configuration
- **Name**: `wonderbot`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn src.kidapp.api:app --host 0.0.0.0 --port $PORT`

#### Environment Variables
Add in Render dashboard:
```
OPENAI_API_KEY=your_openai_api_key_here
```

#### Result
- **Live URL**: `https://your-app-name.onrender.com`

---

### Option 3: Heroku (Paid but Reliable)

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-wonderbot-app`
4. **Deploy**: `git push heroku main`

#### Environment Variables
```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🌐 Sharing Your API

### For Web Interface
Share the URL: `https://your-app-name.railway.app`

### For API Testing
Share the API endpoint: `https://your-app-name.railway.app/generate`

### API Usage Examples

#### Text Question
```bash
curl -X POST "https://your-app-name.railway.app/generate" \
  -F "topic=Why do birds sing?" \
  -F "age=7" \
  -F "interests=nature,music"
```

#### Image Upload
```bash
curl -X POST "https://your-app-name.railway.app/generate" \
  -F "image=@path/to/image.jpg" \
  -F "age=8" \
  -F "interests=animals"
```

---

## 🔧 Local Development

### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
set OPENAI_API_KEY=your_key_here  # Windows
# export OPENAI_API_KEY=your_key_here  # Mac/Linux

# Start server
uvicorn src.kidapp.api:app --reload
```

### Access Locally
- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📋 Pre-deployment Checklist

- [ ] **GitHub repository** is up to date
- [ ] **OpenAI API key** is ready
- [ ] **requirements.txt** includes all dependencies
- [ ] **Procfile** is present (for Heroku)
- [ ] **runtime.txt** specifies Python version
- [ ] **Environment variables** are configured

---

## 🛠️ Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` has all dependencies
   - Ensure Python version is compatible

2. **API Key Error**
   - Verify `OPENAI_API_KEY` is set in environment variables
   - Check API key is valid and has credits

3. **Import Errors**
   - Make sure all files are committed to GitHub
   - Check file paths in imports

4. **Port Issues**
   - Railway/Render auto-assign ports
   - Use `$PORT` environment variable

---

## 📞 Support

If you need help with deployment:
1. Check the platform's documentation
2. Look at the build logs for errors
3. Verify environment variables are set correctly

---

## 🎉 Success!

Once deployed, your WonderBot will be accessible to anyone with the URL!

**Features Available:**
- ✅ Kid-friendly AI explanations
- ✅ DALL-E generated diagrams
- ✅ Text-to-speech audio
- ✅ Image analysis
- ✅ Built-in guardrails for safety
- ✅ Beautiful, responsive web interface 