from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    mail.init_app(app)
    
    
    from src.api.resources import bp_api
    app.register_blueprint(bp_api)

    #from src.errors import bp as bp_errors
    #app.register_blueprint(bp_errors)

    # from src.thread import check_data
    # check_data.process(app)

    return app


