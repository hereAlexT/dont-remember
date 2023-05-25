from os import environ
from flask import Flask
from flask_jwt_extended import JWTManager

from views.routers import users_blueprint
from models import db
import logging


def create_app(_config_overrides=None):
    _app = Flask(__name__)

    # set up loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    _app.logger.handlers = gunicorn_logger.handlers
    _app.logger.setLevel(gunicorn_logger.level)

    # set up sqlalchemy
    _app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 1,
        'pool_recycle': 60,
        'max_overflow': 1
    }
    _app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')  # Change this! #todo
    jwt = JWTManager(_app)

    # debug: print all env variables in logger error
    for key, value in environ.items():
        _app.logger.info(f"{key}={value}")
    print(_config_overrides)
    if _config_overrides:
        _app.config.update(_config_overrides)

    # Initialize the database
    db.init_app(_app)

    # Create the database tables.
    with _app.app_context():
        db.create_all()
        db.session.commit()

    # Register the blueprint
    _app.register_blueprint(users_blueprint, url_prefix='/api/v1/users')
    return _app


def wsgi_app(_environ, start_response):
    _app = create_app()
    return _app(_environ, start_response)


if __name__ == '__main__':
    config_overrides = {
        'SQLALCHEMY_DATABASE_URI': "postgresql://postgres:postgres@127.0.0.1:5432/dont_remember",
        'JWT_SECRET_KEY': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDgzMDI5NywianRpI"
    }
    # get environment form local.env file

    # Create the Flask application instance with the configuration overrides.
    app = create_app(_config_overrides=config_overrides)

    app.run(debug=True, port=8888)
