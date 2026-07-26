from flask import Blueprint, jsonify

category_bp = Blueprint('category_bp', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def get_categories():
    return jsonify({"message": "Esta é a rota de listagem das categorias"})

@category_bp.route('/', methods=['POST'])
def create_category():
    return jsonify({"message": "Esta é a rota de criação de uma categoria"})