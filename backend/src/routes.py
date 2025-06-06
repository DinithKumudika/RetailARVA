import os
from typing import List
from bson import ObjectId
from flask import jsonify, request, make_response, redirect, Blueprint, current_app as app
from flask_pymongo import PyMongo
from src.exceptions.exceptions import UserNotFoundError, ChatHistoryNotFoundError, ProductNotFoundError,UserProfileNotFoundError
from src.helpers.db import get_product_by_id, add_products, get_user_by_id, create_chat, add_chat_message, update_message_count, get_chat_history_by_chat_id, add_user, get_user_by_email, add_user_profile, get_user_profile_by_id, get_user_profile_by_user_id, update_user_profile
from src.utils.vector_db import VectorDb
from langchain.docstore.document import Document
from src.models.models import User, Chat, Message, UserProfile
from src.utils.chatbot import Chatbot
from src.helpers.import_json_to_mongo import load_from_json
import json

api_bp = Blueprint("api", __name__)



@api_bp.route("/", methods=['GET'])
def root():
    response = make_response(jsonify({
        "message" : "hello from RetailARVA API"
    }))

    response.status_code = 200
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/database", methods=['GET'])
async def test_db_connection():
    mongo : PyMongo = app.config.get('MONGO')
    
    response = make_response(jsonify({
        "message" : f"connected to {mongo.db.name}"
    }))

    response.status_code = 200
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/database/collections", methods=['GET'])
async def get_collections():
    mongo : PyMongo = app.config.get('MONGO')
    collections = mongo.db.list_collection_names()
    print("Collections in the database:")
    for collection in collections:
        print(collection)
    
    response = make_response(jsonify({
        "data": collections,
        "message" : f"{len(collections)} in the database"
    }))

    response.status_code = 200
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route('/gradio-app')
def redirect_to_gradio():
    return redirect(app.config.get('GRADIO_URL'), code=302)

@api_bp.route("/products", methods=['POST'])
async def add_products_from_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'data', 'products.json')

    try:
        products = load_from_json(json_path)
        # save_to_json("./src/data/products.json", products)

        ids = add_products(products)
        
        if len(ids) > 0:
            response = make_response(jsonify({
                "data" : ids,
                "message": f"{len(ids)} products successfully added"
            }))
            response.status_code = 201
    except FileNotFoundError:
        response = make_response(jsonify({
                "message" : f"product info source doesn't exist. {json_path}"
        }))
        response.status_code = 404        
    except Exception as ex:
        response = make_response(jsonify({
                "message" : f"something went wrong",
                "error": str(ex)
        }))
        response.status_code = 500
    response.headers['content-type'] = 'application/json'
    return response


@api_bp.route("/products/<product_id>", methods=['GET'])
def get_product_by_product_id(product_id: str):
    try:
        if product_id:
            product = get_product_by_id(int(product_id))
            response = make_response(jsonify({
                "data": product.to_dict(),
                "message": "product retieved successfully"
            }))
            response.status_code = 200
        else:
            response = make_response(jsonify({
                "message": "invalid request parameter"
            }))
            response.status_code = 400
    except ProductNotFoundError as ex:
        response = make_response(jsonify({
            "message": str(ex)
        }))
        response.status_code = 404
    except Exception:
        response = make_response(jsonify({
            "message": "something went wrong"
        }))
        response.status_code = 500

    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/users", methods=['POST'])
