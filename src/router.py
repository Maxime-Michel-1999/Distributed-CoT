import os
from typing import Any, Tuple

import model_calling
import model_details
from prompt_manager import PromptManager


class LLMRouter:
    """Routes prompts to appropriate models based on complexity and context length."""

    def __init__(self, models_complexity: dict[str, Any]):
        """Initializes the LLMRouter with a dictionary of models and their complexities.

        Args:
            models_complexity (dict): A dictionary where keys are model names and values are their complexities.
        """
        self.models_complexity = models_complexity

    def classify_prompt(self, user_prompt: str) -> Tuple[str, int]:
        """Classifies the given prompt and selects appropriate model.

        Args:
            prompt (str): The prompt to classify.

        Returns:
            Tuple[str, int]: Model name and its context window size
        """
        api_key = os.getenv("GROQ_API_KEY")

        # Calculate prompt length in tokens (rough estimate)
        prompt_tokens = len(user_prompt.split())
        
        # Filter out models with insufficient context windows
        viable_models = {}
        for model_name, model_info in self.models_complexity.items():
            context_size = model_info["context_size"]
            if context_size >= prompt_tokens * 2:  # Leave room for response
                viable_models[model_name] = model_info["parameters"]

        if not viable_models:
            raise ValueError("Prompt is too long for all available models")

        # For remaining models, check complexity requirements
        prompt_manager = PromptManager(template_dir="templates")
        model = model_calling.GroqModelCaller(api_key=api_key)
        classification_prompt = prompt_manager.render_template(
            "classification_instructions.j2", {"user_prompt": user_prompt}
        )
        output = model.get_completion(
            classification_prompt, model="llama3-8b-8192"
        )[0]

        sorted_models = sorted(
            viable_models.items(), key=lambda item: item[1]
        )

        if output == "Complicated":
            selected_model = sorted_models[-1]
        else:
            selected_model = sorted_models[0]

        model_name = selected_model[0]
        context_size = self.models_complexity[model_name]["context_size"]
        return model_name, context_size


if __name__ == "__main__":

    print(os.getcwd())
    router = LLMRouter(model_details.get_available_models())

    # Test with a simple prompt
    prompt = "Say hello in English"
    print("Sending prompt:", prompt)

    model, context = router.classify_prompt(prompt)
    print(f"Selected model: {model} (context size: {context})")
