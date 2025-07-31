# LeetCode AI Coach - Chrome Extension

> 🤖 Get instant AI coaching feedback on your LeetCode solutions!

## Quick Installation

### Step 1: Load the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select this `chrome-extension` folder
5. The extension should now appear in your extensions list

### Step 2: Configure Backend URL

1. Open `background.js` in this folder
2. Update the `API_BASE_URL` constant:
   ```javascript
   // For local development
   const API_BASE_URL = 'http://localhost:8000';
   
   // For deployed backend  
   const API_BASE_URL = 'https://your-deployed-api.onrender.com';
   ```
3. Save the file and reload the extension

### Step 3: Test the Extension

1. Navigate to any LeetCode problem (e.g., `https://leetcode.com/problems/two-sum/`)
2. Write or paste a solution in the code editor
3. Click "Run" or "Submit"
4. Look for the AI Coach feedback panel that appears below the problem description

## How It Works

- **content.js** - Detects Run/Submit clicks and extracts code from Monaco/ACE editor
- **background.js** - Handles API communication with the backend
- **styles.css** - Styles the floating feedback panel
- **popup.html** - Simple extension popup interface

## Troubleshooting

**Extension not working?**
- Check if it's enabled in `chrome://extensions/`
- Verify backend URL in `background.js`
- Check browser console for errors (F12)

**No feedback appearing?**
- Ensure you're on a LeetCode problem page
- Verify backend is running
- Check if there's code in the editor

**Need help?**
- See the main README.md for full setup instructions
- Check the troubleshooting section for common issues