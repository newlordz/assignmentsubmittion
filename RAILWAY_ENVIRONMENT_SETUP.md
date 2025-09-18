# 🚀 Railway Environment Variables Setup Guide

## 📋 Complete List of Required Environment Variables

Based on your Flask app configuration, here are ALL the environment variables you need to set in Railway:

### 🔐 **CRITICAL - Must Set These:**

```bash
# Application Security
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random-32-chars-minimum

# Database (Railway will auto-set this, but you can override)
DATABASE_URL=postgresql://username:password@host:port/database

# Flask Environment
FLASK_ENV=production
FLASK_DEBUG=False
```

### 📧 **Email Configuration (Gmail SMTP):**

```bash
# Gmail SMTP Settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=enochessel5@gmail.com
MAIL_PASSWORD=xgaq ceff cwlh aabb
MAIL_DEFAULT_SENDER=E-Assignment.edu.gh <enochessel5@gmail.com>
MAIL_SUPPRESS_SEND=False
```

### 🔍 **Plagiarism Detection (Optional):**

```bash
# PlagiarismCheck.org API (if you want to use it)
PLAGIARISM_CHECK_API_TOKEN=nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4
USE_PLAGIARISM_CHECK_API=True
PLAGIARISM_CHECK_API_URL=https://plagiarismcheck.org/api/org/text/check/

# Alternative APIs (optional)
QUETEXT_API_KEY=
USE_QUETEXT_API=False
DUPLICHECKER_API_KEY=
USE_DUPLICHECKER_API=False
```

### 📨 **SendGrid (Alternative to Gmail - Optional):**

```bash
# SendGrid Configuration (if you prefer SendGrid over Gmail)
SENDGRID_API_KEY=
USE_SENDGRID=False
SENDGRID_FROM_EMAIL=noreply@university.edu
```

## 🛠️ **How to Set Environment Variables in Railway:**

### **Step 1: Access Railway Dashboard**
1. Go to [railway.app](https://railway.app)
2. Sign in to your account
3. Select your project

### **Step 2: Navigate to Variables**
1. Click on your **service** (not the project)
2. Go to the **Variables** tab
3. Click **"New Variable"**

### **Step 3: Add Each Variable**
For each variable above:
1. Click **"New Variable"**
2. Enter the **Variable Name** (e.g., `SECRET_KEY`)
3. Enter the **Value** (e.g., `your-super-secret-key-here`)
4. Click **"Add"**

### **Step 4: Verify All Variables**
Make sure you have added ALL these variables:

✅ **Required Variables:**
- `SECRET_KEY`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`

✅ **Optional but Recommended:**
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_SUPPRESS_SEND`
- `PLAGIARISM_CHECK_API_TOKEN`
- `USE_PLAGIARISM_CHECK_API`

## 🔧 **Step-by-Step Railway Setup:**

### **1. Generate a Strong SECRET_KEY:**
```bash
# Use this command to generate a secure secret key:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### **2. Set Your Gmail Credentials:**
```bash
MAIL_USERNAME=enochessel5@gmail.com
MAIL_PASSWORD=xgaq ceff cwlh aabb
MAIL_DEFAULT_SENDER=E-Assignment.edu.gh <enochessel5@gmail.com>
```

### **3. Configure Plagiarism Detection:**
```bash
PLAGIARISM_CHECK_API_TOKEN=nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4
USE_PLAGIARISM_CHECK_API=True
```

## 🚨 **Common Issues & Solutions:**

### **Issue 1: Email Not Working**
**Problem:** Emails not being sent
**Solution:** Check these variables are set correctly:
- `MAIL_USERNAME` (your Gmail address)
- `MAIL_PASSWORD` (your Gmail App Password - no spaces)
- `MAIL_DEFAULT_SENDER` (sender name and email)

### **Issue 2: Plagiarism Detection Not Working**
**Problem:** Plagiarism API not responding
**Solution:** 
- Set `USE_PLAGIARISM_CHECK_API=True`
- Verify `PLAGIARISM_CHECK_API_TOKEN` is correct
- Contact PlagiarismCheck.org support to activate your token

### **Issue 3: App Crashes on Startup**
**Problem:** Missing required variables
**Solution:** Ensure `SECRET_KEY` is set with a strong value

### **Issue 4: Database Issues**
**Problem:** Database connection errors
**Solution:** Railway auto-sets `DATABASE_URL` - don't override unless needed

## 📱 **Quick Setup Commands:**

### **For Railway CLI (if you have it installed):**
```bash
# Set critical variables
railway variables set SECRET_KEY="your-secret-key-here"
railway variables set MAIL_USERNAME="enochessel5@gmail.com"
railway variables set MAIL_PASSWORD="xgaq ceff cwlh aabb"
railway variables set MAIL_DEFAULT_SENDER="E-Assignment.edu.gh <enochessel5@gmail.com>"
railway variables set PLAGIARISM_CHECK_API_TOKEN="nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4"
railway variables set USE_PLAGIARISM_CHECK_API="True"
```

## ✅ **Verification Checklist:**

After setting all variables, verify:

- [ ] `SECRET_KEY` is set (32+ characters)
- [ ] `MAIL_USERNAME` is your Gmail address
- [ ] `MAIL_PASSWORD` is your Gmail App Password (no spaces)
- [ ] `MAIL_DEFAULT_SENDER` includes your sender name
- [ ] `PLAGIARISM_CHECK_API_TOKEN` is set (if using API)
- [ ] `USE_PLAGIARISM_CHECK_API` is set to `True` (if using API)
- [ ] All variables are saved in Railway dashboard

## 🎯 **Priority Order:**

**Set these FIRST (Critical):**
1. `SECRET_KEY`
2. `MAIL_USERNAME`
3. `MAIL_PASSWORD`
4. `MAIL_DEFAULT_SENDER`

**Then add these (Important):**
5. `PLAGIARISM_CHECK_API_TOKEN`
6. `USE_PLAGIARISM_CHECK_API`

**Finally (Optional):**
7. Other email settings
8. Alternative API keys

## 🚀 **After Setting Variables:**

1. **Redeploy** your app (Railway will auto-redeploy when you add variables)
2. **Test email functionality** by registering a new user
3. **Test plagiarism detection** by submitting an assignment
4. **Check logs** in Railway dashboard for any errors

---

**Need Help?** Check Railway logs in the dashboard for specific error messages!
