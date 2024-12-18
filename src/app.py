import streamlit as st
from model_calling import GroqModelCaller
from router import LLMRouter

# Configure page layout to remove default margins
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Title
st.title("LLM Router Prototype")


# Initialize GroqModelCaller
print("Initializing GroqModelCaller...")
grokCaller = GroqModelCaller()
print("GroqModelCaller initialized successfully")

# Text input
user_input = st.text_area("Enter your text:", height=120)

# Submit button
if st.button("Submit"):
    if user_input:
        # Get model name from router
        model_name = LLMRouter(user_input)
        st.write(f"Model {model_name} will be used")
        
        # Call model with prompt
        output = grokCaller.get_completion(user_input, model_name)
        st.write("Output:", output)
    else:
        st.warning("Please enter some text.")
