import streamlit as st
from model_calling import GroqModelCaller
import model_details
from router import LLMRouter
import analytics

# Configure page layout to remove default margins
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Title
st.title("LLM Router Prototype")


# Initialize GroqModelCaller
grokCaller = GroqModelCaller()

# Text input
user_input = st.text_area("Enter your text:", height=120)

# Submit button
if st.button("Submit"):
    if user_input:

        with st.container(border=True):
            # Get model name from router
            try:
                LLM_router = LLMRouter(model_details.get_available_models())
                model_name = LLM_router.classify_prompt(user_input)[0]
                st.write(f"Model {model_name} will be used")   # Call model with prompt
                output = grokCaller.get_completion(user_input, model = model_name)
            except:
                #Default behavior if model can't be called
                output = ("I can't respond right now",50)
                model_name = "mixtral-8x7b-32768"

            st.write("Output:", output[0])

            # Analytics
            analytics.display_model_impact(model_name, output[1])

    else:
        st.warning("Please enter some text.")