def add_new_user():
    try:
        data = request.get_json()
        if not data or 'first_name' not in data or 'last_name' not in data or 'email' not in data:
            response = make_response(jsonify({
                "error": "Invalid payload. Please provide 'first_name', 'last_name' and 'email'"
            }))
            response.status_code = 400
        
        user_id = add_user(User(
            first_name=data.get('first_name'), 
            last_name=data.get('last_name'),
            email=data.get('email')
        ))
        
        user = get_user_by_id(str(user_id))
        
        print(user.first_name)
        print(user.last_name)
        print(user.email)
        
        response = make_response(jsonify({
            "message": f"new user with id {str(user_id)} created",
            "data": User(
                _id=str(user.id) if user.id else None,  # Convert ObjectId to string
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                created_at=user.created_at,
            ).to_dict()
        }))
        response.status_code = 201  
    except UserNotFoundError as ex:
        response = make_response(jsonify({
            "message" : str(ex)
        }))
        response.status_code = 404
    except Exception as ex:
        print(str(ex))
        response = make_response(jsonify({
                "message" : "something went wrong"
        }))
        response.status_code = 500
        
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/users/login", methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            response = make_response(jsonify({
                "error": "Invalid payload. Please provide 'email'"
            }))
            response.status_code = 400
        email = data.get('email')    
        user = get_user_by_email(email)
        response = make_response(jsonify({
            "message": f"user with email: {email} retrieved successfully",
            "data": User(
                _id=str(user.id) if user.id else None,  # Convert ObjectId to string
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                created_at=user.created_at,
            ).to_dict()
        }))
        response.status_code = 200
    except UserNotFoundError as ex:
        response = make_response(jsonify({
            "message" : str(ex)
        }))
        response.status_code = 404
    except Exception as ex:
        print(str(ex))
        response = make_response(jsonify({
                "message" : "something went wrong"
        }))
        response.status_code = 500
        
    response.headers['content-type'] = 'application/json'
    return response

# @api_bp.route("/profile/<user_id>", methods=['POST'])
# def add_profile(user_id: str):
#     try:
#         if user_id:
#             data = request.get_json()
#             if not data or 'profileData' not in data:
#                 response = make_response(jsonify({
#                     "error": "Invalid payload."
#                 }))
#                 response.status_code = 400
#             profile_data = data.get('profileData')
#             user = get_user_by_id(user_id)

#             user_profile = UserProfile(
#                 user_id=user.id,
#                 age=profile_data.get('age'),
#                 gender=profile_data.get('gender'),
#                 skin_type=profile_data.get('skinType'),
#                 sensitive_skin=True if profile_data.get('sensitiveSkin') == "Yes" else False,
#                 skin_concerns=profile_data.get('skinConcerns'),
#                 ingredients_to_avoid=profile_data.get('ingredientsToAvoid'),
#                 known_allergies=profile_data.get('knownAllergies'),
#                 min_price=profile_data.get('minPrice'),
#                 max_price=profile_data.get('maxPrice'),
#                 preferences=profile_data.get('preferences')
#             )
#             user_profile_id = add_user_profile(user_profile)

#             response = make_response(jsonify({
#                 "message": f"new user profile with id {str(user_profile_id)} created",
#             }))
#             response.status_code = 201
#         else:
#             response = make_response(jsonify({
#                 "message" : "invalid request parameter"
#             }))
#             response.status_code = 400
#     except UserNotFoundError as ex:
#         response = make_response(jsonify({
#                 "message" : str(ex)
#         }))
#         response.status_code = 404
#     except Exception as ex:
#         print(ex)
#         response = make_response(jsonify({
#             "message": "something went wrong"
#         }))
#         response.status_code = 500
#     response.headers['content-type'] = 'application/json'
#     return response

