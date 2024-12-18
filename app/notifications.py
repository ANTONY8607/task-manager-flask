from flask import current_app
from flask_mail import Message
from celery import Celery
from datetime import datetime, timedelta
import redis
from app import mail
from app.models import Task, User, TaskShare, db

# Configuration Redis pour la persistance des données
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Configuration Celery pour les tâches asynchrones
celery = Celery('app', broker='redis://localhost:6379/0')

@celery.task
def send_notification_email(user_email, subject, body):
    """Envoie un email de notification"""
    with current_app.app_context():
        msg = Message(subject,
                     sender=current_app.config['MAIL_DEFAULT_SENDER'],
                     recipients=[user_email])
        msg.body = body
        mail.send(msg)

@celery.task
def check_upcoming_tasks():
    """Vérifie les tâches à venir et envoie des notifications"""
    with current_app.app_context():
        # Vérifier les tâches dues dans les prochaines 24 heures
        tomorrow = datetime.now() + timedelta(days=1)
        tasks = Task.query.filter(
            Task.due_date <= tomorrow,
            Task.completed == False
        ).all()

        for task in tasks:
            # Vérifier si une notification a déjà été envoyée
            notification_key = f'notification:task:{task.id}'
            if not redis_client.get(notification_key):
                # Envoyer la notification
                send_notification_email.delay(
                    task.user.email,
                    "Rappel de tâche",
                    f"La tâche '{task.title}' est due le {task.due_date.strftime('%d/%m/%Y à %H:%M')}"
                )
                # Marquer la notification comme envoyée
                redis_client.setex(notification_key, 86400, 'sent')  # expire après 24h

def share_task(task_id, shared_with_email):
    """Partage une tâche avec un autre utilisateur"""
    task = Task.query.get(task_id)
    shared_with_user = User.query.filter_by(email=shared_with_email).first()
    
    if task and shared_with_user:
        # Créer le partage
        share = TaskShare(
            task_id=task.id,
            shared_by_id=task.user_id,
            shared_with_id=shared_with_user.id
        )
        db.session.add(share)
        db.session.commit()
        
        # Envoyer une notification
        send_notification_email.delay(
            shared_with_email,
            "Nouvelle tâche partagée",
            f"{task.user.username} a partagé la tâche '{task.title}' avec vous."
        )
        return True
    return False

def sync_with_google_calendar(user_id):
    """Synchronise les tâches avec Google Calendar"""
    # Cette fonction serait implémentée avec l'API Google Calendar
    pass
