# Skill Hub Academy

> A comprehensive e-learning platform built with Django that empowers students and professionals to develop practical skills and thrive in the digital age.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Key Features

### For Students
- **Course Discovery** - Browse and search courses by category, difficulty level, and delivery mode
- **Flexible Enrollment** - Enroll in course sessions (online, onsite, or hybrid)
- **Progress Tracking** - Monitor enrollment status from pending to completion
- **Course Reviews** - Rate courses (1-5 stars) and share detailed feedback
- **Course Suggestions** - Request new courses or custom training programs
- **Personal Dashboard** - Manage profile, enrollments, and learning history

### For Instructors
- **Course Management** - Create, edit, and manage courses with rich metadata
- **Session Scheduling** - Schedule multiple sessions with capacity management
- **Project Assignments** - Add projects and assignments to courses
- **Professional Profile** - Showcase expertise, certifications, and hourly rates
- **Student Insights** - View enrollments and student engagement

### For Administrators
- **User Management** - Manage users and role assignments
- **Instructor Approval** - Review and approve instructor applications
- **Content Moderation** - Activate, feature, and manage courses
- **Feedback Management** - Respond to user feedback and suggestions
- **Analytics Dashboard** - Monitor platform activity via Django Admin

### Platform Highlights
- Role-based access control (Student, Instructor, Admin)
- Instructor verification workflow
- Course rating and review system
- Multi-delivery modes (Online, Onsite, Hybrid)
- Difficulty levels (Beginner to Expert)
- Target audience segmentation
- Cloud-based media storage

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Django 5.2, Python 3.11 |
| **Database** | PostgreSQL (AWS RDS) |
| **Frontend** | Bootstrap 5, Django Templates |
| **Media Storage** | Cloudinary |
| **Static Files** | WhiteNoise |
| **Deployment** | Heroku, Gunicorn |
| **Authentication** | Django Authentication System |

---

## Screenshots

<p align="center">
  <i>Screenshots coming soon...</i>
</p>

<!--
Add your screenshots here:
![Homepage](screenshots/homepage.png)
![Course Catalog](screenshots/courses.png)
![Dashboard](screenshots/dashboard.png)
-->

---

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (or SQLite for development)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Skill-Hub-Academy.git
   cd Skill-Hub-Academy
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True

   # Database (use SQLite for local development)
   DATABASE_URL=sqlite:///db.sqlite3

   # Cloudinary (optional for local development)
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## Project Structure

```
Skill-Hub-Academy/
│
├── apps/                       # Django applications
│   ├── core/                   # Homepage, about, contact pages
│   ├── users/                  # Authentication & user management
│   ├── courses/                # Course & session management
│   ├── enrollments/            # Student enrollment system
│   ├── reviews/                # Course ratings & reviews
│   ├── feedback/               # User feedback system
│   └── suggestions/            # Course suggestion requests
│
├── config/                     # Project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
│
├── templates/                  # Global HTML templates
├── static/                     # CSS, JavaScript, images
├── media/                      # User-uploaded content
│
├── manage.py                   # Django CLI
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku configuration
├── runtime.txt                 # Python version
└── README.md                   # Project documentation
```

---

## API Endpoints Overview

| Endpoint | Description |
|----------|-------------|
| `/` | Homepage with featured courses |
| `/courses/` | Course catalog with filtering |
| `/courses/<slug>/` | Course detail page |
| `/categories/` | Browse by category |
| `/enrollments/` | User enrollments |
| `/reviews/` | Course reviews |
| `/feedback/` | Submit feedback |
| `/suggestions/` | Suggest new courses |
| `/profile/` | Student profile |
| `/profile_pro/` | Instructor profile |
| `/admin/` | Admin dashboard |

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

**Ahmed Ghali** - Full-Stack Django Developer

- LinkedIn: [linkedin.com/in/ghali-ahmed](https://www.linkedin.com/in/ghali-ahmed/)
- GitHub: [github.com/ahmedghali](https://github.com/ahmedghali)

---

## Acknowledgments

- Django Documentation
- Bootstrap 5
- Cloudinary for media management
- The open-source community

---

<p align="center">
  <b>Built with Django</b><br>
  <i>A portfolio project demonstrating full-stack web development skills</i>
</p>
