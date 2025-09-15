# Course-Based Assignment System

## 🎯 Overview

The assignment submission system now includes a **course-based structure** that allows lecturers to organize students into specific courses and send targeted assignments and notifications.

## ✨ Key Features

### 📚 Course Management
- **Lecturers can create courses** with unique codes (e.g., CS101, MATH201)
- **Students can enroll in courses** using course codes
- **Course-based assignment distribution** - no more sending to ALL students

### 🎯 Targeted Communication
- **Assignments are course-specific** - only students in that course receive them
- **Email notifications are targeted** to relevant students only
- **Professional course-based communication**

### 👥 User Experience
- **Students see only their course assignments** in "My Assignments"
- **Lecturers select which course** when creating assignments
- **Navigation updated** with course management links

## 🚀 How It Works

### For Lecturers:
1. **Create a course** (e.g., "CS101 - Introduction to Programming")
2. **Share the course code** with students (e.g., "CS101")
3. **Create assignments** and select which course they're for
4. **Only students in that course** get notified!

### For Students:
1. **Enroll in courses** using course codes from lecturers
2. **See only assignments** from courses they're enrolled in
3. **Receive targeted email notifications** for relevant assignments

## 📧 Email System Benefits
- **No more spam** - students only get emails for their courses
- **Lecturers can target specific groups** of students
- **Professional course-based communication**

## 🧪 Demo Data
The system comes with pre-created demo data:
- **4 demo courses**: CS101, CS201, CS301, CS401
- **All students enrolled** in all courses initially
- **Sample assignments** assigned to appropriate courses

## 🌐 Testing the System

### Demo Accounts:
- **Lecturer**: `lecturer1` / `password123`
- **Student**: `student1` / `password123`

### Test Flow:
1. **Login as lecturer1** → Create a new assignment → Select a course
2. **Login as student1** → Check "My Assignments" → Only see relevant assignments
3. **Check your Gmail** → Only get emails for assignments in your courses

## 🔧 Technical Implementation

### Database Changes:
- Added `Course` model with course information
- Added `course_enrollment` table for many-to-many relationship
- Updated `Assignment` model to include `course_id`
- Updated all assignment queries to be course-specific

### New Routes:
- `/course/create` - Create new courses (lecturers)
- `/course/enroll` - Enroll in courses (students)
- `/course/available` - View available courses (students)

### Updated Routes:
- `/assignment/create` - Now requires course selection
- `/student/assignments` - Only shows course-specific assignments
- Email notifications - Only sent to students in the course

## 🎉 Benefits

1. **Better Organization**: Lecturers can manage multiple courses separately
2. **Targeted Communication**: Students only get relevant notifications
3. **Professional Structure**: Mimics real university course systems
4. **Reduced Spam**: No more emails to all students for every assignment
5. **Scalable**: Easy to add more courses and manage large student bodies

## 📱 Navigation Updates

### For Students:
- **"Enroll in Course"** - Join courses using course codes
- **"My Assignments"** - View only course-specific assignments

### For Lecturers:
- **"Create Course"** - Set up new courses
- **"Create Assignment"** - Now includes course selection dropdown

This system provides a much more professional and organized approach to assignment management, exactly as requested!
