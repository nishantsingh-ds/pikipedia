// LeetCode AI Coach - Background Script (Standalone Version)
console.log('LeetCode AI Coach background script loaded');

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'ANALYZE') {
    handleAnalyzeRequest(message.data, sendResponse);
    return true;
  }
});

async function handleAnalyzeRequest(data, sendResponse) {
  try {
    console.log('Received analyze request:', data);
    
    // Simulate AI analysis with predefined feedback
    const feedback = {
      approach: "This solution uses a straightforward approach - consider if there are more efficient patterns",
      gaps: [
        "Think about the time complexity - can you do better than checking every possibility?",
        "Consider what data structures might help you avoid repeated work", 
        "Ask yourself: what information from previous steps can you reuse?"
      ],
      principles: [
        "Start with a working solution, then optimize step by step",
        "Look for patterns like two pointers, sliding window, or divide and conquer",
        "Test your solution with edge cases like empty inputs or single elements"
      ],
      recommendations: [
        {title: "Two Sum", link: "https://leetcode.com/problems/two-sum/"},
        {title: "Valid Parentheses", link: "https://leetcode.com/problems/valid-parentheses/"},
        {title: "Best Time to Buy and Sell Stock", link: "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
        {title: "Maximum Subarray", link: "https://leetcode.com/problems/maximum-subarray/"},
        {title: "Merge Two Sorted Lists", link: "https://leetcode.com/problems/merge-two-sorted-lists/"}
      ]
    };
    
    // Add small delay to simulate AI processing
    setTimeout(() => {
      sendResponse({
        success: true,
        feedback: feedback
      });
    }, 1000);
    
  } catch (error) {
    console.error('Error:', error);
    sendResponse({
      success: false,
      error: error.message || 'Failed to analyze code'
    });
  }
}

chrome.runtime.onInstalled.addListener((details) => {
  console.log('LeetCode AI Coach installed/updated:', details.reason);
});
