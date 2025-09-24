# 🔑 Quick Guide: Create New Google Cloud API Key

## 🚀 FASTEST SOLUTION: New Google Cloud Project

### Step 1: Create New Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" dropdown at the top
3. Click "NEW PROJECT" 
4. Enter project name: `ai-exam-generator-2` (or any unique name)
5. Click "CREATE"

### Step 2: Enable Gemini API
1. In the new project, go to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
2. Search for "Generative Language API" 
3. Click on it and press "ENABLE"

### Step 3: Create API Key
1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "CREATE CREDENTIALS" > "API key"
3. Copy the generated API key
4. **IMPORTANT**: Click "RESTRICT KEY" and select "Generative Language API" for security

### Step 4: Update Your Project
Replace the API key in your `.env` file:
```
GEMINI_API_KEY=YOUR_NEW_API_KEY_HERE
```

### Step 5: Test
Run your project - you now have a fresh 50 requests/day quota!

---

## 💰 LONG-TERM SOLUTION: Enable Billing

### Why Enable Billing?
- **Free Tier**: 50 requests/day 
- **Tier 1 (Billing)**: 1,000-4,000 requests/minute!
- Cost: Usually $0.00-0.02 per request for typical usage

### How to Enable Billing:
1. Go to [AI Studio](https://aistudio.google.com/app/apikey)
2. Find your project and click "Upgrade"
3. Follow the billing setup (requires credit card)
4. **Benefit**: Massive quota increase instantly

---

## 📊 Current Quota Status

**Free Tier Limits:**
- Gemini 1.5 Flash: 15 RPM, 250K TPM, **50 RPD** ⬅️ You hit this
- Gemini 2.5 Flash: 10 RPM, 250K TPM, 250 RPD

**Tier 1 Limits (with billing):**
- Gemini 1.5 Flash: 2,000 RPM, 4M TPM, unlimited daily
- Gemini 2.5 Flash: 1,000 RPM, 1M TPM, 10,000 RPD

---

## ⏰ Quota Reset Time
Daily quotas reset at **midnight Pacific Time** (PST/PDT)

Current time: Check [WorldClock](https://www.worldclock.com/timezone/pst)

---

## 🔧 Your Enhanced Error Handling

I've already updated your `ai_generator/services.py` with:
- ✅ Automatic retry logic
- ✅ Quota-aware error messages  
- ✅ Exponential backoff for temporary errors
- ✅ Helpful user messages when quota exceeded

Your app will now gracefully handle quota issues and provide clear feedback to users!