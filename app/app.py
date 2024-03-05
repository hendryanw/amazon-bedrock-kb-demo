import streamlit as st 
import lib as glib
import s3_uri_helper as s3_helper

bedrock_kb = "K2NUJDLGRK" # Update your Amazon Bedrock Knowledge Bases ID here
retriever = glib.get_retriever(bedrock_kb)

if 'memory' not in st.session_state:
    st.session_state.memory = glib.get_memory()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Set the page title
st.set_page_config(page_title="Intelligent Document Q&A Powered by Amazon Bedrock Knowledge Bases")
st.title("Intelligent Document Q&A Powered by Amazon Bedrock Knowledge Bases")

# Print the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): 
        st.markdown(message["text"]) 

# Textbox to input user question
input_text = st.chat_input("Chat with your bot here") 

# The following code are executed when the question is submitted
if input_text: 
    # Display the user question in the chat interface and store it in the chat history
    with st.chat_message("user"):
        st.markdown(input_text)

    st.session_state.chat_history.append({"role": "user", "text": input_text})
    
    # Get the LLM response
    chat_response = glib.get_rag_chat_response(
        input_text = input_text, 
        memory = st.session_state.memory, 
        retriever = retriever)
    answer = chat_response["result"]
    
    # Display the LLM response in the chat interface
    # Also display the source documents URLs and snippets
    with st.chat_message("assistant"):
        st.markdown(answer)
        with st.expander(label = "View source documents"): #display the references
            url_count = 0
            for document in chat_response['source_documents']:
                url_count = url_count + 1
                metadata = document.metadata
                s3_presigned_url, bucket_name, object_key = s3_helper.generate_presigned_url(metadata['location']['s3Location']['uri'])
                st.markdown('**[**' + f"**{url_count}**" + '**]**' + ' ' + f"**[{object_key}]({s3_presigned_url})**" + '  \n' + document.page_content[:250])
    
    # Store the LLM answer in the chat history
    st.session_state.chat_history.append({"role": "assistant", "text": answer})