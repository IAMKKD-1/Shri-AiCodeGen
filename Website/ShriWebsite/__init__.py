from flask import Flask
import os

def index():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    return app