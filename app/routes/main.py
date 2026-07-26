from flask import Blueprint, jsonify, request
from app.models.user import LoginPayload
from pydantic import ValidationError

main_bp = Blueprint('main_bp', __name__)


# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição"}), 500

    if user_data.username == "admin" and user_data.password == "admin":
        return jsonify({"message": f"Login bem-sucedido para o usuário {user_data.username}"})
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401


# RF: O sistema deve permitir a listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify({"message": "Esta é a rota de listagem dos produtos"})


# RF: O sistema deve permitir a criação de todos os produtos
@main_bp.route('/products', methods=['POST'])
def create_products():
    return jsonify({"message": "Esta é a rota de criação do produtos"})


# RF: O sistema deve permitir a visualização dos detalhes de um unico produto
@main_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return jsonify({"message": f"Esta é a rota de visualização do produto com ID {product_id}"})


# RF: O sistema deve permitir a atualização de um unico produto e produto existente
@main_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message": f"Esta é a rota de atualização do produto com ID {product_id}"})


# RF: O sistema deve permitir deletar um unico produto e produto existente
@main_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({"message": f"Esta é a rota de deleção do produto com ID {product_id}"})


# RF: O sistema deve permitir a importação de vendas atraves de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message": "Esta é a rota de upload de vendas"})


@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bem vindo ao Flask"})

