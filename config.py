import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '7110c8ae51a4b5af97be6534caefs0e4bb9bdcb3380af00sr50b23a5d1616bf319bc298105da20fe'
    PROPAGATE_EXCEPTIONS = True


    #Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_SQLALCHEMY_LOG_MESSAGES = False

    ERROR_404_HELP = False

