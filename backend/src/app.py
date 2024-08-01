from typing import List
from flask import Flask, make_response, jsonify
from dotenv import dotenv_values
from configs.database import Database
from models.product_model import ProductModel
from utils.gemini_chat import GeminiChat, OutputParserTypes
from utils.database import create_all, is_database_created
from utils.vector_db import VectorDb
from repositories.product_repository import ProductRepository
from helpers.formatting import format_list, sqlalchemy_to_dict
from langchain.docstore.document import Document
import templates

app = Flask(__name__)
env = dotenv_values("../.env")

db = Database(env.get('DATABASE_URL'))
db.connect()

qdrant = VectorDb(
    env.get('QDRANT_CLUSTER_URL'), 
    env.get('QDRANT_API_KEY')
)
qdrant.set_embedding_model(model_id="models/embedding-001", api_key=env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'))


if is_database_created(db) == False:
    create_all(db)

product_repo = ProductRepository(db)


@app.route("/chat/gemini", methods=['POST'])
def chat_with_assistant():
    gemini_chat = GeminiChat(env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'))
    gemini_chat.set_parser(OutputParserTypes.STRING)
    gemini_chat.set_vector_store(qdrant.get_collection("products"))
    chat_response = gemini_chat.invoke("hello")

    print(f"chat response: {chat_response.content}")

    response = make_response(jsonify({
        "response" : chat_response.content
    }))

    response.status_code = 201
    response.headers['content-type'] = 'application/json'
    return response


@app.route("/products/embeddings", methods=['POST'])
def create_product_embeddings():
    product_profiles : list[str] = []
    docs : List[Document] = []
    
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)