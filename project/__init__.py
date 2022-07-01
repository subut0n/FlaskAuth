from venv import create
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

load_dotenv()

def create_app():
    app = Flask(__name__)

    # sentry_sdk.init(
    #     dsn="https://62f8d8dea17c4a36a179f3abffed88d9@o1303935.ingest.sentry.io/6543498",
    #     integrations=[
    #         FlaskIntegration(),
    #     ],

    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for performance monitoring.
    #     # We recommend adjusting this value in production.
    #     traces_sample_rate=1.0
    # )

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()