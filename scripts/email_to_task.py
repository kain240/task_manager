import imaplib
import email
import requests
import re
from email.header import decode_header
import dateparser
from dateparser.search import search_dates
from email.utils import parseaddr
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db, Task, User

EMAIL = "captain.pika21@gmail.com"
APP_PASSWORD = "etoi mbsm sgnq klxd"
IMAP_SERVER = "imap.gmail.com"
API_ENDPOINT = "http://127.0.0.1:5000/api/tasks"
USER_ID = 1


# Check if the email looks like a task
def is_task_email(subject, body):
    keywords = ['task', 'to-do', 'due', 'submit', 'finish', 'complete', 'deadline', 'do']
    content = f"{subject.lower()} {body.lower()}"
    contains_keyword = any(word in content for word in keywords)

    date_patterns = [
        r'\bby\s+\w+\b',
        r'\bby\s+\d{1,2}\s*\w+\b',
        r'\b\d{1,2}[:.]\d{2}\b',
        r'\b(?:on|before|after)\s+\w+\b'
    ]
    contains_deadline = any(re.search(pattern, content) for pattern in date_patterns)

    return contains_keyword and contains_deadline

# Extract due date and time from body
def extract_due_data(body):
    parsed = search_dates(body)

    if parsed:
        dt = parsed[0][1]  # Get datetime object
        due_date = dt.date()  # 'YYYY-MM-DD'
        due_time = dt.time()  # 'HH:MM'
        return due_date, due_time
    else:
        return None, None


# Decode subject line
def clean_subject(subject):
    decoded, charset = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or 'utf-8')
    return decoded

# Main fetcher
def fetch_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, APP_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} unread emails")

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        subject = clean_subject(msg["Subject"])
        from_email = msg.get("From")

        # Get plain text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        print(f"\nEmail from {from_email}, subject: {subject}")

        # ✅ Check if this email is a task
        if is_task_email(subject, body):
            print("✅ Task-related email detected.")

            due_date, due_time = extract_due_data(body)
            task_data = {
                "title": subject,
                "description": body.strip(),
                "due_date": due_date,
                "due_time": due_time
            }

            with app.app_context():
                user = User.query.filter_by(email='captain.pika21@gmail.com').first()
                if user:
                    new_task = Task(
                        title=task_data['title'],
                        description=task_data['description'],
                        status='incomplete',
                        due_date=task_data['due_date'],
                        due_time=task_data['due_time'].strftime("%H:%M") if task_data['due_time'] else None,
                        user_id=user.id
                    )
                    db.session.add(new_task)
                    db.session.commit()
                    print(f"✅ Task saved: {task_data['title']}")
                else:
                    print("❌ No matching user found.")

    mail.logout()


if __name__ == "__main__":
    fetch_emails()

