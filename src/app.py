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
                try:
                    LLM_router = LLMRouter(model_details.get_available_models())
                    model_name = LLM_router.classify_prompt(user_input)[0]
                except:
                    model_name = "mixtral-8x7b-32768"

                # Get responses from all available models
                outputs = {}
                for model in model_details.get_available_models().keys():
                    try:
                        outputs[model] = grokCaller.get_completion(user_input, model=model)
                    except:
                        outputs[model] = ("I can't respond right now", 50)

                # Display chosen model's response first
                with st.container(border=True):
                    # Header with model name and chosen status
                    header_cols = st.columns([3, 1])
                    with header_cols[0]:
                        st.markdown(f"### 🌟 {model_name} <div style='display: inline-block; background-color: #90EE9033; padding: 1px 10px; border-radius: 5px; margin-left: 10px;'><p style='color: #2E8B57; font-weight: bold; margin: 0;'>Selected by Router</p></div>", unsafe_allow_html=True)
                    # Message container
                    st.write(outputs[model_name][0])

                # Display other models' responses
                for model, output in outputs.items():
                    if model != model_name:
                        with st.expander(f"# {model}"):
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
