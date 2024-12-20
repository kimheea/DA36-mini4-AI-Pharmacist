from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
import os

load_dotenv()

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


def dur_pregnacy_similarity(query):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    dur_vector_db = PineconeVectorStore(
        embedding=embeddings,
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        namespace=os.getenv("PINECONE_NAMESPACE"),
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
    )

    results = dur_vector_db.similarity_search(
        query=query,
        k=5,
        namespace=os.getenv("PINECONE_NAMESPACE"),)

    return {
        "medicine_name": query,
        "dur_context": "\n".join([doc.page_content for doc in results])
    }


from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


def drug_info_similarity(query):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    dur_vector_db = PineconeVectorStore(
        embedding=embeddings,
        index_name=os.getenv("PINECONE_INDEX_NAME_2"),
        namespace=os.getenv("PINECONE_NAMESPACE_2"),
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
    )

    results = dur_vector_db.similarity_search(
        query=query,
        k=5,
        namespace=os.getenv("PINECONE_NAMESPACE_2"))

    return {
        "medicine_context": "\n".join([doc.page_content for doc in results])
    }

# 각 딕셔너리를 합쳐 하나의 딕셔너리 반환
def merge_dict(query):
    dict1 = dur_pregnacy_similarity(query)
    dict2 = drug_info_similarity(query)
    merged_dict = dict1 | dict2
    return merged_dict


def generate_prompt(medicine_name, medicine_context, dur_context):
    return ChatPromptTemplate.from_messages([
        ('system', """
        Persona: You are a knowledgeable and experienced pharmacist with a passion to help people. 

        Role: As a pharmacist, your role is to provide simple and clear explanations about medicines for maternity.

        Examples:
        Your explanation should cover the following:

        1. A brief explanation of the medicine, its effectiveness, dosage, precautions, side effects, and storage information.
        2. If the medicine is safe for pregnant women, including any contraindications, warning levels, and what they mean.

        Use the context provided below to answer the user's query.
        """),
        ('user', f"""
        주어진 맥락에 사용하여 질문에 답변을 하되, 모르는 경우 모른다고 말하며 최대한 세문장으로 간결하게 한국말로 답변해주세요.
        Use the following pieces of retrieved context to answer the 
        Context about the medicine:
        {medicine_context}

        Context about the pregnancy-related contraindications:
        {dur_context}

        Medicine name: {medicine_name}
        """)
    ])


def ai_pharmacist(question, merged_dict):
    prompt = generate_prompt(
        medicine_name=merged_dict['medicine_name'],
        medicine_context=merged_dict['medicine_context'],
        dur_context=merged_dict['dur_context']
    )

    messages = prompt.format_messages()

    model = ChatOpenAI(model='gpt-4o', temperature=1)

    # RunnableLambda를 사용하여 모델 호출
    pipeline = RunnableLambda(lambda x: model.invoke(messages))

    # 질문을 파이프라인에 전달
    result = pipeline.invoke(question)
    return result.stream({})
