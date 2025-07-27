from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# LoginManager: It controls how users log in and where to redirect unauthorized users.
# UserMixin: A helper class: is_authenticated, is_active, get_id etc.

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta

app = Flask(__name__)

app.secret_key = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='Pending')   # pending/ In Progress/ Completed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date = db.Column(db.Date, default= lambda : date.today()+ timedelta(days=1))  # tomorrows date as default
    due_time = db.Column(db.String, default= lambda: datetime.now().strftime('%H:%M'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username = username).first():
            flash('Username taken! Try another.', 'error')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password = generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Login now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date_str = request.form['due_date']
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # converted string into date format
        due_time = request.form['due_time']

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            due_time=due_time,
            user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Task added!', 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_edit_task.html', task= None)


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POSt'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        due_date_str = request.form['due_date']
        task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # converted string into date format
        task.due_time = request.form['due_time']
        task.status = request.form['status']

        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_edit_task.html', task=task)


@app.route('/delete/<int:task_id>', methods= ['GET', 'POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized!', 'error')
        return redirect(url_for('dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('task deleted', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

