from flask import Flask

from pymongo import MongoClient

db = None

def create_app():
   app = Flask(__name__)
   app.config.from_object('config.Config')
   global db

   try:
      client = MongoClient(app.config['MONGO_URI'])
      db = client.get_default_database()
   except Exception as e:
      print(f"Erro ao conectar ao MongoDB: {e}")

   from app.routes.main import main_bp
   from app.routes.category_routes import category_bp #Importações dos blueprint evitanto erro com o banco de dados, evitando que o banco de dados seja chamado antes da criação do app
   app.register_blueprint(main_bp)
   app.register_blueprint(category_bp)


   return app
