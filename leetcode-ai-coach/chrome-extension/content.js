// LeetCode AI Coach - Content Script
console.log('LeetCode AI Coach content script loaded');

let feedbackPanel = null;
let isAnalyzing = false;

function getProblemSlug() {
  const pathMatch = window.location.pathname.match(/\/problems\/([^\/]+)/);
  return pathMatch ? pathMatch[1] : null;
}

function extractCodeFromMonaco() {
  try {
    const monaco = window.monaco;
    if (monaco && monaco.editor) {
      const editors = monaco.editor.getEditors();
      if (editors.length > 0) {
        return editors[0].getValue();
      }
    }
    
    const monacoEditors = document.querySelectorAll('.monaco-editor .view-lines');
    if (monacoEditors.length > 0) {
      return monacoEditors[0].textContent || '';
    }
    
    const codeElements = document.querySelectorAll('textarea[data-testid*="code"], pre.monaco-editor');
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
  
  const problemDescription = document.querySelector('[data-track-load="description_content"]') || 
                           document.querySelector('.content__u3I1') ||
                           document.body;
  
  if (problemDescription.parentNode) {
    problemDescription.parentNode.insertBefore(feedbackPanel, problemDescription.nextSibling);
  } else {
    document.body.appendChild(feedbackPanel);
  }
  
  document.getElementById('close-coach-panel').addEventListener('click', () => {
    feedbackPanel.remove();
    feedbackPanel = null;
  });
}

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

function handleCodeSubmission(event) {
  if (isAnalyzing) return;
  
  const problemSlug = getProblemSlug();
  const code = extractCodeFromMonaco();
  
  if (!problemSlug || !code || code.trim().length === 0) {
    console.error('Could not extract problem slug or code');
    return;
  }
  
  console.log('Extracted data:', { problemSlug, codeLength: code.length });
  
  isAnalyzing = true;
  createFeedbackPanel();
  
  chrome.runtime.sendMessage({
    type: 'ANALYZE',
    data: { problemSlug, code }
  }, (response) => {
    isAnalyzing = false;
    if (response && response.success) {
      updateFeedbackPanel(response.feedback);
    } else {
      console.error('Analysis failed:', response?.error);
    }
  });
}

function addButtonListeners() {
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
    console.log('Added listener to button:', button.textContent);
  });
}

function initialize() {
  addButtonListeners();
  setInterval(addButtonListeners, 2000);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initialize);
} else {
  initialize();
}
