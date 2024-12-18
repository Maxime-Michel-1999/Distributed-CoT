import streamlit as st

# Configure page layout to remove default margins
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Title
st.title("LLM Router Prototype")

# Text input
user_input = st.text_area("Enter your text:", height=150)

# Submit button
if st.button("Submit"):
    if user_input:
        # Placeholder for routing logic
        st.write("Processing your input...")
    else:
        st.warning("Please enter some text.")
