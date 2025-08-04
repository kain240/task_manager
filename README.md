Task Master – Smart Task Management System
Task Master is a Flask-based task management web application that helps users organize tasks efficiently.
It supports user authentication, CRUD operations for tasks, and automated task creation via email triggers,
making productivity simple and seamless.

🚀 Features
User Authentication: Secure login and registration using Flask-Login.

Task Management (CRUD): Create, view, update, and delete tasks.

Email-based Task Creation: Automatically create tasks via scheduled emails.

Task Status Tracking: Mark tasks as completed and filter by status.

Responsive Dashboard: Clean, mobile-friendly UI using Bootstrap.

Database Integration: Persistent data storage using SQLite (can upgrade to MySQL/PostgreSQL).

🖥️ Tech Stack
Frontend: HTML, CSS, Bootstrap, JavaScript

Backend: Python, Flask

Database: SQLite (via SQLAlchemy ORM)

Other Tools: Flask-Login, Flask-Mail, Jinja2 Templates

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
│── requirements.txt         # Python dependencies
│── README.md                # Project documentation
⚡ Getting Started
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/kain240/task_manager.git
cd task_manager
2️⃣ Create Virtual Environment & Install Dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
3️⃣ Run the Application
bash
Copy
Edit
python app.py
Then open http://127.0.0.1:5000/ in your browser.

📝 Usage
Register or Login to your account.

Add new tasks with title, description, and due date.

Mark tasks as completed or delete when done.

View tasks in a clean, responsive dashboard.

📌 Future Enhancements
Add priority levels and reminder notifications.

Integrate Google Calendar for auto-syncing events.

Deploy to cloud with PostgreSQL support.

