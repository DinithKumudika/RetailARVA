from langchain_ollama.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from markdownify import markdownify as md
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_transformers import (
     LongContextReorder
)
from flask import current_app as app
from sentence_transformers import CrossEncoder
from src.helpers.db import get_product_by_id, get_user_profile_by_user_id
from src.templates import user_profile, product_profile
from jinja2 import Template


class RagHelper:
    @staticmethod
    def get_classification_model():
        return ChatGoogleGenerativeAI(
            model=app.config.get('CLASSIFICATION_MODEL_ID'),
            google_api_key=app.config.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'),
            temperature=0.0,
            convert_system_message_to_human=True
        )

    @staticmethod
    def get_recommendation_model():
        return ChatOllama(
            base_url=app.config.get('OLLAMA_URL'),
            model=app.config.get('RECOMMENDATION_MODEL_ID'),
            temperature=0.5
        )

    @staticmethod
    def get_tts_input_model():
        return ChatOllama(
            base_url=app.config.get('OLLAMA_URL'),
            model=app.config.get('TTS_INPUT_PARSER_MODEL_ID'),
            temperature=0.0
        )

    @staticmethod
    def retrieve_for_all_queries(inputs: dict):
        """Retrieve documents for all expanded queries."""
        expanded_queries = inputs["expanded_queries"]
        query = inputs["query"]
        vector_store = RagHelper.get_vector_store('products')
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        all_docs = []
        for expanded_query in expanded_queries:
            print(f"Retrieving documents for query: {expanded_query}")
            try:
                retrieved_docs = retriever.invoke(expanded_query)
                print(f"Number of retrieved docs for query: {len(retrieved_docs)}")
                all_docs.extend(retrieved_docs)
            except Exception as e:
                print(f"Error during retriever.invoke(): {e}")

        return {"docs": all_docs, "query": query}

    @staticmethod
    def rerank_n_reorder(query, docs):
        unique_contents = set()

        unique_docs = []
        for doc in docs:
            if doc.page_content not in unique_contents:
                unique_docs.append(doc)
                unique_contents.add(doc.page_content)

        # Create query-document pairs for reranking
        pairs = [[query, doc.page_content] for doc in unique_docs]
        scores = RagHelper.get_cross_encoder().predict(pairs)

        # Sort documents by their scores
        scored_docs = zip(scores, unique_docs)
        sorted_docs = sorted(scored_docs, reverse=True)

        # Get top 5 documents
        reranked_docs = [doc for _, doc in sorted_docs][:5]

        # Reorder documents to address "lost in the middle" problem
        reordering = LongContextReorder()
        reordered_docs = reordering.transform_documents(reranked_docs)

        return {"processed_docs": reordered_docs}

    @staticmethod
    def process_docs(inputs):
        """Helper function to deduplicate, rerank, and reorder documents."""
        docs = inputs["docs"]
        query = inputs["query"]

        reordered_docs = RagHelper.rerank_n_reorder(query, docs)
        return {"processed_docs": reordered_docs["processed_docs"]}

    @staticmethod
    def get_formatted_user_profile(user_id: str) -> str | None:

        profile = get_user_profile_by_user_id(user_id)

        if profile:
            skin_concerns = "not specified" if not profile.skin_concerns else ", ".join(profile.skin_concerns)
            ingredients_to_avoid = "not specified" if not profile.ingredients_to_avoid else ", ".join(
                profile.ingredients_to_avoid)
            known_allergies = "not specified" if not profile.known_allergies else ", ".join(profile.known_allergies)
            preferences = "not specified" if not profile.preferences else ", ".join(profile.preferences)

            user_profile_template=Template(user_profile)

            user_profile_summary = user_profile_template.render({
                "age": profile.age,
                "gender": profile.gender,
                "skin_type": profile.skin_type,
                "sensitive": "Yes" if profile.sensitive_skin else "No",
                "skin_concerns": skin_concerns,
                "min_price": profile.min_price,
                "max_price": profile.max_price,
                "preferences": preferences,
                "ingredients_to_avoid": ingredients_to_avoid,
                "known_allergies": known_allergies
            })
            return user_profile_summary
        return None

    @staticmethod
    def get_formatted_product(product_id):
        product = get_product_by_id(product_id)
        if product is None:
            return None

        key_ingredients = "not specified" if product.key_ingredients is None or len(
            product.key_ingredients) == 0 else ", ".join(product.key_ingredients)
        concentrations = "not specified" if product.concentrations is None or len(
            product.concentrations) == 0 else ", ".join(product.concentrations)
        ingredients = "not specified" if product.ingredients is None or len(product.ingredients) == 0 else ", ".join(
            product.ingredients)
        benefits = "not specified" if product.benefits is None or len(product.benefits) == 0 else ", ".join(
            product.benefits)
        claims = "not specified" if product.claims is None or len(product.claims) == 0 else ", ".join(product.claims)
        skin_types = "not specified" if product.skin_types is None or len(product.skin_types) == 0 else ", ".join(
            product.skin_types)
        skin_concerns = "not specified" if product.skin_concerns is None or len(
            product.skin_concerns) == 0 else ", ".join(product.skin_concerns)
        potential_side_effects = "not specified" if product.side_effects is None or len(
            product.side_effects) == 0 else ", ".join(product.side_effects)
        allergens = "not specified" if product.allergens is None or len(product.allergens) == 0 else ", ".join(
            product.allergens)

        product_profile_template = Template(product_profile)

        profile = product_profile_template.render({
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "price": product.price,
            "is_natural": "natural" if product.is_natural else "not natural",
            "key_ingredients": key_ingredients,
            "concentrations": concentrations,
            "ingredients": ingredients,
            "benefits": benefits,
            "claims": claims,
            "usage": product.usage,
            "application_tips": product.application_tips,
            "skin_types": skin_types,
            "skin_concerns": skin_concerns,
            "for_sensitive_skin": product.for_sensitive_skin,
            "side_effects": potential_side_effects,
            "allergens": allergens,
            "average_rating": product.average_rating,
            "customer_reviews": product.customer_reviews,
            "expert_review": product.expert_review
        })

        return profile

    @staticmethod
    def get_formatted_products(inputs: dict):
        docs = inputs["docs"]
        products = []
        for doc in docs:
            product_id = doc.metadata["id"]
            profile = RagHelper.get_formatted_product(product_id)
            products.append(profile)

        # Join all product profiles into a single string
        product_str = "\n".join(products)
        return {"products": product_str}

    @staticmethod
    def get_llm():
        if app.config.get('USE_OLLAMA'):
            return ChatOllama(
                base_url = app.config.get('OLLAMA_URL'),
                model = app.config.get('OLLAMA_MODEL_ID'),
                temperature = 0.5
            )
        elif app.config.get('USE_GEMINI'):
            return ChatGoogleGenerativeAI(
                model= app.config.get('GEMINI_MODEL_ID'),
                google_api_key= app.config.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'),
                temperature=0.5,
                convert_system_message_to_human=True
            )
        elif app.config.get('USE_GROQ'):
            return ChatGroq(
                model= app.config.get('GROQ_MODEL_ID'),
                api_key= app.config.get('GROQ_API_KEY'),
                temperature=0.5,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

    @staticmethod
    def retrieve_recommendation(inputs):
        product_info = inputs["product_info"]
        user_info = inputs["user_info"]
        query = inputs["query"]
        vector_store = RagHelper.get_vector_store('products')

        product_docs_1 = RagHelper.get_retriever(vector_store, 5).invoke(product_info)
        print(f"Retrieved {len(product_docs_1)} docs using product_info")

        product_docs_2 = RagHelper.get_retriever(vector_store, 3).invoke(user_info)
        print(f"Retrieved {len(product_docs_2)} docs using user_info")

        combined_docs = product_docs_1 + product_docs_2

        reordered_docs = RagHelper.rerank_n_reorder(query, combined_docs)

        context = RagHelper.get_formatted_products({"docs": reordered_docs["processed_docs"]})["products"]
        return {"context": context}


    @staticmethod
    def get_embedding_model():
        if app.config.get('USE_OLLAMA_EMBEDDING'):
            print(f"using ollama embedding: {app.config.get('OLLAMA_EMBEDDING_MODEL_ID')}")
            return OllamaEmbeddings(
                base_url= app.config.get('OLLAMA_URL'),
                model= app.config.get('OLLAMA_EMBEDDING_MODEL_ID')
            )
        elif app.config.get('USE_GOOGLE_EMBEDDING'):
            return GoogleGenerativeAIEmbeddings(
                model= app.config.get('GEMINI_EMBEDDING_MODEL_ID'),
                google_api_key= app.config.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
            )
        elif app.config.get('USE_HUGGINGFACE_EMBEDDING'):
            return HuggingFaceBgeEmbeddings(
                model_name= app.config.get('HUGGINGFACE_EMBEDDING_MODEL_ID'),
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )

    @staticmethod
    def get_vector_store(collection_name: str):
        qdrant = app.config['QDRANT']()
        return qdrant.get_collection(collection_name)

    @staticmethod
    def get_retriever(vector_store: QdrantVectorStore, search_k: int):
        return vector_store.as_retriever(search_kwargs={"k": search_k})

    @staticmethod
    def get_cross_encoder():
        return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    @staticmethod
    def remove_markdown(response: str) -> str:
        """Utility function to remove markdown from the response"""
        return md(response)

    @staticmethod
    def filter_product_info_inputs(inputs: dict) -> dict:
        return {
            "query": inputs["query"],
            "product_info": inputs["product_info"],
            "chat_history": inputs.get("chat_history", []),  # in case it's injected later
        }
        