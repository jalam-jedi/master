# GIS Image Analysis Platform

A comprehensive Flask-based web application for managing, analyzing, and comparing Geographic Information System (GIS) imagery. This platform provides users with detailed insights into geographical locations, including historical relevance, modern impact, and climate analysis, coupled with an interactive community discussion system.

## 🚀 Features

- **User Authentication**: Secure sign-up, login, and logout functionality powered by `Flask-Login` and `Flask-Bcrypt`.
- **GIS Data Management**: Browse and view detailed information for various geographical locations, including coordinates (Latitude/Longitude), sources, and dates.
- **Detailed Image Analysis**: 
    - **Historical Relevance**: Insights into the past of the location.
    - **Modern Impact**: Current significance and influence.
    - **Comparative Analysis**: Technical comparisons between different states or times.
    - **Insights**: Key takeaways for each location.
- **Interactive Commenting System**: Users can post comments and replies on specific images, fostering community discussion.
- **Image Comparison Tool**: Compare two different analysis models side-by-side to identify differences and patterns.
- **Admin Dashboard**: A powerful administrative interface using `Flask-Admin` for managing users, GIS data, and comments.
- **Database Migrations**: Seamless schema updates managed by `Flask-Migrate`.

## 🛠️ Tech Stack

- **Framework**: [Flask](https://flask.palletsprojects.com/)
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite by default)
- **Forms**: [Flask-WTF](https://flask-wtf.readthedocs.io/)
- **Authentication**: [Flask-Login](https://flask-login.readthedocs.io/)
- **Security**: [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
- **Admin Panel**: [Flask-Admin](https://flask-admin.readthedocs.io/)
- **Styling**: Custom CSS (Vanilla)
- **Deployment**: Heroku-ready with `Procfile`

## 📋 Prerequisites

Ensure you have Python 3.x installed on your system.

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd master-main
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

5. **(Optional) Add initial admin data**:
   ```bash
   python add_data.py
   ```

## 🏃 Running the Application

Start the development server:
```bash
python main.py
```
The application will be accessible at `http://127.0.0.1:5000/`.

## 📂 Project Structure

```text
.
├── main.py              # Entry point of the application & route definitions
├── extensions.py        # Initialization of Flask extensions (db, login, admin, etc.)
├── dbclasses.py         # Database models and Flask-WTF forms
├── viewmodels.py        # Custom ModelViews for Flask-Admin
├── add_data.py          # Script for seeding the database with initial data
├── static/              # Static assets (CSS, JS, Images)
│   ├── css/             # Custom stylesheets
│   ├── scripts/         # Client-side scripts
│   └── Images/          # Uploaded/Managed imagery
├── templates/           # Jinja2 HTML templates
├── instance/            # Instance-specific files (e.g., sqlite db)
├── migrations/          # Database migration files
└── Procfile             # Configuration for Heroku deployment
```

## 🔒 Admin Access

To access the admin panel, navigate to `/admin` after logging in with an account that has `is_admin=True`. You can use the `add_data.py` script to create an initial admin user.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
*Created with ❤️ for GIS Enthusiasts.*
