import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
GEMINI_API_KEY=st.secrets['GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

initial_prompt = """You are Elaine, a friendly and helpful personal assistant chatbot made by Arun John M S. 
Your responses should be concise but informative. Use emojis and examples to explain 
concepts clearly. Provide more detailed information when asked. Try to understand 
the user's way of thinking and adapt accordingly. Always complete your thoughts and 
code snippets."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [initial_prompt]},
        {"role": "model", "parts": ["Understood! I'm Elaine, your friendly AI assistant. How can I help you today? 😊"]}
    ])
# Function to get response from Gemini
def get_gemini_response(prompt):
    response = st.session_state.chat.send_message(prompt)
    return response.text

# Streamlit app
st.title("🤖 Elaine - Your Personal Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate Elaine's response
    response = get_gemini_response(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a button to clear the chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [initial_prompt]},
        {"role": "model", "parts": ["Understood! I'm Elaine, your friendly AI assistant. How can I help you today? 😊"]}
    ])
    st.experimental_rerun()
