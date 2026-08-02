from flask import Blueprint, jsonify, request, current_app
from app.models.product import ProductDBModel, UpdateProduct
from app.models.sale import Sale
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import PyMongoError
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt
import csv
import os
import io

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

    if user_data.username == "admin" and user_data.password == "123":
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return jsonify({'access_token': token}), 200

    return jsonify({"error": "Credenciais inválidas"}), 401


# RF: O sistema deve permitir a listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [
        ProductDBModel(**doc).model_dump(by_alias=True, exclude_none=True)
        for doc in products_cursor
    ]
    return jsonify(products_list)


# RF: O sistema deve permitir a criação de todos os produtos
@main_bp.route('/products', methods=['POST'])
@token_required
def create_products(token_data):
    try:
        product = ProductDBModel(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição"}), 500

    result = db.products.insert_one(product.model_dump())

    return jsonify({"message": "Produto criado com sucesso", "id": str(result.inserted_id)}), 201


# RF: O sistema deve permitir a visualização dos detalhes de um unico produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except (InvalidId, TypeError):
        return jsonify({"error": f"ID inválido: {product_id}"}), 400

    found_product = db.products.find_one({"_id": oid})

    if not found_product:
        return jsonify({"error": f"Produto com ID {product_id} não encontrado"}), 404

    product_model = ProductDBModel(**found_product).model_dump(by_alias=True, exclude_none=True)
    return jsonify(product_model)

# RF: O sistema deve permitir a atualização de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['PUT'])
@token_required
def update_product(token_data, product_id):
    try:
        oid = ObjectId(product_id)
    except (InvalidId, TypeError):
        return jsonify({"error": f"ID inválido: {product_id}"}), 400

    try:
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição"}), 500

    fields_to_update = update_data.model_dump(exclude_unset=True)

    if not fields_to_update:
        return jsonify({"error": "Nenhum campo para atualizar foi informado"}), 400

    update_result = db.products.update_one({"_id": oid}, {"$set": fields_to_update})

    if update_result.matched_count == 0:
        return jsonify({"error": f"Produto com ID {product_id} não encontrado"}), 404

    updated_product = db.products.find_one({"_id": oid})

    if not updated_product:
        return jsonify({"error": f"Produto com ID {product_id} não encontrado"}), 404

    return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True)), 200


# RF: O sistema deve permitir deletar um unico produto e produto existente
@main_bp.route('/product/<product_id>', methods=['DELETE'])
@token_required
def delete_product(token_data, product_id):
    try:
        oid = ObjectId(product_id)
    except (InvalidId, TypeError):
        return jsonify({"error": f"ID inválido: {product_id}"}), 400

    
    delete_result = db.products.delete_one({"_id": oid})

    if delete_result.deleted_count == 0:
        return jsonify({"error": f"Produto com ID {product_id} não encontrado"}), 404

    

    return jsonify({"message": f"Produto com ID {product_id} deletado com sucesso"}), 200


# RF: O sistema deve permitir a importação de vendas atraves de um arquivo
SALE_CSV_COLUMNS = ('product_id', 'quantity', 'sale_date', 'total_value')


@main_bp.route('/sales/upload', methods=['POST'])
@token_required
def upload_sales(token_data):
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if not file.filename:
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "Formato inválido: envie um arquivo .csv"}), 400

    try:
        # Lê o upload em streaming, sem carregar o arquivo inteiro na memória
        csv_stream = io.TextIOWrapper(file.stream, encoding='utf-8', newline='')
        csv_reader = csv.DictReader(csv_stream)

        if not csv_reader.fieldnames:
            return jsonify({"error": "Arquivo CSV vazio"}), 400

        missing_columns = [c for c in SALE_CSV_COLUMNS if c not in csv_reader.fieldnames]
        if missing_columns:
            return jsonify({"error": f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}"}), 400

        sales_to_insert = []
        errors = []

        # start=2 porque a linha 1 do arquivo é o cabeçalho
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Ignora colunas extras do arquivo, mantendo apenas as do modelo
                sale_data = Sale.model_validate({column: row[column] for column in SALE_CSV_COLUMNS})
                sales_to_insert.append(sale_data.to_mongo())
            except ValidationError as e:
                details = '; '.join(f"{err['loc'][0]}: {err['msg']}" for err in e.errors())
                errors.append(f'Linha {row_num}: {details}')
            except Exception as e:
                errors.append(f'Linha {row_num}: Erro inesperado: {str(e)}')

    except UnicodeDecodeError:
        return jsonify({"error": "Arquivo não está codificado em UTF-8"}), 400
    except csv.Error as e:
        return jsonify({"error": f"Arquivo CSV malformado: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo: {str(e)}"}), 500

    if not sales_to_insert:
        return jsonify({"error": "Nenhuma venda válida encontrada no arquivo", "errors": errors}), 400

    try:
        result = db.sales.insert_many(sales_to_insert)
    except PyMongoError as e:
        return jsonify({"error": f"Erro ao salvar as vendas: {str(e)}"}), 500

    response = {
        "message": "Importação concluída",
        "inserted": len(result.inserted_ids),
        "failed": len(errors)
    }

    if errors:
        response["errors"] = errors
        return jsonify(response), 207

    return jsonify(response), 201


@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bem vindo ao Flask"})

