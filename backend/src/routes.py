from typing import List
from flask import jsonify, request, make_response, redirect, Blueprint, current_app as app
from helpers.formatting import format_list, sqlalchemy_to_dict
from models.product_model import ProductModel
from repositories.product_repository import ProductRepository
from utils.vector_db import VectorDb
import templates
from utils.chatbot import Chatbot, OutputParserTypes
from langchain.docstore.document import Document

api_bp = Blueprint("api", __name__)

@api_bp.route("/", methods=['GET'])
def root():
    response = make_response(jsonify({
        "message" : "hello from RetailARVA API"
    }))

    response.status_code = 200
    response.headers['content-type'] = 'application/json'
    return response


@api_bp.route('/gradio-app')
def redirect_to_gradio():
    return redirect(app.config.get('GRADIO_URL'), code=302)


@api_bp.route("/products/<product_id>", methods=['GET'])
def get_by_id(product_id: int):
    if product_id:
        product_repo = ProductRepository(app.config['DB']())
        product = product_repo.fetch_by_id(product_id)
        response = make_response(jsonify({
            "data" : product.to_dict()
        }))
        response.status_code = 200
    else:
        response = make_response(jsonify({
            "error" : "no product found with the given id"
        }))
        response.status_code = 404
        
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/chat", methods=['POST'])
def chat_with_assistant():
    chat = app.config['CHAT']()
    rag_pipeline = app.config['RAG_PIPELINE']()
    
    request_data = request.get_json()
    query = request_data['message']
    print(f"user query: {query}")
    response = chat.invoke(query, rag_pipeline)

    print(f"chat response: {response}")

    response = make_response(jsonify({
        "response" : response
    }))

    response.status_code = 201
    response.headers['content-type'] = 'application/json'
    return response


@api_bp.route("/products/embeddings", methods=['POST'])
def create_product_embeddings():
    product_profiles : list[str] = []
    docs : List[Document] = []
    product_repo = ProductRepository(app.config['DB']())
    qdrant : VectorDb = app.config['QDRANT']()
    
    for product in product_repo.fetch_all():
        product_data = sqlalchemy_to_dict(product)
        # Convert comma-separated strings to lists
        product_data['ingredients'] = product_data['ingredients'].split(',')
        product_data['key_ingredients'] = product_data['key_ingredients'].split(',')
        product_data['benefits'] = product_data['benefits'].split(',')
        product_data['application_tips'] = product_data['application_tips'].split(',')
        product_data['skin_types'] = product_data['skin_types'].split(',')
        product_data['skin_concerns'] = product_data['skin_concerns'].split(',')
        if product_data['side_effects']:
            product_data['side_effects'] = product_data['side_effects'].split(',')
        if product_data['allergens']:
            product_data['allergens'] = product_data['allergens'].split(',')
        if product_data['sensitivities']:
            product_data['sensitivities'] = product_data['sensitivities'].split(',')
        
        product_model = ProductModel(**product_data)

        product_profile = templates.product_profile.format(
            id=product_model.id,
            name=product_model.name,
            brand=product_model.brand,
            category=product_model.category,
            price=product_model.price,
            is_natural="Yes" if product_model.is_natural else "No",
            concentrations=product_model.concentrations,
            ingredients_list=format_list(product_model.ingredients),
            key_ingredients_list=format_list(product_model.key_ingredients),
            benefits_list=format_list(product_model.benefits),
            side_effects_list=format_list(product_model.side_effects),
            usage=product.usage,
            application_tips_list=format_list(product_model.application_tips),
            skin_types_list=format_list(product_model.skin_types),
            skin_concerns_list=format_list(product_model.skin_concerns),
            allergens_list=format_list(product_model.allergens),
            sensitivities_list=format_list(product_model.sensitivities)            
        )

        product_profiles.append(product_profile)

        docs.append(
            Document(
                page_content=product_profile,
                metadata={
                    "id": product_model.id,
                    "product name": product_model.name,
                    "product brand": product_model.brand,
                    "product category": product_model.category
                }
            )
        )
    
    print(f"embedding {len(docs)} documents")
    qdrant.embed_documents(
        docs=docs,
        collection="products"
    )
    
    response = make_response(jsonify({
        "message" : "vectors in products collection created successfully"
    }))
    response.status_code = 201
    response.headers['content-type'] = 'application/json'
    return product_profiles