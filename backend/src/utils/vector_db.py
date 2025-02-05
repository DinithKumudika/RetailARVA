from typing import List
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain.docstore.document import Document
from utils.rag_helper import RagHelper

class VectorDb:
    def __init__(self, url : str, api_key : str) -> None:
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
    
    def set_embedding_model(self):
        rag_helper = RagHelper()
        self.embeddings = rag_helper.get_embedding_model()

    def get_collection(self, collection: str) -> QdrantVectorStore:
        self.vector_store = QdrantVectorStore.from_existing_collection(
            collection_name=collection,
            url=self.url,
            api_key=self.api_key,
            embedding=self.embeddings,
            prefer_grpc=True
        )
        return self.vector_store
    
    def embed_documents(self, docs : List[Document], collection: str) -> QdrantVectorStore:
        qdrant = QdrantVectorStore.from_documents(
            docs,
            self.embeddings,
            url=self.url,
            prefer_grpc=True,
            api_key=self.api_key,
            collection_name=collection
        )
        self.vector_store = qdrant
    
    def get_point_ids_in_collection(self, collection: str, limit: int) -> list:
        record_ids = []
        scroll_result = self.vector_store.client.scroll(collection_name=collection, limit=limit)

        while scroll_result:
            record_ids.extend(point["id"] for point in scroll_result["points"])
            if not scroll_result["next_page"]:
                break
            scroll_result = self.vector_store.client.scroll(collection_name=collection, limit=limit)
        
        return record_ids
    
    def get_point_count_in_collection(self, collection: str) -> int | None:
        collection_info = self.vector_store.client.get_collection(collection)
        return collection_info.vectors_count

        