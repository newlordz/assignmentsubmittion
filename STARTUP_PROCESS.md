# 🚀 E-Assignment System Startup Process

## 📋 Complete Startup Sequence

When you run `python app.py` in the terminal, here's exactly what happens:

### **Phase 1: Import Dependencies (Lines 1-31)**
```
1. Flask framework and extensions
2. Database components (SQLAlchemy, Flask-Login)
3. Email components (Flask-Mail, SendGrid)
4. Security components (Werkzeug)
5. Data processing (pandas, numpy, scikit-learn)
6. Visualization (matplotlib, seaborn)
7. Background tasks (APScheduler)
8. File handling and utilities
```

### **Phase 2: Optional Integrations (Lines 33-39)**
```
✅ Try to import Dolos integration
   - If successful: DOLOS_AVAILABLE = True
   - If failed: DOLOS_AVAILABLE = False
   - Prints: "Dolos integration not available - using local plagiarism detection only"
```

### **Phase 3: Environment Configuration (Lines 41-47)**
```
📁 Load .env file
   - Read all environment variables
   - Set MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, etc.
   - Configure database URL
   - Set secret keys and API tokens
```

### **Phase 4: Flask App Initialization (Lines 49-89)**
```
🏗️ Create Flask application
   - Set SECRET_KEY for sessions
   - Configure database URI (SQLite with absolute path)
   - Set upload folder and file size limits
   - Configure email settings (Gmail SMTP)
   - Configure SendGrid (optional)
   - Configure plagiarism detection APIs
```

### **Phase 5: Database Setup (Lines 89-90)**
```
🗄️ Initialize SQLAlchemy
   - Connect to SQLite database
   - Set up database models
```

### **Phase 6: Email System Setup (Line 90)**
```
📧 Initialize Flask-Mail
   - Configure SMTP settings
   - Set up email templates
```

### **Phase 7: Authentication Setup (Lines 91-95)**
```
🔐 Initialize Flask-Login
   - Set login view
   - Configure session protection
   - Set remember cookie duration (30 days)
```

### **Phase 8: Dolos Integration (Lines 97-110)**
```
🔍 Initialize plagiarism detection
   - Try to create DolosIntegration instance
   - Check if Node.js is available
   - Print status: "✅ Dolos integration available" or "⚠️ Dolos integration not properly configured"
```

### **Phase 9: Background Scheduler (Lines 112-115)**
```
⏰ Start background scheduler
   - Initialize APScheduler
   - Start scheduler service
   - Print: "INFO:apscheduler.scheduler:Scheduler started"
```

### **Phase 10: Server Startup Logging (Lines 117-120)**
```
📝 Log server startup
   - Record startup timestamp
   - Print: "🚀 Server started at: [timestamp]"
   - Print: "📋 Session Management: Users will need to sign in again after server restart"
```

### **Phase 11: Database Initialization (Lines 122-200)**
```
🗄️ Initialize database tables and data
   - Create all database tables
   - Create admin user if not exists
   - Create demo accounts (students, lecturers)
   - Print: "🚀 Creating demo accounts..."
   - Print: "✅ Database initialization completed"
```

### **Phase 12: Background Jobs Setup (Lines 200+)**
```
⏰ Add scheduled jobs
   - Add deadline reminder job
   - Add overdue assignment check job
   - Print: "INFO:apscheduler.scheduler:Added job 'check_deadline_reminders'"
   - Print: "INFO:apscheduler.scheduler:Added job 'check_overdue_assignments'"
```

### **Phase 13: Route Registration (Lines 200-3075)**
```
🛣️ Register all application routes
   - Authentication routes (login, register, logout)
   - Assignment routes (create, submit, grade)
   - Admin routes (dashboard, user management)
   - API routes (plagiarism check, notifications)
   - Static file routes
```

### **Phase 14: Database Initialization Call (Line 3076)**
```
🔄 Call initialize_database()
   - This runs the database setup process
   - Creates tables and demo accounts
   - Handles any database errors
```

### **Phase 15: Server Launch (Lines 3078-3083)**
```
🌐 Start Flask development server
   - Get port from environment (default: 5000)
   - Set debug mode based on environment
   - Print: " * Serving Flask app 'app'"
   - Print: " * Debug mode: on"
   - Print: "INFO:werkzeug:WARNING: This is a development server..."
   - Print: " * Running on all addresses (0.0.0.0)"
   - Print: " * Running on http://127.0.0.1:5000"
   - Print: " * Running on http://[your-ip]:5000"
   - Print: "INFO:werkzeug:Press CTRL+C to quit"
```

## 📊 Startup Output Summary

When you run `python app.py`, you'll see:

```
WARNING:dolos_integration:Node.js not found. Dolos integration will not be available.
⚠️ Dolos integration not properly configured - using local detection only
INFO:apscheduler.scheduler:Scheduler started
🚀 Server started at: 2025-09-19 10:34:13.114005
📋 Session Management: Users will need to sign in again after server restart
INFO:apscheduler.scheduler:Added job "check_deadline_reminders" to job store "default"
INFO:apscheduler.scheduler:Added job "check_overdue_assignments" to job store "default"
🚀 Creating demo accounts...
✅ Database initialization completed
 * Serving Flask app 'app'
 * Debug mode: on
INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.100.33:5000
INFO:werkzeug:Press CTRL+C to quit
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: 109-416-955
```

## ⏱️ Timing Breakdown

- **Import Phase**: ~2-3 seconds
- **Configuration Phase**: ~1 second
- **Database Setup**: ~1-2 seconds
- **Route Registration**: ~1 second
- **Server Launch**: ~1 second

**Total Startup Time**: ~6-8 seconds

## 🔧 What Happens After Startup

Once the server is running:
1. **Database is ready** with all tables and demo accounts
2. **Email system is configured** and ready to send notifications
3. **Background scheduler is running** for automated tasks
4. **All routes are registered** and ready to handle requests
5. **Static files are served** (CSS, JS, images)
6. **Templates are loaded** and ready for rendering
7. **Session management is active** for user authentication

## 🎯 Ready for Use

After startup completes, your E-Assignment Submission System is fully operational with:
- ✅ User authentication
- ✅ Assignment management
- ✅ File uploads
- ✅ Email notifications
- ✅ Plagiarism detection
- ✅ Grading system
- ✅ Admin dashboard
