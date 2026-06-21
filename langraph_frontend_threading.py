import streamlit as st
from langraph_backend import chatbot
from langchain_core.messages import HumanMessage
#session state=store message 
import uuid

#utility finvction
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id);
##sessin state

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

#sidebar ui
st.sidebar.title('Langraph chatbot')
if st.sidebar.button('new chat'):
    reset_chat()

st.sidebar.header('myconverstation')  
st.sidebar.text(st.session_state['thread_id'])  


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input('Type here') 

if user_input:

    st.session_state['message_history'].append({'role':'user','content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG={'configurable':{'thread_id': st.session_state['thread_id']}}

    # response=chatbot.invoke({"messages": [HumanMessage(content=user_input)]},config=CONFIG)
    # ai_message=response['messages'][-1].content

    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
          

    st.session_state['message_history'].append({'role':'assistant','content': ai_message})