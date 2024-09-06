from flask import Flask, render_template
from .main_routes import main_routes
from .writeups_routes import writeups_routes
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ''
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    

    from .models import Post, User
    from .CRUD_post import create_post, display_post, delete_post, edit_post, upload_image
    from .auth import auth

    app.register_blueprint(main_routes, url_prefix='/')
    app.register_blueprint(writeups_routes, url_prefix='/writeups')
    app.register_blueprint(create_post, url_prefix='/create_post')
    app.register_blueprint(delete_post, url_prefix='/delete_post')
    app.register_blueprint(edit_post, url_prefix='/edit_post')
    app.register_blueprint(upload_image, url_prefix='/upload_image')
    app.register_blueprint(display_post, url_prefix='/post')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


