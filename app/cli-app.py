# Import lib.py
import lib as glib

bedrock_kb = "K2NUJDLGRK" # Update your Amazon Bedrock Knowledge Bases ID here

# Initialize retriever and memory
retriever = glib.get_retriever(bedrock_kb)
memory = glib.get_memory()

while (True):
    input_text = input("User: ")

    # Get the LLM response
    chat_response = glib.get_rag_chat_response(
        input_text = input_text, 
        memory = memory, 
        retriever = retriever)
    answer = chat_response["result"]

    # Print the answer
    print(f"Assistant: {answer}")