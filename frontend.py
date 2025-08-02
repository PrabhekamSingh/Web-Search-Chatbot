import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage


# Sidebar navigation
page = st.sidebar.radio(
    "Choose a page",
    ("Chatbot", "About")
)

if page == "Chatbot":
    st.title("Web Search Chatbot")

    # Initialize message history
    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = []

    # Display conversation history
    for message in st.session_state['message_history']:
        with st.chat_message(message['role']):
            st.text(message['content'])

    # Chat input
    user_input = st.chat_input('Type here')

    if user_input:
        # Add user message to history and display
        st.session_state['message_history'].append({'role': 'user', 'content': user_input})
        with st.chat_message('user'):
            st.text(user_input)
        
        # Get bot response
        with st.spinner("Thinking..."):
            response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config={'configurable': {'thread_id': 'thread-1'}})
            ai_message = response['messages'][-1].content
        
        # Add bot message to history and display
        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
        with st.chat_message('assistant'):
            st.text(ai_message)

elif page == "About":
    st.title("About")
    st.write("This is a Gemini-powered web search chatbot built with Streamlit and LangGraph.")
    st.markdown(
        """
        [![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=YOUR_USERNAME&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/YOUR_USERNAME)
        """,
        unsafe_allow_html=True
    )