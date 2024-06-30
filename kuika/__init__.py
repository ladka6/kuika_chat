from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # type: ignore
from config import settings
from flask_migrate import Migrate  # type: ignore
import redis

db = SQLAlchemy()
sess = Session()
migrate = Migrate()
redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        settings.SQLALCHEMY_TRACK_MODIFICATIONS
    )
    app.config["SESSION_TYPE"] = settings.SESSION_TYPE
    app.config["SESSION_PERMANENT"] = settings.SESSION_PERMANENT
    app.config["POSTGRES_USER"] = settings.POSTGRES_USER
    app.config["POSTGRES_PASSWORD"] = settings.POSTGRES_PASSWORD
    app.config["POSTGRES_HOST"] = settings.POSTGRES_HOST
    app.config["POSTGRES_PORT"] = settings.POSTGRES_PORT
    app.config["POSTGRES_DB"] = settings.POSTGRES_DB
    app.config["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

    db.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from kuika.main.models.models import Job  # type: ignore
        from kuika.main.controllers.chat_controller import chat_blueprint

        app.register_blueprint(chat_blueprint, url_prefix="/api")
        db.create_all()

    return app
