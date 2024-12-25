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
    for model, model_info in available_models.items():
        with st.container():
            st.markdown(
                f"🟢 **{model}**  \n"
                f"Parameters: {model_info['parameters']} Billion  \n"
                f"Context Size: {model_info['context_size']} tokens  \n"
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

# Option for RAG above prompt input
enable_rag = st.checkbox("🔍 Enable RAG (Retrieval-Augmented Generation)")
if enable_rag:
    uploaded_file = st.file_uploader("Upload context document", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            context_text = str(uploaded_file.read(), "utf-8")
            st.success("Document uploaded successfully!")
            st.info(f"Context length: {len(context_text.split())} words")
        else:
            st.warning("Currently only supporting .txt files. PDF and DOCX support coming soon!")
            context_text = ""
    else:
        context_text = ""
else:
    context_text = ""

user_input = st.text_area("Enter your text here:", height=100)

# Display prompt length
if user_input:
    st.info(f"Prompt length: {len(user_input.split())} words")

# Submit button
if st.button("🔍 Analyze and Route"):
    if user_input:
        with st.container():
            try:
                # Combine user input with context if RAG is enabled
                full_prompt = user_input
                if enable_rag and context_text:
                    full_prompt = f"Context:\n{context_text}\n\nQuestion:\n{user_input}"
                    st.info(f"Total input length (context + prompt): {len(full_prompt.split())} words")
                
                LLM_router = LLMRouter(model_details.get_available_models())
                model_name = LLM_router.classify_prompt(full_prompt)[0]
            except Exception as e:
                model_name = "mixtral-8x7b-32768"

            # Get responses from all available models
            outputs = {}
            for model in model_details.get_available_models().keys():
                try:
                    outputs[model] = groqCaller.get_completion(
                        full_prompt, model=model
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
