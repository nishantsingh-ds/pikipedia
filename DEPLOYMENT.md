# 🚀 WonderBot Deployment Guide

This guide will help you deploy your WonderBot to a public platform so others can access it via a URL.

## 📋 Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **OpenAI API Key**: You'll need this for the AI features
3. **Basic Git knowledge**: To push your code

## 🎯 Quick Deploy Options

### Option 1: Railway (Recommended - Free)

**Railway** is the easiest option with a generous free tier.

#### Step 1: Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your KidApp repository
5. Railway will automatically detect it's a Python app

#### Step 3: Configure Environment Variables
In your Railway project dashboard:
1. Go to "Variables" tab
2. Add: `OPENAI_API_KEY` = `your_openai_api_key_here`
3. Add: `PORT` = `8000` (Railway sets this automatically)

#### Step 4: Deploy
- Railway will automatically deploy your app
- You'll get a URL like: `https://your-app-name.railway.app`

### Option 2: Render (Free)

**Render** is another great free option.

#### Step 1: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `wonderbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -e .`
   - **Start Command**: `uvicorn src.kidapp.api:app --host 0.0.0.0 --port $PORT`

#### Step 2: Environment Variables
Add in Render dashboard:
- `OPENAI_API_KEY` = `your_openai_api_key_here`

### Option 3: Heroku (Paid but Reliable)

**Heroku** is very reliable but now requires a paid plan.

#### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-kidapp-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_openai_api_key_here

# Deploy
git push heroku main
```

## 🔧 Local Testing Before Deployment

Test your app locally first:

```bash
# Install dependencies
pip install -e .

# Test locally
python deploy.py

# Or with uvicorn directly
uvicorn src.kidapp.api:app --host 0.0.0.0 --port 8000
```

## 🌐 After Deployment

### Share Your App
Once deployed, you'll get a URL like:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Heroku: `https://your-app-name.herokuapp.com`

### Test the Deployment
1. **Frontend**: Visit your URL in a browser
2. **API**: Test with curl:
   ```bash
   curl -X POST "https://your-app-url/generate" \
     -F "topic=Why do birds sing?" \
     -F "age=7"
   ```

## 🔒 Security Considerations

### For Production
1. **CORS**: Update `allow_origins` in `api.py` to your domain
2. **API Key**: Never commit your `.env` file
3. **Rate Limiting**: Consider adding rate limiting for public use
4. **HTTPS**: All platforms provide HTTPS automatically

### Environment Variables
Make sure these are set in your deployment platform:
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Usually set automatically by the platform

## 🐛 Troubleshooting

### Common Issues

1. **Port Issues**
   - Make sure your app uses `$PORT` environment variable
   - Check the Procfile is correct

2. **Dependencies**
   - Ensure `pyproject.toml` includes all dependencies
   - Some platforms have size limits

3. **Environment Variables**
   - Double-check `OPENAI_API_KEY` is set correctly
   - Verify the variable name matches exactly

4. **File Permissions**
   - Make sure `uploaded_images` directory can be created
   - Some platforms have read-only filesystems

### Debug Commands

```bash
# Check logs (Railway/Render)
# Use the platform's dashboard

# Check if app starts locally
python -c "from src.kidapp.api import app; print('App loads successfully')"

# Test API locally
curl -X POST "http://localhost:8000/generate" -F "topic=test"
```

## 📊 Monitoring

### Free Monitoring Options
1. **Railway**: Built-in logs and metrics
2. **Render**: Basic monitoring included
3. **Uptime Robot**: Free uptime monitoring

### Add Monitoring
```python
# Add to your api.py for basic logging
import logging
logging.basicConfig(level=logging.INFO)
```

## 🎉 Success!

Once deployed, you can:
1. **Share the URL** with others
2. **Test the frontend** and API
3. **Monitor usage** and performance
4. **Scale up** if needed

Your KidApp is now accessible worldwide! 🌍

---

**Need help?** Check the platform's documentation or create an issue in your repository. 