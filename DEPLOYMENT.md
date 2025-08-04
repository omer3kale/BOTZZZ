# 🚀 BOTZZZ Deployment Guide

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/omer3kale/BOTZZZ.git
cd BOTZZZ/admin_panel
```

### 2. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5001`

## 🔐 Authentication Systems

### Admin Access
- **URL**: `http://localhost:5001/login`
- **Default Credentials**:
  - **Super Admin**: `admin` / `BOTZZZ2025!`
  - **Operator**: `operator` / `operator123`
  - **Viewer**: `viewer` / `viewer123`

### User Registration & Login
- **Registration**: `http://localhost:5001/register`
- **User Login**: `http://localhost:5001/user-login`
- **User Dashboard**: `http://localhost:5001/user-dashboard` (after login)

## 🌟 Features

### For Users
- **Service Registration**: Choose from Instagram, YouTube, TikTok, or Twitter bot services
- **User Dashboard**: Track your bot activities and analytics
- **Service Management**: Monitor engagement metrics and performance

### For Admins
- **Complete Control Panel**: Manage all bot operations
- **Real-time Analytics**: Monitor system performance and user activities
- **User Management**: Oversee registered users and their activities
- **System Monitoring**: Track logs, errors, and system health

## 🛠️ Technical Stack

- **Backend**: Flask 3.1.1 with Flask-Login authentication
- **Frontend**: Bootstrap 5.1.3 with responsive design
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Authentication**: Role-based access control (Admin/User)
- **Deployment**: Gunicorn ready for production

## 📱 Available Services

1. **Instagram Bot Services**
   - Follower growth automation
   - Engagement optimization
   - Content interaction

2. **YouTube Bot Services**
   - Subscriber management
   - View optimization
   - Comment automation

3. **TikTok Bot Services**
   - Viral content promotion
   - Follower acquisition
   - Engagement boost

4. **Twitter Bot Services**
   - Tweet automation
   - Follower growth
   - Engagement enhancement

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///botzzz.db
```

### Production Deployment
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 📊 Monitoring

Access the admin dashboard to monitor:
- **User Registration Trends**
- **Service Usage Statistics**
- **System Performance Metrics**
- **Revenue Analytics**
- **Error Logs and System Health**

## 🔒 Security Features

- **Password Hashing**: Werkzeug secure password hashing
- **Session Management**: Flask-Login secure session handling
- **Role-Based Access**: Separate admin and user privileges
- **CSRF Protection**: Built-in Flask security features
- **Input Validation**: Form validation and sanitization

## 📞 Support

For technical support or feature requests, please visit the GitHub repository:
https://github.com/omer3kale/BOTZZZ

---

**BOTZZZ** - Professional Bot Automation Platform
*Empowering social media growth through intelligent automation*
