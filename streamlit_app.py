import streamlit as st
import openai

def get_response(messages):
    """Send chat history and user message to OpenAI and get a response with a food recipe focus."""
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Ensure the system message is always included
    if messages[0]["role"] != "system":
        messages.insert(0, {"role": "system", "content": "You are a helpful chef assistant. You only respond with food recipes, ingredients, and cooking instructions."})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# Set Streamlit app title
st.title("MeFoodie - Recipe Assistant")

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful chef assistant. You only respond with food recipes, ingredients, and cooking instructions."}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":  # Hide system message in chat UI
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask for a recipe...")

if user_input:
    # Append user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response (focused on food recipes)
    assistant_response = get_response(st.session_state.messages)

    # Append assistant message to session state and display it
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
