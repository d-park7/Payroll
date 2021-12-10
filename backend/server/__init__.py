from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager


db = SQLAlchemy()
# flask_marshmallow is used to seralize/deseralize data to and from the frontend/backed
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'david'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://david:david@db/testpayroll'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    from .views import views
    # from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    from .models import Employee, Pay, Record
    create_database(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app


def create_database(app):
    """Creates the postgresql database if not created"""
    db.create_all(app=app)
