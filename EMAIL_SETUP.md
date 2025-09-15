# Email Service Setup Guide

This guide will help you configure the email service for the E-Assignment Submission System.

## Features

The email service provides automated notifications for:

- ✅ **Welcome emails** for new users
- ✅ **New assignment notifications** to students
- ✅ **Submission notifications** to lecturers
- ✅ **Grade notifications** to students
- ✅ **Deadline reminders** to students

## Configuration

### Environment Variables

Set these environment variables in your deployment platform (Railway, Heroku, etc.):

```bash
# Email Server Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false

# Email Credentials
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Sender Information
MAIL_DEFAULT_SENDER=noreply@university.edu

# Development/Testing
MAIL_SUPPRESS_SEND=false  # Set to true to disable email sending
```

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password as `MAIL_PASSWORD`

3. **Configure Environment Variables**:
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-character-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

### Other Email Providers

#### Outlook/Hotmail
```bash
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

#### Yahoo Mail
```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

#### Custom SMTP Server
```bash
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
```

## Testing Email Service

### Local Testing

1. **Set up environment variables** in a `.env` file:
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   MAIL_SUPPRESS_SEND=false
   ```

2. **Test email sending**:
   ```python
   from app import app, send_email
   
   with app.app_context():
       send_email(
           to_email='test@example.com',
           subject='Test Email',
           template='welcome.html',
           user={'first_name': 'Test', 'last_name': 'User'}
       )
   ```

### Production Testing

1. **Register a new user** - should receive welcome email
2. **Create a new assignment** - students should receive notifications
3. **Submit an assignment** - lecturer should receive notification
4. **Grade a submission** - student should receive grade notification

## Email Templates

The system includes professionally designed email templates:

- `welcome.html` - Welcome email for new users
- `new_assignment.html` - New assignment notifications
- `new_submission.html` - Submission notifications for lecturers
- `grade_notification.html` - Grade notifications for students
- `deadline_reminder.html` - Deadline reminder emails

### Customizing Templates

You can customize email templates by editing files in `templates/emails/`:

1. **Modify styling** - Update CSS in the `<style>` section
2. **Change content** - Update HTML content and text
3. **Add branding** - Include your institution's logo and colors
4. **Modify layout** - Adjust the email structure

## Troubleshooting

### Common Issues

1. **"Authentication failed" error**:
   - Check your email credentials
   - Ensure 2FA is enabled and app password is used
   - Verify SMTP settings

2. **"Connection refused" error**:
   - Check MAIL_SERVER and MAIL_PORT settings
   - Ensure firewall allows SMTP connections
   - Try different port (465 for SSL, 587 for TLS)

3. **Emails not sending**:
   - Check MAIL_SUPPRESS_SEND is set to false
   - Verify all required environment variables are set
   - Check application logs for error messages

4. **Emails going to spam**:
   - Use a professional sender email address
   - Add SPF, DKIM, and DMARC records
   - Avoid spam trigger words in subject lines

### Debug Mode

Enable debug logging by setting:
```bash
FLASK_ENV=development
```

This will show detailed email sending logs in the console.

### Testing Without Sending

Set `MAIL_SUPPRESS_SEND=true` to test email functionality without actually sending emails. The system will log email content instead.

## Security Considerations

1. **Never commit email credentials** to version control
2. **Use environment variables** for all sensitive information
3. **Use app passwords** instead of main account passwords
4. **Enable 2FA** on email accounts
5. **Regularly rotate** email passwords

## Performance

- Emails are sent asynchronously to avoid blocking the web application
- Failed email sends are logged but don't affect user experience
- Email templates are cached for better performance

## Monitoring

Monitor email delivery by:

1. **Checking application logs** for email send status
2. **Monitoring bounce rates** in your email provider dashboard
3. **Tracking user engagement** with email notifications
4. **Setting up alerts** for email service failures

## Support

If you encounter issues with the email service:

1. Check the troubleshooting section above
2. Review application logs for error messages
3. Test with a simple email first
4. Verify your email provider's SMTP settings
5. Contact your email provider's support if needed

---

**Note**: The email service is designed to be robust and fail gracefully. If emails fail to send, users will still receive in-app notifications, ensuring they don't miss important updates.
