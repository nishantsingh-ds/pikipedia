# WonderBot Deployment Guide

This guide provides comprehensive instructions for deploying WonderBot to various cloud platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Free)

**Render** is the easiest option with a generous free tier.

#### Prerequisites
- GitHub repository with your WonderBot code
- OpenAI API key

#### Step 1: Prepare Your Repository
1. Ensure your repository is pushed to GitHub
2. Verify you have these files in your root directory:
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `src/kidapp/api.py`

#### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up/login with your GitHub account
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Choose your WonderBot repository

#### Step 3: Configure the Service
In your Render project dashboard:

1. **Name**: `wonderbot` (or any name you prefer)
2. **Environment**: `Python 3`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn src.kidapp.api:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: `8000` (Render sets this automatically)

#### Step 4: Deploy
- Click "Create Web Service"
- Render will automatically deploy your app
- You'll get a URL like: `https://your-app-name.onrender.com`

### Option 2: Heroku (Paid)

**Heroku** is reliable but requires a paid account.

#### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-wonderbot-app

# Add your OpenAI API key
heroku config:set OPENAI_API_KEY=your_api_key_here

# Deploy
git push heroku main

# Open your app
heroku open
```

### Option 3: Local Development

For local testing and development:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY=your_api_key_here

# Run the application
uvicorn src.kidapp.api:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuration Files

### requirements.txt
```
fastapi
uvicorn[standard]
python-multipart
crewai
crewai-tools
openai
python-dotenv
Pillow
requests
```

### Procfile
```
web: uvicorn src.kidapp.api:app --host 0.0.0.0 --port $PORT
```

### runtime.txt
```
python-3.11.9
```

## 🌐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `PORT` | Port for the web server | No (auto-set) |

## 📊 Monitoring & Logs

### Render
- Built-in logs in the Render dashboard
- Automatic health checks
- Easy rollback to previous versions

### Heroku
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

### Local Development
```bash
# Check logs (Railway/Render)
# View in your terminal where you started the app

# Check if app is running
curl http://localhost:8000/
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Build Failures
**Symptoms**: Deployment fails during build
**Solutions**:
- Check `requirements.txt` for correct dependencies
- Verify Python version in `runtime.txt`
- Ensure all files are committed to Git

#### 2. Runtime Errors
**Symptoms**: App starts but crashes
**Solutions**:
- Check environment variables are set correctly
- Verify OpenAI API key is valid
- Check logs for specific error messages

#### 3. Port Issues
**Symptoms**: App won't start
**Solutions**:
- Ensure `$PORT` is used in start command
- Check if port is already in use locally

### Debugging Commands

```bash
# Test API locally
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "topic=Why do birds sing?"

# Check environment variables
echo $OPENAI_API_KEY

# Test OpenAI connection
python -c "import openai; print('OpenAI configured')"
```

## 📈 Performance Optimization

### Render
- Free tier: 750 hours/month
- Automatic scaling based on traffic
- Built-in CDN for static files

### Heroku
- Paid dynos for better performance
- Add-on services available
- Custom domain support

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to Git
2. **Environment Variables**: Use platform-specific secret management
3. **HTTPS**: All platforms provide SSL certificates
4. **Rate Limiting**: Monitor OpenAI API usage

## 📞 Support

### Platform Support
- **Render**: Excellent documentation and support
- **Heroku**: Comprehensive guides and community
- **Local**: Full control but requires more setup

### Getting Help
1. Check the platform's documentation
2. Review error logs in the dashboard
3. Test locally to isolate issues
4. Check the [Render troubleshooting guide](https://render.com/docs/troubleshooting-deploys)

## 🎉 Success Checklist

- [ ] App deploys successfully
- [ ] Web interface loads at your URL
- [ ] API endpoints respond correctly
- [ ] OpenAI API key is working
- [ ] Image upload and analysis works
- [ ] Text Q&A functionality works
- [ ] Generated diagrams display correctly
- [ ] Audio files play properly
- [ ] Content safety guardrails are active

## 🚀 Next Steps

After successful deployment:

1. **Test all features** thoroughly
2. **Share your URL** with users
3. **Monitor usage** and performance
4. **Set up custom domain** (optional)
5. **Configure monitoring** (optional)

Your WonderBot is now live and ready to help kids learn! 🎓✨ 