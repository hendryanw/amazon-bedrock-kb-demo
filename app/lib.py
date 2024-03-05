from langchain.llms.bedrock import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever

from langchain.chains import RetrievalQA
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Initialize Bedrock LLM
llm = Bedrock(
    model_id = "anthropic.claude-instant-v1",
    region_name = "us-east-1",
    model_kwargs = {
        "max_tokens_to_sample": 3000, 
        "temperature": 0, 
        "top_k": 10
    })

# Amazon Bedrock Knowledge Bases Retriever
def get_retriever(bedrock_kb_id):
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id = bedrock_kb_id,
        region_name = "us-east-1",
        retrieval_config = {
            "vectorSearchConfiguration": {
                "numberOfResults": 3 # Number of document search results
            }
        })
    return retriever

# LangChain conversation memory allows the application to consider past conversation when answering questions.
def get_memory():
    memory = ConversationBufferWindowMemory(
        memory_key = "chat_history", 
        input_key = "question",
        human_prefix = "user",
        ai_prefix = "assistant",
        k = 10, #number of messages to store in buffer
        return_messages = True) 
    return memory
    
# Get the response from LLM using the context retrieved from Amazon Bedrock Knowledge Bases
def get_rag_chat_response(input_text, memory, retriever):
    system_template = '''
You are an intelligent document assistant.
You are polite and helpful.

Given the specific context, please give a concise answer to the question.
You can find the context enclosed in <context> tag below.
<context>
{context}
</context>
Do not hallucinate. You must say that you don't know if you can't find the answer within the context.

However, you should also respond to user greetings without having to look at the context.

You can find the chat history enclosed in <chat_history> tag below. Consider the past conversation when answering the question.
<chat_history>
{chat_history}
</chat_history>
'''
    user_template = "Question: ```{question}```"
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(user_template)
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    retrieval_qa = RetrievalQA.from_chain_type(
        llm = llm,
        retriever = retriever,
        return_source_documents = True,
        chain_type_kwargs = {
            "prompt": prompt,
            "memory": memory
        }
    )

    qa_response = retrieval_qa.invoke({"query": input_text})
    return qa_response