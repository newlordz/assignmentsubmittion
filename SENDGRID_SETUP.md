# SendGrid Email Service Setup Guide

This guide will help you set up SendGrid to send real emails to Gmail and other email providers.

## Why SendGrid?

- ✅ **Free Tier**: 100 emails/day forever (3,000/month)
- ✅ **Reliable Delivery**: 99%+ delivery rate to Gmail
- ✅ **No SMTP Issues**: Uses API instead of SMTP
- ✅ **Professional Service**: Used by major companies
- ✅ **Easy Setup**: Just need an API key

## Step 1: Create SendGrid Account

1. **Go to SendGrid**: https://sendgrid.com/
2. **Click "Start for Free"**
3. **Sign up** with your email address
4. **Verify your email** (check your inbox)

## Step 2: Get API Key

1. **Login to SendGrid Dashboard**
2. **Go to Settings → API Keys**
3. **Click "Create API Key"**
4. **Choose "Restricted Access"**
5. **Give it a name**: "Assignment System"
6. **Set permissions**:
   - ✅ Mail Send: Full Access
   - ❌ Everything else: No Access
7. **Click "Create & View"**
8. **Copy the API key** (starts with `SG.`)

## Step 3: Verify Sender Identity

### Option A: Single Sender Verification (Easiest)

1. **Go to Settings → Sender Authentication**
2. **Click "Verify a Single Sender"**
3. **Fill out the form**:
   - From Name: Your University Name
   - From Email: your-email@university.edu (or your Gmail)
   - Reply To: your-email@university.edu
   - Company Address: Your university address
4. **Click "Create"**
5. **Check your email** and click the verification link

### Option B: Domain Authentication (For Production)

1. **Go to Settings → Sender Authentication**
2. **Click "Authenticate Your Domain"**
3. **Enter your domain** (e.g., university.edu)
4. **Follow DNS setup instructions**

## Step 4: Configure Your Application

### For Local Testing:

Create a `.env` file in your project root:
```bash
# SendGrid Configuration
USE_SENDGRID=true
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=your-verified-email@university.edu

# Disable other email methods
MAIL_SUPPRESS_SEND=false
```

### For Railway Deployment:

Add these environment variables in Railway:
```bash
USE_SENDGRID=true
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=your-verified-email@university.edu
MAIL_SUPPRESS_SEND=false
```

## Step 5: Test the Setup

### Install SendGrid:
```bash
pip install sendgrid==6.10.0
```

### Test Email Sending:
```bash
# Test with SendGrid
$env:USE_SENDGRID="true"
$env:SENDGRID_API_KEY="SG.your-api-key-here"
$env:SENDGRID_FROM_EMAIL="your-email@university.edu"
$env:MAIL_SUPPRESS_SEND="false"

python test_email.py
```

## Step 6: Test with Real Emails

1. **Start your app**: `python app.py`
2. **Register a new user** with your real Gmail address
3. **Check your Gmail inbox** for the welcome email
4. **Create an assignment** as a lecturer
5. **Check Gmail** for assignment notifications

## Troubleshooting

### Common Issues:

1. **"Invalid API Key"**:
   - Check that your API key starts with `SG.`
   - Make sure you copied the full key
   - Regenerate the key if needed

2. **"Sender not verified"**:
   - Complete the sender verification process
   - Check your email for verification link
   - Use the exact email address you verified

3. **"Emails not delivered"**:
   - Check SendGrid dashboard for delivery stats
   - Look in Gmail spam folder
   - Verify sender authentication is complete

4. **"Rate limit exceeded"**:
   - Free tier allows 100 emails/day
   - Check your usage in SendGrid dashboard
   - Wait until next day or upgrade plan

### Check SendGrid Dashboard:

1. **Activity Feed**: See all sent emails
2. **Statistics**: View delivery rates
3. **Suppressions**: Check blocked emails
4. **API Keys**: Manage your keys

## Alternative Services

If SendGrid doesn't work for you, here are other options:

### Mailgun (5,000 emails/month free)
```bash
# Add to requirements.txt
requests==2.31.0

# Environment variables
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
USE_MAILGUN=true
```

### Resend (3,000 emails/month free)
```bash
# Add to requirements.txt
resend==0.6.0

# Environment variables
RESEND_API_KEY=your-resend-api-key
USE_RESEND=true
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Use restricted permissions** for API keys
5. **Monitor usage** in SendGrid dashboard

## Cost Information

### SendGrid Free Tier:
- ✅ 100 emails/day (3,000/month)
- ✅ Forever free
- ✅ Full API access
- ✅ Email templates
- ✅ Delivery tracking

### Paid Plans (if needed):
- **Essentials**: $19.95/month for 50,000 emails
- **Pro**: $89.95/month for 100,000 emails
- **Premier**: Custom pricing

## Support

- **SendGrid Documentation**: https://docs.sendgrid.com/
- **SendGrid Support**: Available in dashboard
- **Community Forum**: https://community.sendgrid.com/

---

**Note**: SendGrid is the most reliable option for sending emails to Gmail. The free tier should be more than enough for your assignment system!
