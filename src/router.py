from typing import Any
import model_calling
import model_details
import classification_instructions
import os


class LLMRouter:
    """Classifies prompts as 'Complicated' or 'Not Complicated'."""

    def __init__(self, models_complexity: dict[str, Any]):
        """Initializes the LLMRouter with a dictionary of models and their complexities.

        Args:
            models_complexity (dict): A dictionary where keys are model names and values are their complexities.
        """
        self.models_complexity = models_complexity

    def classify_prompt(self, user_prompt: str) -> str:
        """Classifies the given prompt.

        Args:
            prompt (str): The prompt to classify.

        Returns:
            str: 'Complicated' or 'Not Complicated' based on the model's output.
        """
        api_key = os.getenv("GROQ_API_KEY")
        model = model_calling.GroqModelCaller(api_key=api_key, model="llama3-8b-8192")
        classification_prompt = classification_instructions.prompt.format(user_prompt=user_prompt)
        output = model.get_completion(classification_prompt)[0]
        
        sorted_models = sorted(self.models_complexity.items(), key=lambda item: item[1])
        
        if output == "Complicated":
            return sorted_models[-1]
        else:
            return sorted_models[0]


if __name__ == "__main__":
    # Create a GroqModelCaller instance
    print(os.getcwd())
    router = LLMRouter(model_details.get_available_models())
    
    # Test with a simple prompt
    prompt = "Say hello in English"
    print("Sending prompt:", prompt)
    
    model = router.classify_prompt(prompt)
    print(model)

