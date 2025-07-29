// LeetCode AI Coach - Content Script
console.log('LeetCode AI Coach content script loaded');

// Global variables
let feedbackPanel = null;
let isAnalyzing = false;

// Function to extract problem slug from URL
function getProblemSlug() {
  const pathMatch = window.location.pathname.match(/\/problems\/([^\/]+)/);
  return pathMatch ? pathMatch[1] : null;
}

// Function to extract code from Monaco editor
function extractCodeFromMonaco() {
  try {
    // Try to get Monaco editor instance
    const monaco = window.monaco;
    if (monaco && monaco.editor) {
      const editors = monaco.editor.getEditors();
      if (editors.length > 0) {
        return editors[0].getValue();
      }
    }
    
    // Fallback: try to find Monaco editor DOM elements
    const monacoEditors = document.querySelectorAll('.monaco-editor .view-lines');
    if (monacoEditors.length > 0) {
      return monacoEditors[0].textContent || '';
    }
    
    // Another fallback: look for textarea or pre elements
    const codeElements = document.querySelectorAll('textarea[data-testid*="code"], pre.monaco-editor, .CodeMirror-code');
    for (const element of codeElements) {
      if (element.value) return element.value;
      if (element.textContent) return element.textContent;
    }
    
    return null;
  } catch (error) {
    console.error('Error extracting code:', error);
    return null;
  }
}

// Function to create and show feedback panel
function createFeedbackPanel() {
  if (feedbackPanel) {
    feedbackPanel.remove();
  }
  
  feedbackPanel = document.createElement('div');
  feedbackPanel.id = 'leetcode-ai-coach-panel';
  feedbackPanel.innerHTML = `
    <div class="coach-header">
      <h3>🤖 AI Coach</h3>
      <button id="close-coach-panel">&times;</button>
    </div>
    <div class="coach-content">
      <div class="loading">Analyzing your code...</div>
    </div>
  `;
  
  // Find a good place to inject the panel (next to problem description)
  const problemDescription = document.querySelector('[data-track-load="description_content"]') || 
                           document.querySelector('.content__u3I1') ||
                           document.querySelector('.question-content') ||
                           document.body;
  
  if (problemDescription.parentNode) {
    problemDescription.parentNode.insertBefore(feedbackPanel, problemDescription.nextSibling);
  } else {
    document.body.appendChild(feedbackPanel);
  }
  
  // Add close functionality
  document.getElementById('close-coach-panel').addEventListener('click', () => {
    feedbackPanel.remove();
    feedbackPanel = null;
  });
}

// Function to update feedback panel with AI response
function updateFeedbackPanel(feedback) {
  if (!feedbackPanel) return;
  
  const content = feedbackPanel.querySelector('.coach-content');
  content.innerHTML = `
    <div class="feedback-section">
      <h4>🎯 Approach</h4>
      <p>${feedback.approach}</p>
    </div>
    
    <div class="feedback-section">
      <h4>🧠 Conceptual Gaps</h4>
      <ul>
        ${feedback.gaps.map(gap => `<li>${gap}</li>`).join('')}
      </ul>
    </div>
    
    <div class="feedback-section">
      <h4>⚡ First-Principles Tips</h4>
      <ul>
        ${feedback.principles.map(tip => `<li>${tip}</li>`).join('')}
      </ul>
    </div>
    
    <div class="feedback-section">
      <h4>🔗 Similar Problems</h4>
      <ul>
        ${feedback.recommendations.map(rec => `<li><a href="${rec.link}" target="_blank">${rec.title}</a></li>`).join('')}
      </ul>
    </div>
  `;
}

// Function to show error in feedback panel
function showFeedbackError(error) {
  if (!feedbackPanel) return;
  
  const content = feedbackPanel.querySelector('.coach-content');
  content.innerHTML = `
    <div class="error">
      <h4>❌ Analysis Failed</h4>
      <p>Sorry, we couldn't analyze your code. ${error}</p>
      <button onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
    </div>
  `;
}

// Function to handle Run/Submit button clicks
function handleCodeSubmission(event) {
  if (isAnalyzing) return;
  
  const problemSlug = getProblemSlug();
  const code = extractCodeFromMonaco();
  
  if (!problemSlug) {
    console.error('Could not extract problem slug');
    return;
  }
  
  if (!code || code.trim().length === 0) {
    console.error('Could not extract code');
    return;
  }
  
  console.log('Extracted data:', { problemSlug, codeLength: code.length });
  
  isAnalyzing = true;
  createFeedbackPanel();
  
  // Send message to background script
  chrome.runtime.sendMessage({
    type: 'ANALYZE',
    data: { problemSlug, code }
  }, (response) => {
    isAnalyzing = false;
    if (response && response.success) {
      updateFeedbackPanel(response.feedback);
    } else {
      showFeedbackError(response?.error || 'Unknown error occurred');
    }
  });
}

// Function to add click listeners to Run/Submit buttons
function addButtonListeners() {
  // Common selectors for Run/Submit buttons on LeetCode
  const buttonSelectors = [
    'button[data-e2e-locator="console-run-button"]',
    'button[data-e2e-locator="console-submit-button"]',
    '[data-cy="run-code-btn"]',
    '[data-cy="submit-code-btn"]'
  ];
  
  buttonSelectors.forEach(selector => {
    const buttons = document.querySelectorAll(selector);
    buttons.forEach(button => {
      if (!button.hasAttribute('data-coach-listener')) {
        button.addEventListener('click', handleCodeSubmission);
        button.setAttribute('data-coach-listener', 'true');
      }
    });
  });
  
  // Also listen for buttons that might be added dynamically
  const runButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.toLowerCase().includes('run') && 
    !btn.hasAttribute('data-coach-listener')
  );
  
  const submitButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.toLowerCase().includes('submit') && 
    !btn.hasAttribute('data-coach-listener')
  );
  
  [runButton, submitButton].filter(Boolean).forEach(button => {
    button.addEventListener('click', handleCodeSubmission);
    button.setAttribute('data-coach-listener', 'true');
  });
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'FEEDBACK') {
    updateFeedbackPanel(message.feedback);
    sendResponse({ success: true });
  } else if (message.type === 'ERROR') {
    showFeedbackError(message.error);
    sendResponse({ success: true });
  }
});

// Initialize when DOM is ready
function initialize() {
  addButtonListeners();
  
  // Re-check for buttons periodically since LeetCode uses SPA routing
  setInterval(addButtonListeners, 2000);
}

// Start when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initialize);
} else {
  initialize();
}

// Also reinitialize on navigation (for SPA behavior)
let currentUrl = window.location.href;
setInterval(() => {
  if (window.location.href !== currentUrl) {
    currentUrl = window.location.href;
    setTimeout(initialize, 1000); // Delay to let new page load
  }
}, 1000);