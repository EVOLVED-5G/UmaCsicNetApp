from os import environ

# Configuration class
class Config(object):
    """Flask config variables"""
    FLASK_APP = environ.get('FLASK_APP') 
    # Server status
    FLASK_ENV = "development"
    SECRET_KEY = environ.get('SECRET_KEY')
    PROPAGATE_EXCEPTIONS = True
    ERROR_404_HELP = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_SQLALCHEMY_LOG_MESSAGES = False

    # Telegram configuration
    TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = environ.get('TELEGRAM_CHAT_ID')