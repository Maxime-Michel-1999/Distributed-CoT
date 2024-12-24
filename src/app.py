import streamlit as st

import analytics
import model_details
from model_calling import GroqModelCaller
from router import LLMRouter

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title("🤖 Smart LLM Router")

with st.sidebar:

    st.image("data/icon/logo_router.png", width=200, use_column_width=True)

    # Display available models and their details
    st.write("## 📋 Available Models")
    available_models = model_details.get_available_models()
    for model, complexity in available_models.items():
        with st.container():
            st.markdown(
                f"🟢 **{model}**  \n"
                f"Parameters: {complexity} Billion  \n"
                f"Cost per million tokens: ${model_details.get_model_token_cost(model)['token_cost']*1e6:.2f}"
            )

    st.markdown(
        "ℹ️ [More information about the models](https://console.groq.com/docs/models/)",
        unsafe_allow_html=True,
    )

    st.markdown("--------")

    st.header("📖 FAQ")
    st.write(
        "This prototype routes prompts to the most suitable Large Language Model (LLM) based on your input. "
        "It also allows you to compare responses from various models."
    )
    st.markdown(
        "### How does it work?\n"
        "1. Enter your prompt in the text box.\n"
        "2. The router selects the best model for your input.\n"
        "3. Compare responses from all available models."
    )

    st.markdown(
        "### Need Help?\n"
        "Feel free to reach out to our support team for assistance."
    )


groqCaller = GroqModelCaller()

# Text input section
st.write("## 🌟 Prompt Input")
user_input = st.text_area("Enter your text here:", height=100)

# Submit button
if st.button("🔍 Analyze and Route"):
    if user_input:
        with st.container():
            try:
                LLM_router = LLMRouter(model_details.get_available_models())
                model_name = LLM_router.classify_prompt(user_input)[0]
            except Exception as e:
                model_name = "mixtral-8x7b-32768"

            # Get responses from all available models
            outputs = {}
            for model in model_details.get_available_models().keys():
                try:
                    outputs[model] = groqCaller.get_completion(
                        user_input, model=model
                    )
                except Exception as e:
                    outputs[model] = (
                        "Sorry, I can't respond right now.",
                        0,
                    )

            # Display router-selected model's response
            with st.container():
                st.write(f"### 🏆 Selected Model: {model_name}")
                st.write(outputs[model_name][0])

            # Display responses from other models
            for model, output in outputs.items():
                if model != model_name:
                    with st.expander(f"🔎 Response from {model}"):
                        st.write(output[0])

            # Display analytics for the selected model
            analytics.display_model_impact(model_name, outputs[model_name][1])

    else:
        st.warning("Please enter a prompt to analyze.")
