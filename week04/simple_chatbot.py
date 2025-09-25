import streamlit as st
import random
import time

# Configure the page
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖")

st.title("🤖 Simple Chatbot")
st.caption("A basic rule-based chatbot that works without external dependencies")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm a simple chatbot. Ask me anything!"}
    ]

# Predefined responses
responses = {
    "hello": ["Hello! How can I help you today?", "Hi there! What's on your mind?", "Hey! Nice to meet you!"],
    "how are you": ["I'm doing great, thanks for asking!", "I'm good! How about you?", "Fantastic! Ready to chat!"],
    "weather": ["I can't check the weather, but I hope it's nice where you are!", "Weather is always better with good company!", "I don't have weather data, but every day is a good day to chat!"],
    "time": [f"I don't have real-time data, but it's always time to chat!", "Time flies when you're having fun!", "Every moment is the right time for a conversation!"],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a fake noodle? An impasta!"
    ],
    "bye": ["Goodbye! Have a great day!", "See you later!", "Bye! Come back anytime!"],
    "thanks": ["You're welcome!", "Happy to help!", "Anytime!"],
    "help": ["I'm a simple chatbot. Try asking me about the weather, time, jokes, or just say hello!", "I can chat about various topics. What would you like to know?"]
}

def get_response(user_input):
    """Generate a response based on user input"""
    user_input = user_input.lower().strip()
    
    # Check for keywords in user input
    for keyword, reply_list in responses.items():
        if keyword in user_input:
            return random.choice(reply_list)
    
    # Default responses for unrecognized input
    default_responses = [
        "That's interesting! Tell me more.",
        "I see! What else would you like to chat about?",
        "Hmm, I'm not sure about that, but I'm here to chat!",
        "That's a good point! What do you think about it?",
        "I'd love to learn more about what you're thinking!",
        "Interesting! Can you elaborate on that?",
        "I appreciate you sharing that with me!"
    ]
    
    return random.choice(default_responses)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to chat about?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response
    response = get_response(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Simulate typing effect
        message_placeholder = st.empty()
        full_response = ""
        
        # Type out the response character by character
        for char in response:
            full_response += char
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.02)  # Adjust typing speed
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with chatbot info
with st.sidebar:
    st.header("🤖 Chatbot Info")
    st.write("This is a simple rule-based chatbot that works without any external dependencies.")
    
    st.subheader("Try asking about:")
    st.write("• Greetings (hello, hi)")
    st.write("• Weather")
    st.write("• Time")
    st.write("• Jokes")
    st.write("• How I'm doing")
    st.write("• Or just chat freely!")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! I'm a simple chatbot. Ask me anything!"}
        ]
        st.rerun()
    
    st.write("---")
    st.write("💡 **Tip**: This chatbot uses predefined responses and doesn't require any AI models to be installed!")
