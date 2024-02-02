import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='cExf9s1CqdAR6sAfDTZLSA',
       SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'bfile.sqlite'),
       SQLALCHEMY_ECHO=True,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise Flask with the SQLAlchemy database extension
    db.init_app(app)

    # Models are defined in the models module, so you must import them before calling create_all, otherwise SQLAlchemy
    # will not know about them.
    from bfile.models import User, Region, Event
    # Create the tables in the database
    # create_all does not update tables if they are already in the database.
    with app.app_context():
        db.create_all()

        # Register the routes with the app in the context
        from bfile import paralympics

    return app