@api_bp.route("/profile/<user_id>", methods=['GET'])
def get_user_profile(user_id: str):
    try:
        if user_id:
           user = get_user_by_id(user_id)
           user_profile = get_user_profile_by_id(str(user.id))
           response = make_response(jsonify({
               "data": user_profile.to_dict(),
               "message": f"user profile with for user {user_id} retrieved successfully"
           }))
           response.status_code = 200
        else:
            response = make_response(jsonify({
                "message": "invalid request parameter"
            }))
            response.status_code = 400
    except UserNotFoundError as ex:
        response = make_response(jsonify({
            "message" : str(ex)
        }))
        response.status_code = 404
    except UserProfileNotFoundError as ex:
        response = make_response(jsonify({
            "message" : f"User profile for user {user_id} not found"
        }))
        response.status_code = 404  # Profile not found should return 404
    except Exception as ex:
        print(ex)
        response = make_response(jsonify({
                "message" : "something went wrong"
        }))
        response.status_code = 500
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/users/<user_id>", methods=['GET'])    
def get_user_by_user_id(user_id: str):
    try:
        if user_id:
            user = get_user_by_id(user_id)
            response = make_response(jsonify({
                "data" : User(
                    _id=str(user.id) if user.id else None,  # Convert ObjectId to string
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    created_at=user.created_at,
                ).to_dict(),
                "message": f"user with id {user_id} retieved successfully"
            }))
            response.status_code = 200 
        else:
            response = make_response(jsonify({
                "message" : "invalid request parameter"
            }))
            response.status_code = 400
    except UserNotFoundError as ex:
        response = make_response(jsonify({
            "message" : str(ex)
        }))
        response.status_code = 404
    except Exception as ex:
        print(ex)
        response = make_response(jsonify({
                "message" : "something went wrong"
        }))
        response.status_code = 500
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/chat/new/<user_id>", methods=['POST'])
def create_new_chat(user_id: str):
    chat: Chatbot = app.config['CHAT']()
    try:
        if user_id:
            user = get_user_by_id(user_id)
            chat_id = create_chat(Chat(user_id=user_id))

            chat.session_id = str(chat_id)
            chat.set_chat_session()

            response = chat.greet(user.first_name)
            message_id = add_chat_message(
                Message(
                    chat_id=chat_id, 
                    role="assistant", 
                    content=response,
                    message_id=1
                )
            )

            print(chat_id)

            is_updated = update_message_count(chat_id=str(chat_id), count=1)

            if is_updated:
                response = make_response(jsonify({
                    "data" : Message(
                            _id=message_id, 
                            chat_id=chat_id, 
                            content=response, 
                            role="assistant", 
                            message_id=1
                        ).to_dict(),
                    "message": f"chat session with chat id {chat_id} created successfully"
                }))
                response.status_code = 201    
            else:
                response = make_response(jsonify({
                    "message" : "something went wrong"
                }))
                response.status_code = 500                
    except UserNotFoundError as ex:
        response = make_response(jsonify({
                "message" : str(ex)
        }))
        response.status_code = 404
    except Exception as ex:
        response = make_response(jsonify({
                "message" : f"something went wrong, {str(ex)}"
        }))
        response.status_code = 500
    response.headers['content-type'] = 'application/json'
    return response  
        

@api_bp.route("/chat/<chat_id>", methods=['POST'])
def chat_with_assistant(chat_id: str):
    chat_id = chat_id.strip()  # Fix: remove extra spaces
    try:
        if chat_id:
            chat: Chatbot = app.config['CHAT']()
            
            request_data = request.get_json()
            user_id = request_data.get('user_id')
            product_id = request_data.get('product_id')
            query = request_data.get('message')
            role = request_data.get('role')
            
            print(f"user query: {query}")

            chat_history = get_chat_history_by_chat_id(chat_id=chat_id)

            chat.session_id = chat_id
            chat.set_chat_session()

            response = chat.invoke(query=query, user_id = user_id, product_id=product_id)
            
            print(f"chat response: {response}")
            
            add_chat_message(Message(
                role=role, 
                content=query, 
                chat_id=ObjectId(chat_id), 
                message_id=len(chat_history) + 1
            ))
            
            message_id = add_chat_message(Message(
                role="assistant", 
                content=response, 
                chat_id=ObjectId(chat_id), 
                message_id=len(chat_history) + 2
            ))

            chat_history = get_chat_history_by_chat_id(chat_id=chat_id)
            is_updated = update_message_count(chat_id=chat_id, count=len(chat_history))

            if is_updated:
                response = make_response(jsonify({
                    "data": Message(
                            _id=message_id,
                            chat_id=ObjectId(chat_id),
                            role="assistant",
                            content=response,
                            message_id=len(chat_history) + 2
                        ).to_dict(),
                    "message" : f"message with id {message_id} added to the chat {chat_id}"
                }))
                response.status_code = 201
    except ChatHistoryNotFoundError as ex:
        response = make_response(jsonify({
                "message" : str(ex)
        }))
        response.status_code = 404
    except Exception as ex:
        print(str(ex))
        response = make_response(jsonify({
                "message" : f"something went wrong, {str(ex)}"
        }))
        response.status_code = 500
    response.headers['content-type'] = 'application/json'
    return response

