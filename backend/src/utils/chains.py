from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, \
    FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from src.utils.parsers import QuestionArrayOutputParser
from src.utils.prompts import product_suitability_prompt, recommendation_prompt, classification_prompt, system_prompt, greet_prompt, product_info_prompt, query_expansion_prompt, qa_system_prompt, response_parse_prompt
from src.utils.rag_helper import RagHelper

classification_examples = [
    {"query": "What are the ingredients in the [Brand B] moisturizer?", "category": "product_info"},
    {"query": "Is the [Product C] serum suitable for my sensitive skin?", "category": "suitability_check"},
    {"query": "What are some alternatives to the Acme Cleanser for oily skin?", "category": "recommendation"},
    {"query": "Does [Brand E] have any products for acne-prone skin?", "category": "recommendation"},
    {"query": "How do I apply the [Product G] cream?", "category": "product_info"},
    {"query": "Is this cream better than [Product J] for dry skin?", "category": "suitability_check"}
]

# Format Context
format_context = RunnableLambda(
    lambda docs: "\n".join([doc.page_content for doc in docs])
)

def get_greet_chain(model):
    greet_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", greet_prompt)
        ]
    )

    greet_chain = (
            {
                "user": RunnablePassthrough()
            }
            | greet_prompt_template
            | model
            | StrOutputParser()
    )

    return greet_chain

def get_expand_query_chain(model):

    q_expansion_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", query_expansion_prompt),
            ("user", "{query}"),
        ]
    )

    q_expansion_chain = (
        q_expansion_prompt_template
        | model
        | QuestionArrayOutputParser()
    )

    return q_expansion_chain

def get_enhanced_retrieval_chain(model):
    enhanced_retrieval_chain = (
        {
            "expanded_queries": get_expand_query_chain(model),
            "query": RunnablePassthrough()
        }
        | RunnableLambda(RagHelper.retrieve_for_all_queries)
        | RunnableLambda(RagHelper.process_docs)
        | format_context
    )
    return enhanced_retrieval_chain

def retrieve_documents_chain(retriever):
    """Chain for retrieving documents from the vector store."""
    return RunnableLambda(lambda expanded_query: retriever.invoke(expanded_query))

def deduplicate_and_rerank_chain():
    """Chain for deduplicating, reranking, and reordering retrieved documents."""
    return RunnableLambda(RagHelper.process_docs)

def get_qa_chain(model):
    """Chain for generating responses using the QA model."""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", f"{system_prompt} \n {qa_system_prompt}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{query}"),
        ]
    )
    return create_stuff_documents_chain(model, prompt=qa_prompt)

def get_default_chain(model):
    query_expansion_chain = get_expand_query_chain(model)

    # Retrieval chain
    retrieval_chain = (
            {
                "expanded_queries": query_expansion_chain,
                "query": lambda x: x["query"]
            }
            | RunnableLambda(RagHelper.retrieve_for_all_queries)
            | RunnableLambda(RagHelper.process_docs)
            | RunnableLambda(lambda x: RagHelper.get_formatted_products({
                "docs": x["processed_docs"]
            })["products"])
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", f"{system_prompt} \n {qa_system_prompt}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{query}"),
        ]
    )


    # Default chain expects "query" and "chat_history", adds "context"
    default_chain = (
            RunnablePassthrough.assign(context=retrieval_chain)
            | qa_prompt
            | model
            | StrOutputParser()
            | RunnableLambda(RagHelper.remove_markdown)
    )

    return default_chain


def classification_chain_invoke(model, query):

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{query}"),
            ("ai", "{category}")
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=classification_examples,
    )

    print("formatted few show prompt:\n")
    print(few_shot_prompt.format())

    classification_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", classification_prompt),
            few_shot_prompt,
            ("user", "{query}")
        ]
    )

    print(f"classification prompt:\n: {classification_prompt_template.format(query=query)}")

    classification_chain = classification_prompt_template | model | StrOutputParser()

    result: str = classification_chain.invoke({"query": query})
    return result.strip().lower()

def get_parse_response_chain(model):
    """Chain for parsing the model's response."""
    response_parse_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", response_parse_prompt),
            ("human", "{query}"),
        ]
    )

    response_parse_chain = (
        {
            "query": RunnablePassthrough()
        }
        | response_parse_prompt_template
        | model
        | StrOutputParser()
    )

    return response_parse_chain

def get_product_info_chain(model):

    product_info_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", f"{system_prompt}\n{product_info_prompt}"),
            MessagesPlaceholder("chat_history"),
            ("user", "{query}"),
        ]
    )

    product_info_chain = (
        {
            "product_info": lambda inputs: inputs["product_info"],
            "query": lambda inputs: inputs["query"],
            "chat_history": lambda inputs: inputs["chat_history"]
        }
        | product_info_prompt_template
        | model
        | StrOutputParser()
    )

    return product_info_chain


def get_suitability_chain(model):

    suitability_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", f"{system_prompt}\n{product_suitability_prompt}"),
            MessagesPlaceholder("chat_history"),
            ("user", "{query}"),
        ]
    )

    suitability_chain = (
        {
            "product_info": lambda inputs: inputs["product_info"],
            "user_info": lambda inputs: inputs["user_info"],
            "query": lambda inputs: inputs["query"],
            "chat_history": lambda inputs: inputs["chat_history"]
        }
        | suitability_prompt_template
        | model
        | StrOutputParser()
    )

    return suitability_chain

def get_recommendation_chain(model):

    recommendation_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", f"{system_prompt}\n{recommendation_prompt}"),
            MessagesPlaceholder("chat_history"),
            ("user", "{query}")
        ]
    )

    recommendation_chain = (
        {
            "product_info": lambda inputs: inputs["product_info"],
            "user_info": lambda inputs: inputs["user_info"],
            "query": lambda inputs: inputs["query"],
            "chat_history": lambda inputs: inputs["chat_history"],
            "context": RunnableLambda(lambda inputs: RagHelper.retrieve_recommendation(inputs)["context"]),
        }
        | recommendation_prompt_template
        | model
        | StrOutputParser()
    )

    return recommendation_chain



