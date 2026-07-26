from flask import Flask
from .routes.main import main_bp
from .routes.category_routes import category_bp

def create_app():
   app = Flask(__name__)
   app.register_blueprint(main_bp)
   app.register_blueprint(category_bp)
   return app
