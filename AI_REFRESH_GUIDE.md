# 🤖 DidactIA AI Functionality Refresh Guide

## 🔍 Current Situation
Your current Gemini API key `AIzaSyAEEbJICNYIxxqUQiUpfFfH03UPQ_h0pSg` has exceeded its free tier quota of 50 requests per day.

## 🚀 Quick Solutions (Choose One)

### Option 1: Get a New Free API Key (Recommended)
1. **Go to Google AI Studio**: https://aistudio.google.com/
2. **Sign in** with a different Google account (or create new one)
3. **Get API Key**: Click "Get API Key" → "Create API Key" 
4. **Copy the new key** (starts with `AIzaSy...`)
5. **Update your `.env` file** (see instructions below)

### Option 2: Wait for Quota Reset
- Your current quota will reset in ~24 hours
- This is automatic but requires waiting

### Option 3: Upgrade Current Key to Paid Plan
1. **Visit**: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com
2. **Enable billing** on your Google Cloud project
3. **Current key will work** immediately with higher limits

## 🔧 How to Update API Key

### Step 1: Update .env File
Replace line 22 in your `.env` file:
```bash
# OLD (quota exceeded)
GEMINI_API_KEY=AIzaSyAEEbJICNYIxxqUQiUpfFfH03UPQ_h0pSg

# NEW (replace with your new key)
GEMINI_API_KEY=YOUR_NEW_API_KEY_HERE
```

### Step 2: Restart Django Server
```bash
# Stop current server (Ctrl+C if running)
# Then restart:
python manage.py runserver
```

## 🧪 Test AI Functionality

### Quick Test (After updating API key)
```bash
python test_ai_refresh.py
```

This will test:
- ✅ API connection
- ✅ Quiz generation  
- ✅ Exam generation

## 🚀 Three Easy Methods to Refresh

### Method 1: Automatic PowerShell Script (Easiest)
```powershell
# Run this and follow prompts
.\update_api_key.ps1
```

### Method 2: Manual Edit
1. Open `.env` file in any text editor
2. Find line 22: `GEMINI_API_KEY=AIzaSyAEEbJICNYIxxqUQiUpfFfH03UPQ_h0pSg`
3. Replace with your new key: `GEMINI_API_KEY=YOUR_NEW_KEY`
4. Save file
5. Restart Django server

### Method 3: Command Line (PowerShell)
```powershell
# Replace YOUR_NEW_KEY with actual key
$newKey = "YOUR_NEW_KEY"
$env = Get-Content .env -Raw
$env = $env -replace "GEMINI_API_KEY=.*", "GEMINI_API_KEY=$newKey"
Set-Content .env -Value $env
```

## 🎯 Expected Results

After updating the key, your test should show:
```
🚀 DIDACTIA AI REFRESH TEST
==================================================
🤖 TESTING AI CONNECTION
========================================
🔑 API Key: AIzaSyCs4cvAHvzCTI_4...
📡 Testing API connection...
✅ AI CONNECTION SUCCESSFUL!
🎉 Response: Hello, DidactIA is working!

📝 TESTING QUIZ GENERATION
========================================
✅ QuizGenerator imported successfully
🎯 Generating sample quiz...
✅ QUIZ GENERATION SUCCESSFUL!
📊 Generated 2 questions
📝 Sample Question: What is a key characteristic of cloud computing?

📋 TESTING EXAM GENERATION
========================================
✅ ExamGenerator imported successfully
🎯 Generating sample exam...
✅ EXAM GENERATION SUCCESSFUL!
📊 Generated 2 section(s)
📝 Total questions: 3

==================================================
📊 TEST RESULTS SUMMARY
==================================================
AI Connection        ✅ PASS
Quiz Generation      ✅ PASS
Exam Generation      ✅ PASS

🎯 Overall: 3/3 tests passed
🎉 ALL AI FUNCTIONALITY RESTORED!
🚀 Your DidactIA app is ready for AI-powered content generation!
==================================================
```

## 🔥 Ready to Use Features

Once AI is refreshed, you can immediately use:

### In the Web Interface:
- 📝 **AI Generator** → Create Quiz/Exam from uploaded files
- 🎯 **Generate Questions** from any content
- 📊 **Multi-language Support** (English, French, Spanish, etc.)
- 🔄 **Different Difficulty Levels** (Easy, Medium, Hard)
- 📋 **Multiple Question Types** (Multiple Choice, True/False, Short Answer)

### Programmatically:
```python
from ai_generator.services import QuizGenerator, ExamGenerator

# Generate quiz
generator = QuizGenerator()
quiz = generator.generate_quiz(
    content="Your educational content here",
    language="en",
    num_questions=10,
    difficulty="medium"
)

# Generate exam  
exam_gen = ExamGenerator()
exam = exam_gen.generate_exam(
    content="Your content",
    num_questions=25,
    duration=120  # minutes
)
```

## ❓ Troubleshooting

### If test still fails:

**"Quota exceeded"** → Need different Google account for API key
**"Invalid API key"** → Check key format (should start with `AIzaSy`)
**"Permission denied"** → Enable Gemini API in Google Cloud Console
**"Import error"** → Run `pip install google-generativeai`

### Common Solutions:
1. **Clear browser cache** and refresh
2. **Restart Django server** completely
3. **Check .env file** was saved properly
4. **Verify API key** in Google AI Studio

## 🎉 Success!

Once you see all tests passing, your DidactIA application is **100% functional** with full AI capabilities restored!

You can now:
- ✅ Generate quizzes from any content
- ✅ Create comprehensive exams  
- ✅ Use all 12 supported languages
- ✅ Export everything to PDF/DOCX
- ✅ Enjoy the complete educational platform!
