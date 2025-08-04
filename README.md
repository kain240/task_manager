Task Master – Smart Task Management System
Task Master is a Flask-based task management web application that helps users organize their tasks efficiently.
It supports user authentication, CRUD operations for tasks, and automated task creation via email triggers,
making productivity simple and seamless.

🚀 Features
User Authentication: Secure login and registration using Flask-Login.

Task Management (CRUD): Create, view, update, and delete tasks.

Email-based Task Creation: Automatically create tasks by sending scheduled emails.

Task Status Tracking: Mark tasks as completed and filter by pending/completed status.

Responsive Dashboard: Bootstrap-powered UI for a clean and mobile-friendly experience.

Database Integration: Persistent data storage using SQLite (can be upgraded to MySQL/PostgreSQL).

🖥️ Tech Stack
Frontend: HTML, CSS, Bootstrap, JavaScript
Backend: Python, Flask
Database: SQLite (via SQLAlchemy ORM)
Other Tools: Flask-Login, Flask-Mail (for email-based tasks), Jinja2 Templates

📂 Project Structure
csharp
Copy
Edit
Task_Master/
│── backend/
│   ├── app.py               # Main Flask application
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes
│   ├── templates/           # HTML templates (Jinja2)
│   └── static/              # CSS, JS, and images
│
│── database/
│   └── task_master.db       # SQLite database
│
│── README.md                # Project documentation
│── requirements.txt         # Python dependencies
⚡ Getting Started
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/kain240/task_manager.git
cd task_manager
2️⃣ Create a Virtual Environment & Install Dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows

pip install -r requirements.txt
3️⃣ Run the Application
bash
Copy
Edit
python app.py
The app will run on http://127.0.0.1:5000/

📝 Usage
Register/Login to create your account.

Add new tasks with title, description, and due date.

Mark tasks as completed or delete tasks when done.

Send an email to auto-create tasks (if configured).

View tasks in a clean and responsive dashboard.

📸 Screenshots
Home Dashboard

Add Task Page

📌 Future Enhancements
Add priority levels and reminder notifications.

Integrate Google Calendar API for automatic event syncing.

Deploy on Heroku/Render with cloud database support.
