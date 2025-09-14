# Railway Deployment Guide

## 🚀 Deploying to Railway

This guide will help you deploy your E-Assignment Submission System to Railway.

### Prerequisites
- GitHub repository with your code
- Railway account (free tier available)
- Basic understanding of environment variables

### Step 1: Prepare Your Repository

Your repository should include these files:
- ✅ `app.py` - Main Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Railway deployment configuration
- ✅ `railway.json` - Railway-specific settings
- ✅ `runtime.txt` - Python version specification
- ✅ All templates and static files

### Step 2: Deploy to Railway

1. **Go to Railway**: Visit [railway.app](https://railway.app) and sign up/login
2. **Connect GitHub**: Link your GitHub account to Railway
3. **Create New Project**: Click "New Project" → "Deploy from GitHub repo"
4. **Select Repository**: Choose `newlordz/assignmentsubmittion`
5. **Deploy**: Railway will automatically detect it's a Python app and start building

### Step 3: Configure Environment Variables

In your Railway project dashboard, go to **Variables** tab and add:

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=sqlite:///assignment_system.db
FLASK_ENV=production
```

**Important**: 
- Generate a strong SECRET_KEY (32+ characters)
- Railway will automatically set PORT and other variables

### Step 4: Database Setup

Railway will automatically:
- Create a PostgreSQL database (recommended for production)
- Set the DATABASE_URL environment variable
- Handle database migrations

### Step 5: Custom Domain (Optional)

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed

### Step 6: Monitor Your Deployment

- **Logs**: View real-time logs in Railway dashboard
- **Metrics**: Monitor CPU, memory, and network usage
- **Health Checks**: Railway automatically monitors your app

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Yes | - |
| `DATABASE_URL` | Database connection string | Yes | sqlite:///assignment_system.db |
| `FLASK_ENV` | Flask environment | No | development |
| `PORT` | Port number | No | 5000 |

### File Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment command
├── railway.json          # Railway configuration
├── runtime.txt           # Python version
├── static/               # CSS, JS, images
├── templates/            # HTML templates
└── instance/             # Database files
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct dependencies
   - Ensure Python version in `runtime.txt` is supported

2. **App Crashes on Startup**
   - Check environment variables are set correctly
   - Verify SECRET_KEY is set
   - Check logs for specific error messages

3. **Database Issues**
   - Ensure DATABASE_URL is set correctly
   - Check if database tables are created properly

4. **Static Files Not Loading**
   - Verify static folder structure
   - Check file paths in templates

### Getting Help

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Create an issue in your repository

## 📊 Post-Deployment

### Admin Access
- Default admin credentials: `admin` / `admin123`
- **Change these immediately** after first login!

### Features Available
- ✅ User registration and authentication
- ✅ Assignment creation and management
- ✅ File submission and grading
- ✅ Admin dashboard and analytics
- ✅ Report generation
- ✅ Plagiarism detection
- ✅ Notification system

### Security Recommendations
1. Change default admin password
2. Use strong SECRET_KEY
3. Enable HTTPS (Railway provides this automatically)
4. Regularly update dependencies
5. Monitor logs for suspicious activity

## 🎉 Success!

Your E-Assignment Submission System is now live on Railway! 

**Next Steps:**
- Test all functionality
- Create additional user accounts
- Customize the system for your needs
- Set up monitoring and backups
