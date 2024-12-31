import streamlit as st
import model_details
from model_calling import GroqModelCaller
from router import LLMRouter
import json

def get_task_breakdown(prompt: str, groq_caller: GroqModelCaller) -> list:
    """Get the step-by-step breakdown of a complex task."""
    system_prompt = """You are a helpful assistant that breaks down complex tasks into smaller, more manageable steps.
    
    Break down the given task into 3-5 clear steps. For each step, specify:
    1. A clear description of what needs to be done
    2. The type of reasoning required (analytical, creative, mathematical, logical)
    3. The expected output format
    
    Format your response as a JSON array where each step is an object:
    {
        "step_number": integer,
        "description": string, 
        "reasoning_type": string,
        "expected_output": string
    }"""

    full_prompt = f"{system_prompt}\n\nTask: {prompt}"
    steps_response, _ = groq_caller.get_completion(
        full_prompt,
        model="mixtral-8x7b-32768",
        temperature=0.3
    )

    try:
        return json.loads(steps_response)
    except:
        st.error("Failed to parse the steps. Please try again.")
        return None


def process_single_step(step: dict, llm_router: LLMRouter, groq_caller: GroqModelCaller) -> str:
    """Process a single step in the chain of thoughts."""
    step_prompt = f"""Reasoning Type: {step['reasoning_type']}
    Task: {step['description']}
    Expected Output: {step['expected_output']}
    
    Please provide your response:"""
    
    best_model = llm_router.classify_prompt(step_prompt)[0]
    
    response, tokens = groq_caller.get_completion(
        step_prompt,
        model=best_model,
        temperature=0.7
    )
    
    st.write(f"🤖 Using model: **{best_model}**")
    st.write(response)
    return response


def generate_final_summary(outputs: list, llm_router: LLMRouter, groq_caller: GroqModelCaller) -> str:
    """Generate a final summary from all step outputs."""
    summary_prompt = f"""Given these step-by-step outputs, provide a final concise summary:
    {' '.join(outputs)}"""
    
    final_model = llm_router.classify_prompt(summary_prompt)[0]
    final_summary, _ = groq_caller.get_completion(
        summary_prompt,
        model=final_model,
        temperature=0.7
    )
    return final_summary


def chain_of_thoughts_orchestrator(prompt):
    """Main orchestrator function for the chain of thoughts process."""
    # Initialize the router and model caller
    llm_router = LLMRouter({k: v for k, v in model_details.get_available_models().items() if k != "gpt-4"})
    groq_caller = GroqModelCaller()

    # Get task breakdown
    steps = get_task_breakdown(prompt, groq_caller)
    if not steps:
        return

    # Display the chain of thoughts process
    st.write("### 🔄 Chain of Thoughts Process")
    
    # Process each step
    final_outputs = []
    for step in steps:
        with st.expander(f"Step {step['step_number']}: {step['description']}", expanded=True):
            step_output = process_single_step(step, llm_router, groq_caller)
            final_outputs.append(step_output)

    # Generate and display final summary
    final_summary = generate_final_summary(final_outputs, llm_router, groq_caller)
    st.write("### 📝 Final Summary")
    st.write(final_summary)
