from datetime import datetime
from models import db, Task, Notifications
from flask_login import current_user

def check_and_create_overdue_notifications():
    now = datetime.now()

    overdue_tasks = Task.query.filter(
        Task.status != 'Completed',
        Task.user_id == current_user.id,
        ((Task.due_date <= now.date()) & (Task.due_time < now.time()))
    ).all()

    for task in overdue_tasks:
        message = f"Task '{task.title}' is overdue and still incomplete."

        # Avoid duplicate notifications
        existing = Notifications.query.filter_by(user_id=task.user_id, message=message).first()
        if not existing:
            note = Notifications(user_id=task.user_id, message=message)
            db.session.add(note)

    db.session.commit()