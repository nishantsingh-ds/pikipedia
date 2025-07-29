# LeetCode AI Coach - Chrome Extension

> 🤖 Get instant AI-powered coaching feedback on your LeetCode solutions!

## Features

- **Real-time Analysis**: Automatically analyzes your code when you hit "Run" or "Submit"
- **Smart Feedback**: 
  - Identifies your algorithmic approach
  - Points out conceptual gaps using Feynman Technique
  - Provides first-principles optimization tips
  - Recommends similar problems to practice
- **Non-intrusive**: Floating panel that doesn't interfere with LeetCode's UI
- **Works everywhere**: Compatible with all LeetCode problem pages

## Installation

### Step 1: Load the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder from this project
5. The extension should now appear in your extensions list

### Step 2: Configure Backend URL

1. Open `chrome-extension/background.js`
2. Update the `API_BASE_URL` constant:
   ```javascript
   // For deployed backend (recommended)
   const API_BASE_URL = 'https://your-deployed-api.onrender.com';
   
   // For local development
   const API_BASE_URL = 'http://localhost:8000';
   ```
3. Save the file and reload the extension

### Step 3: Test the Extension

1. Navigate to any LeetCode problem (e.g., `https://leetcode.com/problems/two-sum/`)
2. Write or paste a solution in the code editor
3. Click "Run" or "Submit"
4. Look for the AI Coach feedback panel that appears below the problem description

## Usage

1. **Navigate** to any LeetCode problem
2. **Code** your solution in the editor
3. **Click** "Run" or "Submit" 
4. **Review** the AI feedback that appears in the floating panel

The feedback includes:
- **🎯 Approach**: What algorithm/pattern you're using
- **🧠 Conceptual Gaps**: Areas to study further
- **⚡ First-Principles Tips**: How to optimize your solution
- **🔗 Similar Problems**: Related LeetCode problems to practice

## Troubleshooting

### Extension not working?
- Check if the extension is enabled in `chrome://extensions/`
- Verify the backend URL is correctly configured
- Check the browser console for error messages

### No feedback appearing?
- Ensure you're on a LeetCode problem page (`https://leetcode.com/problems/*`)
- Verify the backend server is running and accessible
- Check if there's code in the editor before clicking Run/Submit

### API errors?
- Make sure the backend server has a valid OpenAI API key
- Check the network tab in developer tools for failed requests
- Verify CORS is properly configured on the backend

## Development

### Local Development Setup

1. Start the backend server:
   ```bash
   cd /path/to/backend
   uvicorn src.kidapp.api:app --reload --port 8000
   ```

2. Update `background.js` to use local URL:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000';
   ```

3. Reload the extension in Chrome after any changes

### File Structure

```
chrome-extension/
├── manifest.json       # Extension configuration
├── content.js         # Detects buttons & extracts code
├── background.js      # Handles API communication
├── styles.css         # UI styling
├── popup.html         # Extension popup
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple LeetCode problems
5. Submit a pull request

## License

MIT License - feel free to use and modify as needed!