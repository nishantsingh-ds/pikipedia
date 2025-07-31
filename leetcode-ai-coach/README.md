# LeetCode AI Coach

> 🤖 Get instant AI-powered coaching feedback on your LeetCode solutions!

A minimal AI-driven Chrome extension with FastAPI backend that provides real-time coaching feedback when you solve LeetCode problems.

## ✨ Features

- **Real-time Analysis**: Automatically analyzes your code when you click "Run" or "Submit"
- **Smart Feedback**: 
  - 🎯 **Approach**: Identifies your algorithmic approach
  - 🧠 **Conceptual Gaps**: Points out missing concepts using Feynman Technique  
  - ⚡ **First-Principles Tips**: Provides optimization tips
  - 🔗 **Similar Problems**: Recommends 5 related LeetCode problems
- **Non-intrusive UI**: Floating panel that doesn't interfere with LeetCode's interface
- **Robust Error Handling**: Works with or without OpenAI API key (fallback responses)
- **Cross-platform**: Works on all operating systems with Chrome

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Google Chrome browser
- OpenAI API key (optional - has fallback responses)

### Backend Setup

1. **Clone and navigate to the project**
   ```bash
   git clone <your-repo-url>
   cd leetcode-ai-coach
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

4. **Start the backend server**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   ```

5. **Verify the server is running**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy","openai_configured":true/false}
   ```

### Chrome Extension Setup

1. **Open Chrome Extensions**
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)

2. **Load the extension**
   - Click "Load unpacked"
   - Select the `chrome-extension` folder from this project
   - The extension should appear in your extensions list

3. **Configure backend URL (if needed)**
   - Open `chrome-extension/background.js`
   - Update the `API_BASE_URL` if your backend is not on `localhost:8000`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000'; // or your deployed URL
   ```

4. **Test the extension**
   - Navigate to any LeetCode problem (e.g., `https://leetcode.com/problems/two-sum/`)
   - Write or paste a solution
   - Click "Run" or "Submit"
   - Look for the AI Coach feedback panel!

## 🎯 How to Use

1. **Navigate** to any LeetCode problem page
2. **Code** your solution in the editor
3. **Click** "Run" or "Submit" 
4. **Review** the AI feedback that appears below the problem description

The feedback panel includes:
- **🎯 Approach**: What algorithm/pattern you're using
- **🧠 Conceptual Gaps**: Areas to study further (Feynman Technique)
- **⚡ First-Principles Tips**: How to optimize your solution
- **🔗 Similar Problems**: Related LeetCode problems to practice

## 🧪 Testing the Backend

Test the API directly with curl:

```bash
# Health check
curl http://localhost:8000/health

# Test analyze endpoint
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "problemSlug": "two-sum",
    "code": "def twoSum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]"
  }'

# View API documentation
open http://localhost:8000/docs
```

## 🏗️ Project Structure

```
leetcode-ai-coach/
├── main.py                   # FastAPI backend application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── chrome-extension/        # Chrome extension files
│   ├── manifest.json       # Extension configuration
│   ├── content.js          # Code extraction & UI injection
│   ├── background.js       # API communication
│   ├── styles.css          # Floating panel styles
│   └── popup.html          # Extension popup
├── Procfile                 # Deployment configuration
├── runtime.txt             # Python version for deployment
├── render.yaml             # Render deployment config
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Configuration (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration  
PORT=8000
ENVIRONMENT=development
```

### Chrome Extension Configuration

Edit `chrome-extension/background.js` to point to your backend:

```javascript
// For local development
const API_BASE_URL = 'http://localhost:8000';

// For deployed backend
const API_BASE_URL = 'https://your-deployed-api.onrender.com';
```

## 🚀 Deployment

### Deploy Backend (Render/Heroku)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**
   - Connect your GitHub repo
   - The `render.yaml` file will configure everything automatically
   - Add your `OPENAI_API_KEY` in environment variables

3. **Update Chrome Extension**
   - Update `API_BASE_URL` in `background.js` to your deployed URL
   - Reload the extension in Chrome

### Local Development

For development with auto-reload:

```bash
# Start backend with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, watch for Chrome extension changes
# (Manually reload extension in Chrome after changes)
```

## 🐛 Troubleshooting

### Backend Issues

**Server won't start:**
```bash
# Check if port is in use
lsof -i :8000

# Try a different port
uvicorn main:app --reload --port 8001
```

**Dependencies missing:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Chrome Extension Issues

**Extension not working:**
- Check if extension is enabled in `chrome://extensions/`
- Verify backend URL in `background.js`
- Check browser console for errors (F12 → Console)

**No feedback appearing:**
- Ensure you're on a LeetCode problem page (`/problems/*`)
- Verify backend is running: `curl http://localhost:8000/health`
- Check if code is in the editor before clicking Run/Submit

**API errors:**
- Check browser Network tab for failed requests
- Verify CORS is enabled (it is by default)
- Ensure backend server is accessible

### OpenAI API Issues

**No OpenAI key:**
- The system works with fallback responses
- Add your key to `.env` for AI-powered feedback

**API rate limits:**
- The system has 15-second timeouts and fallbacks
- Check your OpenAI usage dashboard

## 🎮 Demo

Here's what the end-to-end flow looks like:

1. **User visits LeetCode**: `https://leetcode.com/problems/two-sum/`
2. **User writes code**: 
   ```python
   def twoSum(nums, target):
       for i in range(len(nums)):
           for j in range(i+1, len(nums)):
               if nums[i] + nums[j] == target:
                   return [i, j]
   ```
3. **User clicks "Run"**: Extension captures the code
4. **AI analyzes code**: Backend processes with OpenAI/fallback
5. **Feedback appears**: Floating panel shows coaching tips

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test on multiple LeetCode problems
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify as needed!

## 🙏 Acknowledgments

- Built with FastAPI, OpenAI, and Chrome Extensions API
- Inspired by the need for better coding interview preparation
- Fallback responses ensure functionality without API dependencies