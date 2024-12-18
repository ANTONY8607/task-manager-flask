from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='user', lazy=True)
    shared_tasks = db.relationship('TaskShare', 
                                 foreign_keys='TaskShare.shared_with_id',
                                 backref='shared_with',
                                 lazy=True)
    google_token = db.Column(db.String(250))
    notification_preferences = db.Column(db.JSON, default={
        'email': True,
        'browser': True,
        'advance_notice': 24  # heures
    })

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20))
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with = db.relationship('TaskShare', backref='task', lazy=True)
    reminder_sent = db.Column(db.Boolean, default=False)
    google_event_id = db.Column(db.String(250))
    last_sync = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'priority': self.priority,
            'category': self.category,
            'shared_with': [share.shared_with.email for share in self.shared_with]
        }

class TaskShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    shared_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    permissions = db.Column(db.String(20), default='view')  # 'view' ou 'edit'
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    shared_by = db.relationship('User', foreign_keys=[shared_by_id])
    shared_with = db.relationship('User', foreign_keys=[shared_with_id])

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(20))  # 'reminder', 'share', 'update'
