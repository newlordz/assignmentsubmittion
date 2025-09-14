# Demo Accounts for Assignment Submission System

This document contains the login credentials for all demo accounts created for testing purposes.

## 📚 Student Accounts

| Username | Password | Full Name | Email |
|----------|----------|-----------|-------|
| student1 | student123 | John Doe | john.doe@university.edu |
| student2 | student123 | Jane Smith | jane.smith@university.edu |
| student3 | student123 | Mike Johnson | mike.johnson@university.edu |
| student4 | student123 | Sarah Wilson | sarah.wilson@university.edu |
| student5 | student123 | David Brown | david.brown@university.edu |

## 👨‍🏫 Lecturer Accounts

| Username | Password | Full Name | Email |
|----------|----------|-----------|-------|
| lecturer1 | lecturer123 | Professor Jones | prof.jones@university.edu |
| lecturer2 | lecturer123 | Dr. Maria Garcia | dr.garcia@university.edu |
| lecturer3 | lecturer123 | Professor Lee | prof.lee@university.edu |

## 👨‍💼 Admin Account

| Username | Password | Full Name | Email |
|----------|----------|-----------|-------|
| admin | admin123 | System Administrator | admin@university.edu |

## 🎯 Demo Data Created

### Assignments
- **Introduction to Programming - Assignment 1** (Due in 7 days, 100 marks)
- **Database Design Project** (Due in 14 days, 150 marks)
- **Web Development Final Project** (Due in 21 days, 200 marks)
- **Data Structures and Algorithms - Lab 3** (Due in 5 days, 80 marks)
- **Machine Learning Project** (Due in 30 days, 250 marks)

### Submissions
- 9 demo submissions created across different assignments
- Some submissions are marked as late for testing late submission handling
- All submissions have dummy content for testing

### Grades
- 6 demo grades created with varying marks (75-100)
- Feedback comments included for each graded submission

## 🚀 How to Test

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - Open your browser and go to `http://localhost:5000`

3. **Test different user roles:**
   - **Students:** Can view assignments, submit work, check grades
   - **Lecturers:** Can create assignments, grade submissions, view analytics
   - **Admin:** Can view system statistics, manage users, monitor activity

4. **Test key features:**
   - User registration and login
   - Assignment creation and submission
   - File upload and download
   - Grading system
   - Notification system
   - Dashboard views for each role

## 📝 Notes

- All demo accounts use simple passwords for easy testing
- Demo data is created with realistic content for comprehensive testing
- The system includes plagiarism detection features (though simplified for demo)
- File uploads are stored in the `static/uploads` directory
- Database is SQLite (`instance/assignment_system.db`)

## 🔧 Troubleshooting

If you encounter any issues:

1. **Database errors:** Delete the `instance` folder and restart the application
2. **File upload issues:** Ensure the `static/uploads` directory exists and has write permissions
3. **Login issues:** Verify the username and password are correct (case-sensitive)

## 🗑️ Clean Demo Data

To remove all demo data and start fresh:

1. Delete the `instance` folder
2. Delete the `static/uploads` folder
3. Restart the application

The system will recreate the database with only the default admin account.
