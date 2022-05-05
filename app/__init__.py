from pickle import FALSE
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate ()
load_dotenv()

def create_app(test_config = None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TESTING_SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.cats import Cat

    from .routes import cats_bp
    app.register_blueprint(cats_bp)

    return app

