# PlagiarismCheck.org API Integration Guide

This guide will help you set up professional plagiarism detection using PlagiarismCheck.org API.

## 🌟 Benefits of Using PlagiarismCheck.org API

- ✅ **Professional Grade Detection**: Industry-standard plagiarism detection
- ✅ **Comprehensive Database**: Checks against billions of web pages and academic papers
- ✅ **Real-time Results**: Fast and accurate plagiarism reports
- ✅ **Detailed Reports**: Comprehensive similarity analysis with sources
- ✅ **API Integration**: Seamless integration with your application
- ✅ **Reliable Service**: Professional-grade infrastructure

## 📋 Prerequisites

1. **PlagiarismCheck.org Account**: You need an account with PlagiarismCheck.org
2. **API Access**: Request API access from their support team
3. **API Token**: Obtain your group token for API authentication

## 🔧 Step 1: Get API Access

### 1.1 Register with PlagiarismCheck.org

1. Go to [PlagiarismCheck.org](https://plagiarismcheck.org/)
2. Click "Sign Up" or "Register"
3. Create your account with your institutional email
4. Verify your email address

### 1.2 Request API Access

1. **Contact Support**: Email their support team at support@plagiarismcheck.org
2. **Request API Token**: Ask for API access for your educational institution
3. **Provide Details**: 
   - Your institution name
   - Expected usage volume
   - Contact information
4. **Wait for Response**: They will provide you with a group token

### 1.3 Get Your API Token

Once approved, you'll receive:
- **Group Token**: Your unique API authentication token
- **API Documentation**: Detailed integration guide
- **Usage Limits**: Information about your plan limits

## ⚙️ Step 2: Configure Your Application

### 2.1 Environment Variables

Set these environment variables in your deployment:

```bash
# PlagiarismCheck.org API Configuration
USE_PLAGIARISM_CHECK_API=true
PLAGIARISM_CHECK_API_TOKEN=your_group_token_here
```

### 2.2 For Local Development

Create a `.env` file in your project root:

```bash
# PlagiarismCheck.org API Configuration
USE_PLAGIARISM_CHECK_API=true
PLAGIARISM_CHECK_API_TOKEN=your_group_token_here
```

### 2.3 For Railway Deployment

In your Railway dashboard:

1. Go to your project
2. Click on "Variables" tab
3. Add these variables:
   - `USE_PLAGIARISM_CHECK_API` = `true`
   - `PLAGIARISM_CHECK_API_TOKEN` = `your_actual_token`

## 🧪 Step 3: Test the Integration

### 3.1 Run the Test Script

```bash
python test_plagiarism_api.py
```

### 3.2 Expected Output

```
🔍 Testing PlagiarismCheck.org API Integration
============================================================

📋 API Configuration:
USE_PLAGIARISM_CHECK_API: True
PLAGIARISM_CHECK_API_TOKEN: SET
PLAGIARISM_CHECK_API_URL: https://plagiarismcheck.org/api/org/text/check/

🧪 Testing API Submission:
Content length: 500 characters
Author: Test User (test@example.com)

✅ API submission successful!
Check ID: 12345
Status: submitted
```

## 🔄 How It Works

### 3.1 Submission Process

1. **Student Submits Assignment**: File is uploaded to your system
2. **Content Extraction**: System extracts text from the uploaded file
3. **API Submission**: Text is sent to PlagiarismCheck.org API
4. **Check ID Received**: API returns a unique check ID
5. **Status Tracking**: System tracks the check status

### 3.2 Report Retrieval

1. **Periodic Checks**: System periodically checks for completed reports
2. **Report Download**: When ready, report is downloaded from API
3. **Score Update**: Plagiarism score is updated in your database
4. **Notification**: Lecturer is notified of the results

## 📊 API Response Format

### 3.1 Submission Response

```json
{
  "check_id": "12345",
  "status": "submitted",
  "message": "Plagiarism check submitted successfully"
}
```

### 3.2 Report Response

```json
{
  "check_id": "12345",
  "status": "completed",
  "plagiarism_score": 15.5,
  "sources": [
    {
      "url": "https://example.com/source1",
      "similarity": 8.2,
      "title": "Source Title"
    }
  ],
  "report_url": "https://plagiarismcheck.org/report/12345"
}
```

## 🎯 Integration Features

### 3.1 Automatic Fallback

- **API Available**: Uses PlagiarismCheck.org API
- **API Unavailable**: Falls back to local TF-IDF detection
- **Seamless Experience**: Users don't notice the difference

### 3.2 Status Tracking

- **Submitted**: Check has been submitted to API
- **Processing**: Check is being processed
- **Completed**: Report is ready
- **Error**: Check failed (falls back to local)

### 3.3 Report Storage

- **Check ID**: Stored in database for later retrieval
- **Report Data**: Full report stored when available
- **Source Links**: Links to original sources provided

## 💰 Pricing Information

### 3.1 Free Tier

- Limited checks per month
- Basic plagiarism detection
- Standard report format

### 3.2 Paid Plans

- **Educational Plans**: Special pricing for institutions
- **Volume Discounts**: Better rates for higher usage
- **Premium Features**: Advanced reporting and analytics

### 3.3 Contact for Pricing

- Email: sales@plagiarismcheck.org
- Phone: Check their website for current contact info
- Custom Plans: Available for large institutions

## 🔒 Security & Privacy

### 3.1 Data Protection

- **Encrypted Transmission**: All API calls use HTTPS
- **Secure Storage**: Reports stored securely
- **Privacy Compliance**: GDPR and FERPA compliant

### 3.2 Token Security

- **Environment Variables**: Never hardcode tokens
- **Access Control**: Limit who can access API settings
- **Regular Rotation**: Rotate tokens periodically

## 🚨 Troubleshooting

### 3.1 Common Issues

**"API not configured" Error:**
- Check environment variables are set
- Verify `USE_PLAGIARISM_CHECK_API=true`
- Ensure `PLAGIARISM_CHECK_API_TOKEN` is set

**"Authentication failed" Error:**
- Verify your API token is correct
- Check if token has expired
- Contact PlagiarismCheck.org support

**"Request timeout" Error:**
- Check internet connection
- Verify API endpoint is accessible
- Try again after a few minutes

### 3.2 Getting Help

1. **Check Logs**: Look at application logs for detailed errors
2. **Test API**: Use the test script to verify configuration
3. **Contact Support**: Reach out to PlagiarismCheck.org support
4. **Fallback Mode**: System will use local detection if API fails

## 📈 Monitoring & Analytics

### 3.1 Usage Tracking

- **API Calls**: Monitor number of API requests
- **Success Rate**: Track successful vs failed requests
- **Response Times**: Monitor API performance
- **Cost Tracking**: Keep track of API usage costs

### 3.2 Performance Optimization

- **Caching**: Cache reports to reduce API calls
- **Batch Processing**: Process multiple checks together
- **Rate Limiting**: Respect API rate limits
- **Error Handling**: Implement proper error handling

## 🎉 Benefits for Your Institution

### 3.1 For Students

- **Fair Assessment**: Accurate plagiarism detection
- **Learning Tool**: Helps students understand originality
- **Immediate Feedback**: Quick results on submissions

### 3.2 For Lecturers

- **Time Saving**: Automated plagiarism detection
- **Detailed Reports**: Comprehensive similarity analysis
- **Source Identification**: Know exactly what was copied
- **Confidence**: Trust in assessment accuracy

### 3.3 For Administrators

- **Academic Integrity**: Maintain high standards
- **Compliance**: Meet institutional requirements
- **Analytics**: Track plagiarism trends
- **Cost Effective**: Professional service at reasonable cost

---

## 📞 Support Contacts

- **PlagiarismCheck.org Support**: support@plagiarismcheck.org
- **API Documentation**: https://plagiarismcheck.org/for-developers/
- **Sales Inquiries**: sales@plagiarismcheck.org

---

**Note**: This integration provides professional-grade plagiarism detection while maintaining a seamless user experience with automatic fallback to local detection when needed.
