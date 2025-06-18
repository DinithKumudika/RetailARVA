from typing import List
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain.docstore.document import Document
from src.utils.rag_helper import RagHelper

class VectorDb:
    """
    A class to interact with a Qdrant vector database using LangChain's Qdrant integration.
    Provides methods to manage collections, embed documents, and retrieve data.
    """
    def __init__(self, url : str, api_key : str| None = None) -> None:
        """
        Initialize the VectorDb instance.

        Args:
            url (str): The URL of the Qdrant server.
            api_key (Optional[str]): The API key for authentication (if required).
        """
        if not url or not api_key:
            raise ValueError("QDRANT_CLUSTER_URL and QDRANT_API_KEY are required.")

        self.embeddings = None
        self.url = url
        self.api_key = api_key
        self.vector_store = None

    # def get_collection(self, collection: str):
    #     self.vector_store = QdrantVectorStore(
    #         client=QdrantClient(url=self.url, api_key=self.api_key, prefer_grpc=True),
    #         collection_name=collection,
    #         embedding=self.embeddings
    #     )
    #     return self.vector_store
    
    def set_embedding_model(self, embedding_model = None):
        """
        Set the embedding model for vectorizing documents.

        If no embedding model is provided, it uses the default model from RagHelper.

        Args:
            embedding_model (Optional): A custom embedding model. Defaults to None.
        Raises:
            ValueError: If the embedding model is not set.
        """
        if embedding_model:
            self.embeddings = embedding_model
            print(f"embedding model: {self.embeddings.model}")
        else:
            rag_helper = RagHelper()
            self.embeddings = rag_helper.get_embedding_model()
            print(f"embedding model: {self.embeddings.model}")
            
        if self.embeddings is None:
            raise ValueError("Failed to set embedding model. Ensure RagHelper or custom model is configured correctly.")

    def get_collection(self, collection: str) -> QdrantVectorStore:
        """
        Connect to an existing Qdrant collection.

        Args:
            collection (str): The name of the collection to connect to.

        Returns:
            QdrantVectorStore: A QdrantVectorStore instance connected to the specified collection.

        Raises:
            ValueError: If the collection does not exist or the embedding model is not set.
        """
        if self.embeddings is None:
            raise ValueError("Embedding model is not set. Call `set_embedding_model` first.")

        if not self.url or not self.api_key:
            raise ValueError("QDRANT_CLUSTER_URL and QDRANT_API_KEY are required.")

        print(f"Qdrant Api key: {self.api_key}")
        print(f"Qdrant URL: {self.url}")
        
        try:
            self.vector_store = QdrantVectorStore.from_existing_collection(
                collection_name=collection,
                url="https://27c6018a-d381-49b4-aef4-e922ce3eea85.us-west-2-0.aws.cloud.qdrant.io",
                https=True,
                api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.BqanaVupoaZV3GGVQGA5nOdGT3kHQDzOWJZC476Ruh0",
                embedding=self.embeddings,
                prefer_grpc=False
            )
            return self.vector_store
        except Exception as e:
            raise ValueError(f"Failed to connect to collection '{collection}': {e}, qdrant url={self.url}, embeddings= {self.embeddings.model}")
    
    def embed_documents(self, docs : List[Document], collection: str) -> QdrantVectorStore:
        """
        Embed a list of documents into a Qdrant collection.

        If the collection does not exist, it will be created.

        Args:
            docs (List[Document]): A list of Document objects to embed.
            collection (str): The name of the collection to store the documents in.

        Returns:
            QdrantVectorStore: A QdrantVectorStore instance connected to the updated collection.

        Raises:
            ValueError: If the embedding model is not set or if embedding fails.
        """
        if self.embeddings is None:
            raise ValueError("Embedding model is not set. Call `set_embedding_model` first.")

        print(f"Qdrant Api key: {self.api_key}")
        print(f"Qdrant URL: {self.url}")
        
        try:
            qdrant = QdrantVectorStore.from_documents(
                docs,
                self.embeddings,
                url="https://fdda17ab-8e55-4273-a1b2-61227eaf0835.europe-west3-0.gcp.cloud.qdrant.io",
                prefer_grpc=False,
                https=True,
                api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.iB5o-6sSQPdGDJfljEvc9cV73H7dy-0AmByR9-VBVN4",
                collection_name=collection
            )
            self.vector_store = qdrant
            return qdrant
        except Exception as e:
            raise ValueError(f"Failed to embed documents into collection '{collection}': {e}")
    
    def get_point_ids_in_collection(self, collection: str, limit: int) -> list:
        """
        Retrieve the IDs of points (vectors) in a Qdrant collection.

        Uses pagination to handle large collections.

        Args:
            collection (str): The name of the collection.
            limit (int): The maximum number of points to retrieve per page. Defaults to 100.

        Returns:
            List[str]: A list of point IDs in the collection.

        Raises:
            ValueError: If the vector store is not initialized or if scrolling fails.
        """
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Call `get_collection` or `embed_documents` first.")
        
        record_ids = []
        try:
            scroll_result = self.vector_store.client.scroll(collection_name=collection, limit=limit)

            while scroll_result:
                record_ids.extend(point["id"] for point in scroll_result["points"])
                if not scroll_result["next_page"]:
                    break
                scroll_result = self.vector_store.client.scroll(collection_name=collection, limit=limit)
        except Exception as e:
            raise ValueError(f"Failed to retrieve point IDs from collection '{collection}': {e}")
        
        return record_ids
    
    def get_point_count_in_collection(self, collection: str) -> int | None:
        """
        Get the total number of vectors (points) in a Qdrant collection.

        Args:
            collection (str): The name of the collection.

        Returns:
            Optional[int]: The total number of vectors in the collection, or None if retrieval fails.

        Raises:
            ValueError: If the vector store is not initialized or if the collection info cannot be retrieved.
        """
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Call `get_collection` or `embed_documents` first.")
        try:
            collection_info = self.vector_store.client.get_collection(collection)
            return collection_info.vectors_count
        except Exception as e:
            raise ValueError(f"Failed to retrieve point count for collection '{collection}': {e}")
        
