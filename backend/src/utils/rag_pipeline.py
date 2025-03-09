from typing import List
from sentence_transformers import CrossEncoder
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_community.document_transformers import (
     LongContextReorder
)
from markdownify import markdownify as md

from src.utils.prompts import contextualize_q_system_prompt, system_prompt, qa_system_prompt, query_expansion_prompt
from src.utils.parsers import QuestionArrayOutputParser


class RagPipeline:
     def __init__(self, vector_store: QdrantVectorStore, search_k: int, model, embedding_model):
          self.cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
          self.vector_store = vector_store
          self.search_k = search_k
          self.retriever = vector_store.as_retriever(search_kwargs={"k": search_k})
          self.model = model
          self.embedding_model = embedding_model
          self.history_aware_retriever = None
          self.qa_chain = None
          self.rag_chain = None
     
     def set_history_aware_retriever(self):
          contextualize_q_prompt = ChatPromptTemplate.from_messages(
               [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
               ]
          )
          self.history_aware_retriever = create_history_aware_retriever(
               self.model,
               self.retriever,
               contextualize_q_prompt
          )
          
     def remove_markdown(self, response: str) -> str:
          return md(response)
          
     def set_qa_chain(self):
          
          qa_prompt = ChatPromptTemplate.from_messages(
               [
                    ("system", f"{system_prompt} \n {qa_system_prompt}"),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
               ]
          )
          self.qa_chain = create_stuff_documents_chain(self.model, prompt=qa_prompt)
     
     def set_rag_chain(self):
          self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.qa_chain)
          
     def expand_query(self, query: str) -> List[str]:
          q_expansion_prompt = PromptTemplate(
               input_variables=["query"],
               template=query_expansion_prompt,
          )
          q_expansion_chain = q_expansion_prompt | self.model | QuestionArrayOutputParser()
          queries = q_expansion_chain.invoke(query)
          
          return queries
     
     def invoke(self, query: str, chat_history: list):
          queries = self.expand_query(query)
          
          print("<----------------------- Expanded Queries ------------------------------------>")
          for expanded_query in queries:   
               print(expanded_query)
          print("<------------------------------------------------------------------------------>")     

          
          docs = []
          
          for expanded_query in queries:
               print(f"retrieving documents for query: {expanded_query}...")
               try:
                    retrieved_docs = self.retriever.invoke(expanded_query)
                    # response = self.vector_store.client.query_points(
                    #      collection_name="products",
                    #      query= self.embedding_model.embed_documents([expanded_query]),
                    #      limit=self.search_k
                    # )
                    print(f"no of retrieved docs for query: {len(retrieved_docs)}")
                    docs.append(retrieved_docs)
               except Exception as e:
                    print(f"Error during retriever.invoke(): {e}")
                    print(f"Type of error: {type(e)}")
                    print(f"Error details: {e.args}")
                    
          print(docs)
          
          for sublist in docs:
               for doc in sublist:
                    print(doc.metadata)
          
          # Remove duplicate retrievals

          unique_contents = set()
          unique_docs = []
          for sublist in docs:
               for doc in sublist:
                    if doc.page_content not in unique_contents:
                         unique_docs.append(doc)
                         unique_contents.add(doc.page_content)
          unique_contents = list(unique_contents)
          print(f"{len(unique_contents)} unique docs retrieved from query expansion")
          
          # create query and retrieved document pairs for reranking
          pairs = []
          for doc in unique_contents:
               pairs.append([query, doc])
          
          scores = self.cross_encoder.predict(pairs)
          print(f"scores from cross encoder for {len(unique_contents)} docs: {scores}")
          
          # sort documents by their scores
          scored_docs = zip(scores, unique_contents)
          sorted_docs = sorted(scored_docs, reverse=True)
          
          # Get top 5 documents
          reranked_docs = [doc for _, doc in sorted_docs][0:5]
          reranked_docs
          
          # address lost in the middle by reordering
          reordering = LongContextReorder()
          reordered_docs = reordering.transform_documents(reranked_docs)
          
          # Convert reordered_docs (strings) back to Document objects
          reordered_docs = [Document(page_content=doc) for doc in reordered_docs]
          
          response = self.qa_chain.invoke({
               "input": query, 
               "context": reordered_docs,
               "chat_history": chat_history
          })
          
          return self.remove_markdown(response)
