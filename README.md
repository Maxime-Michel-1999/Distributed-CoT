# Optimized Routing for LLMs

This repository contains a **Streamlit app** that leverages **Groq**  to route prompts to the most suitable LLM models. The goal is to optimize the ecological and financial impact by selecting the model that best fits the prompt's requirements.

---

## Features

- **Dynamic Routing**: Automatically determines the best LLM model based on the characteristics of the input prompt.
- **Cost Optimization**: Reduces computational expenses by using the most efficient model for the task.
- **Environmental Impact Awareness**: Prioritizes energy-efficient models to minimize ecological impact.
- **User-Friendly Interface**: Built with Streamlit for an intuitive user experience.


## Installation

### Prerequisites
- Python 3.10 or later
- Pip package manager
- Groq libraries (see [Groq documentation](https://groq.com/docs) for installation)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Maxime-Michel-1999/Distributed-CoT.git
   cd Distributed-CoT
   ```


2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Groq:

    Follow the Groq installation guide and ensure your system is configured correctly.
    Verify installation with:

    ```bash
    groq --version
    ```

### Usage

1. Run the Streamlit app:

    ```bash
    streamlit run src/app.py
    ```

2. Access the app in your browser at http://localhost:8501.

3. Input your prompt:

- Enter a text prompt into the provided field.
- The app will analyze the prompt and route it to the most appropriate LLM model.

4. View results:

    The app displays the chosen model, its cost, and estimated energy consumption.
    You can compare different routing options to understand the trade-offs.