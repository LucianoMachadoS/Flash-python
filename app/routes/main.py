from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"message":"Realizar o login"})


# RF: O sistema deve permitir a listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify({"message": "Esta é a rota de listagem dos produtos"})

# RF: O sistema deve permitir a criação de todos os produtos
@main_bp.route('/products', methods=['POST'])
def create_products():
    return jsonify({"message": "Esta é a rota de criação do produtos"})

# RF: O sistema deve permitir a visualização dos detalhes de um unico produto
@main_bp.route('/products', methods=['GET'])
def get_product_by_id():
    return jsonify({"message": "Esta é a rota de criação do produtos"})
# RF: O sistema deve permitir a atualização de um unico produto e produto existente
# RF: O sistema deve permitir deletar um unico produto e produto existente
# RF: O sistema deve permitir a importação de vendas atraves de um arquivo
@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bem vindo ao Flask"})

