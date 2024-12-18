import streamlit as st
from model_calling import GroqModelCaller
import model_details
from router import LLMRouter

# Configure page layout to remove default margins
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Title
st.title("LLM Router Prototype")




# Text input
user_input = st.text_area("Enter your text:", height=120)

# Submit button
if st.button("Submit"):
    if user_input:
        # Get model name from router
        LLM_router = LLMRouter(model_details.get_available_models())
        model_name = LLM_router.classify_prompt(user_input)[0]
        st.write(f"Model {model_name} will be used")

        # Initialize GroqModelCaller
        print("Initializing GroqModelCaller...")
        grokCaller = GroqModelCaller(model = model_name)
        print("GroqModelCaller initialized successfully")
        
        # Call model with prompt
        output = grokCaller.get_completion(user_input)
        st.write("Output:", output)
    else:
        st.warning("Please enter some text.")
