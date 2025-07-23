# 🧪 WonderBot Testing Guide

This guide explains how to verify that WonderBot's automated testing is working correctly.

## 🚀 Quick Status Check

### 1. GitHub Actions Status
- **URL**: https://github.com/nishantsingh-ds/pikipedia/actions
- **Look for**: Green checkmarks ✅ = tests passing, Red X ❌ = tests failing

### 2. Latest Workflow Status
```bash
# Check latest run status via API
curl -s "https://api.github.com/repos/nishantsingh-ds/pikipedia/actions/runs?per_page=1" | \
  python3 -c "import sys, json; run = json.load(sys.stdin)['workflow_runs'][0]; print(f'Status: {run[\"status\"]} / {run[\"conclusion\"]} at {run[\"created_at\"]}')"
```

## 🔧 Local Testing (Before CI)

### 1. Test Dependencies
```bash
python3 test_local.py
```

### 2. Manual Server Test
```bash
# Start server
uvicorn src.kidapp.api:app --host 0.0.0.0 --port 8000 &

# Test health endpoint
curl http://localhost:8000/health

# Test generate endpoint
curl -X POST "http://localhost:8000/generate" \
  -F "topic=Why is the sky blue?" \
  -F "age=7"
```

## 📋 What the CI Tests Check

### Automated Quality Criteria
Each generated answer is evaluated on:

1. **Kid-Friendly** ✅ "Is this appropriate for a 7-year-old?"
2. **Uses Analogies** ✅ "Does this use analogies or metaphors?"
3. **Factually Correct** ✅ "Is this factually accurate?"

### Test Questions (20 total)
- "Why is the sky blue?"
- "What is a black hole?"
- "How do plants eat?"
- "Why do we dream?"
- And 16 more educational topics...

## 🔍 How to Read Test Results

### ✅ Success Indicators
- **GitHub Actions**: Green checkmark on main branch
- **Slack Notification**: "WonderBot CI passed!" message
- **Log Output**: "All answers passed Judgeval evaluation"
- **Files Created**: `wonderbot_outputs.csv` and `judgeval_results.csv`

### ❌ Failure Indicators
- **GitHub Actions**: Red X mark
- **Slack Notification**: "WonderBot CI failed!" message  
- **Log Output**: "Some answers failed the evaluation!"
- **Error Messages**: Specific failure details in logs

## 🐛 Common Issues & Solutions

### 1. "Run Judgeval" Step Failing
**Cause**: Judgeval dependency or configuration issue
**Fix**: 
```bash
pip install judgeval==0.1.7
judgeval evaluate --input wonderbot_outputs.csv --criteria criteria.yaml --output judgeval_results.csv
```

### 2. Server Startup Timeout
**Cause**: Backend not starting within 30 seconds
**Check**: 
- OPENAI_API_KEY is set
- Dependencies installed correctly
- No port conflicts

### 3. API Connection Errors  
**Cause**: Network issues or server not responding
**Fix**:
- Verify server is running: `curl http://localhost:8000/health`
- Check server logs for errors
- Ensure proper error handling in API

### 4. OpenAI API Issues
**Cause**: Missing or invalid API key
**Fix**:
- Set `OPENAI_API_KEY` in GitHub repository secrets
- Verify API key is valid and has sufficient credits
- Check API rate limits

## 📊 Expected Test Output

### Successful Run Example
```
✅ Dependencies installed successfully
✅ Judgeval imported successfully
✅ FastAPI imported successfully  
✅ CrewAI imported successfully
✅ Server is running!
Health: healthy, OpenAI: True
✅ API endpoint is working
📝 Generating answers...
✅ Answer generation completed
Number of answers generated: 20
⚖️ Running Judgeval evaluation...
✅ Judgeval completed successfully
✅ All answers passed Judgeval evaluation.
```

### Failed Run Example
```
❌ Some answers failed the evaluation!
Failed criteria details:
question,kid_friendly,uses_analogy,factually_correct
"What is a black hole?",YES,NO,YES
```

## 🔄 Triggering Tests

### Automatic Triggers
- Push to `main` branch
- Pull request to `main` branch

### Manual Trigger
1. Go to https://github.com/nishantsingh-ds/pikipedia/actions
2. Click "WonderBot CI" workflow
3. Click "Run workflow" button

## 📈 Monitoring & Alerts

### Slack Integration
- **Success**: Green checkmark notification
- **Failure**: Red X notification with details
- **Webhook**: Configure `SLACK_WEBHOOK_URL` secret

### GitHub Status Badge (Optional)
Add to README.md:
```markdown
![CI Status](https://github.com/nishantsingh-ds/pikipedia/workflows/WonderBot%20CI/badge.svg)
```

## 🚨 Emergency Debugging

### View Recent Logs
```bash
# Get latest run ID
RUN_ID=$(curl -s "https://api.github.com/repos/nishantsingh-ds/pikipedia/actions/runs?per_page=1" | python3 -c "import sys, json; print(json.load(sys.stdin)['workflow_runs'][0]['id'])")

# Check job details  
curl -s "https://api.github.com/repos/nishantsingh-ds/pikipedia/actions/runs/$RUN_ID/jobs"
```

### Local Reproduction
```bash
# Reproduce the CI steps locally
pip install -r requirements.txt
pip install judgeval requests
uvicorn src.kidapp.api:app --host 0.0.0.0 --port 8000 &
sleep 10
python generate_answers.py
judgeval evaluate --input wonderbot_outputs.csv --criteria criteria.yaml --output judgeval_results.csv
```

## ✅ Success Checklist

- [ ] ✅ All dependencies install without errors
- [ ] ✅ Server starts and health check passes  
- [ ] ✅ OPENAI_API_KEY is configured and valid
- [ ] ✅ All 20 test questions generate answers
- [ ] ✅ Judgeval runs without errors
- [ ] ✅ All answers pass quality criteria
- [ ] ✅ Slack notifications work (if configured)

---

**Need Help?** Check the GitHub Actions logs for detailed error messages and troubleshooting information.