@api_bp.route("/products/embeddings", methods=['POST'])
def create_product_embeddings():
    product_profiles : list[str] = []
    docs : List[Document] = []
    qdrant : VectorDb = app.config['QDRANT']()

    # read data from product_descriptions.json to a list
    with open("./src/data/product_descriptions.json", "r") as f:
        product_descriptions = json.load(f)
        print(product_descriptions)
    
    for product in product_descriptions:

        docs.append(
            Document(
                page_content=product["content"],
                metadata={
                    "id": product["id"],
                    "product name": product["metadata"]["name"],
                    "product brand": product["metadata"]["brand"],
                    "product category": product["metadata"]["category"],
                    "price": product["metadata"]["price"]
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
    return response

@api_bp.route("/profile/<user_id>", methods=['POST'])
def add_or_update_profile(user_id: str):
    try:
        if not user_id:
            response = make_response(jsonify({
                "message": "invalid request parameter"
            }))
            response.status_code = 400
            return response

        data = request.get_json()
        if not data or 'profileData' not in data:
            response = make_response(jsonify({
                "error": "Invalid payload."
            }))
            response.status_code = 400
            return response

        profile_data = data.get('profileData')
        user = get_user_by_id(user_id)

        # Check if profile already exists
        existing_profile = get_user_profile_by_user_id(user_id)

        if existing_profile:
            # Update existing profile
            existing_profile.age = profile_data.get('age')
            existing_profile.gender = profile_data.get('gender')
            existing_profile.skin_type = profile_data.get('skinType')
            existing_profile.sensitive_skin = True if profile_data.get('sensitiveSkin') == "Yes" else False
            existing_profile.skin_concerns = profile_data.get('skinConcerns')
            existing_profile.ingredients_to_avoid = profile_data.get('ingredientsToAvoid')
            existing_profile.known_allergies = profile_data.get('knownAllergies')
            existing_profile.min_price = profile_data.get('minPrice')
            existing_profile.max_price = profile_data.get('maxPrice')
            existing_profile.preferences = profile_data.get('preferences')

            update_user_profile(existing_profile)

            response = make_response(jsonify({
                "message": f"user profile with id {str(existing_profile.id)} updated",
            }))
            response.status_code = 200
        else:
            # Create new profile
            user_profile = UserProfile(
                user_id=user.id,
                age=profile_data.get('age'),
                gender=profile_data.get('gender'),
                skin_type=profile_data.get('skinType'),
                sensitive_skin=True if profile_data.get('sensitiveSkin') == "Yes" else False,
                skin_concerns=profile_data.get('skinConcerns'),
                ingredients_to_avoid=profile_data.get('ingredientsToAvoid'),
                known_allergies=profile_data.get('knownAllergies'),
                min_price=profile_data.get('minPrice'),
                max_price=profile_data.get('maxPrice'),
                preferences=profile_data.get('preferences')
            )
            user_profile_id = add_user_profile(user_profile)

            response = make_response(jsonify({
                "message": f"new user profile with id {str(user_profile_id)} created",
            }))
            response.status_code = 201

    except UserNotFoundError as ex:
        response = make_response(jsonify({
            "message": str(ex)
        }))
        response.status_code = 404
    except Exception as ex:
        print(ex)
        response = make_response(jsonify({
            "message": "something went wrong"
        }))
        response.status_code = 500

    response.headers['content-type'] = 'application/json'
    return response
