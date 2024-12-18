import streamlit as st
from model_calling import GroqModelCaller
import model_details
from router import LLMRouter
import analytics

# Configure page layout to remove default margins
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Title
st.title("LLM Router Prototype")

# Create two columns with 2:1 ratio
col1, col_space, col2 = st.columns([10, 1, 3])

with col1:
    # Initialize GroqModelCaller
    grokCaller = GroqModelCaller()

    # Text input
    st.write("### Prompt")
    user_input = st.text_area("Enter your text:", height=60)

    # Submit button
    if st.button("Submit"):
        if user_input:
            with st.container(border=True):
                # Get model name from router
                try:
                    LLM_router = LLMRouter(model_details.get_available_models())
                    model_name = LLM_router.classify_prompt(user_input)[0]
                    output = grokCaller.get_completion(user_input, model=model_name)
                except:
                    #Default behavior if model can't be called
                    output = ("I can't respond right now",50)
                    model_name = "mixtral-8x7b-32768"

                # Display model info in small text
                st.caption(f"Using {model_name}")
                
                # Create message container with avatar and styling
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(output[0])

                # Analytics
                analytics.display_model_impact(model_name, output[1])

        else:
            st.warning("Please enter some text.")

with col2:
    st.write("### Available Models")
    available_models = model_details.get_available_models()
    for model, complexity in available_models.items():
        with st.container(border=True):
            st.write(f"🟢 **{model}**")
            st.caption(f"Parameters: {complexity}B")
            model_costs = model_details.get_model_token_cost(model)
            st.caption(f"Cost per million tokens: ${model_costs['token_cost']*1e6:.2f}")
