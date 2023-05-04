from os import environ
from flask import Flask
from views.routers import users_blueprint
from models import db
import logging
from sqlalchemy.pool import QueuePool


def create_app(config_overrides=None):
    app = Flask(__name__)

    # set up loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    # set up sqlalchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 1,
        'pool_recycle': 60,
        'max_overflow': 1
    }

    # debug: print all env variables in logger error
    for key, value in environ.items():
        app.logger.info(f"{key}={value}")
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize the database
    db.init_app(app)

    # Create the database tables.
    with app.app_context():
        db.create_all()
        db.session.commit()

    # Register the blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    return app


def wsgi_app(environ, start_response):
    app = create_app()
    return app(environ, start_response)


if __name__ == '__main__':
    config_overrides = {}
    # Create the Flask application instance with the configuration overrides.
    app = create_app(config_overrides=config_overrides)

    app.run(debug=True)
