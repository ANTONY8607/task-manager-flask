from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler
from flask_talisman import Talisman
from config import Config
import redis
from celery import Celery

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()
scheduler = APScheduler()

# Initialisation de Redis
redis_client = redis.Redis.from_url(Config.REDIS_URL)

# Initialisation de Celery
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    
    # Configuration de Celery
    celery.conf.update(app.config)
    
    # Configuration de la sécurité
    Talisman(app, content_security_policy={
        'default-src': "'self'",
        'img-src': "'self' data:",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    })
    
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.session_protection = "strong"

    # Enregistrement des blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Démarrage du planificateur
    scheduler.start()
    
    # Configuration des tâches planifiées
    with app.app_context():
        from app.notifications import check_upcoming_tasks
        scheduler.add_job(
            id='check_tasks',
            func=check_upcoming_tasks,
            trigger='interval',
            seconds=app.config['NOTIFICATION_CHECK_INTERVAL']
        )
    
    return app
