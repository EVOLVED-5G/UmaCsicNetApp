from os import environ
#from dotenv import load_dotenv


#basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))

class Config(object):
    """Flask config variables"""
    FLASK_APP = environ.get('FLASK_APP') 
    FLASK_ENV = "development"
    SECRET_KEY = environ.get('SECRET_KEY')
    PROPAGATE_EXCEPTIONS = True
    ERROR_404_HELP = False


    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_SQLALCHEMY_LOG_MESSAGES = False

    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_PORT = environ.get("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_RECIPIENT = environ.get("MAIL_RECIPIENT")