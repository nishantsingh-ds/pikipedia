// LeetCode AI Coach - Background Script (Service Worker)
console.log('LeetCode AI Coach background script loaded');

// Configuration - Update this to your deployed backend URL
const API_BASE_URL = 'http://localhost:8000'; // Change to your deployed backend URL

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'ANALYZE') {
    handleAnalyzeRequest(message.data, sendResponse);
    return true; // Will respond asynchronously
  }
});

// Function to handle analyze requests
async function handleAnalyzeRequest(data, sendResponse) {
  try {
    console.log('Received analyze request:', data);
    
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        problemSlug: data.problemSlug,
        code: data.code
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('API response:', result);
    
    sendResponse({
      success: true,
      feedback: result.feedback
    });
    
  } catch (error) {
    console.error('Error calling analysis API:', error);
    
    sendResponse({
      success: false,
      error: error.message || 'Failed to analyze code'
    });
  }
}

// Extension installation/update handler
chrome.runtime.onInstalled.addListener((details) => {
  console.log('LeetCode AI Coach installed/updated:', details.reason);
});

// Keep service worker alive (manifest v3 requirement)
chrome.runtime.onMessage.addListener(() => {
  return true;
});