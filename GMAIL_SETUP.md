# Gmail SMTP Setup Guide

## 🚀 Free Email Service Using Gmail SMTP

Gmail SMTP is completely free and reliable for sending emails from your application.

## 📋 Prerequisites

- Gmail account
- 2-Factor Authentication enabled on your Gmail

## 🔧 Step 1: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click **2-Step Verification**
3. Follow the setup process
4. **This is required** for App Passwords

## 🔑 Step 2: Generate App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click **App passwords** (under 2-Step Verification)
3. Select **Mail** and **Other (Custom name)**
4. Enter name: "Assignment System"
5. Click **Generate**
6. **Copy the 16-character password** (like: `abcd efgh ijkl mnop`)

## ⚙️ Step 3: Configure Your App

Use these settings in your application:

```python
# Gmail SMTP Configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your_email@gmail.com'  # Your Gmail address
MAIL_PASSWORD = 'your_app_password'      # The 16-character app password
MAIL_DEFAULT_SENDER = 'your_email@gmail.com'
```

## 🧪 Step 4: Test Your Setup

Run the test script to verify everything works:

```bash
python test_gmail_smtp.py
```

## ✅ Benefits of Gmail SMTP

- ✅ **Completely FREE**
- ✅ **No payment required**
- ✅ **Reliable delivery**
- ✅ **Works with any Gmail account**
- ✅ **Professional appearance**
- ✅ **No daily limits for personal use**

## 🔒 Security Notes

- App passwords are safer than your main password
- You can revoke app passwords anytime
- Each app gets its own unique password
- 2FA must be enabled (good security practice)

## 🚨 Troubleshooting

**"Less secure app access" error:**
- Make sure you're using an App Password, not your regular password
- Ensure 2-Factor Authentication is enabled

**"Authentication failed" error:**
- Double-check your Gmail address
- Verify the App Password is correct (16 characters, no spaces)

**"Connection refused" error:**
- Check your internet connection
- Verify SMTP settings are correct
