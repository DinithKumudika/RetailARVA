from typing import List
from flask import jsonify, make_response, redirect, Blueprint, current_app as app
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


@api_bp.route("/chat/gemini", methods=['POST'])
def chat_with_assistant():
    gemini_chat = Chatbot(app.config.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'))
    gemini_chat.set_parser(OutputParserTypes.STRING)
    gemini_chat.set_vector_store(app.config['QDRANT']().get_collection("products"))
    # chat_response = gemini_chat.invoke("hello")
    response = gemini_chat.greet()

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