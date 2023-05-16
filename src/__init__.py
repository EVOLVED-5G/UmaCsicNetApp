from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_mail import Mail

# Init database
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()

# Create function init
def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    mail.init_app(app)
    
    from src.api.resources import bp_api
    app.register_blueprint(bp_api)

    return app