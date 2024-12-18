import subprocess
from typing import Any
from model_calling import model_calling, available_models
import classification_instructions


class LLMRouter:
    """Classifies prompts as 'Complicated' or 'Not Complicated'."""

    def __init__(self, models_complexity: dict[str, Any]):
        """Initializes the LLMRouter with a dictionary of models and their complexities.

        Args:
            models_complexity (dict): A dictionary where keys are model names and values are their complexities.
        """
        self.models_complexity = models_complexity

    def create_prompt(self):
        """"""


    def classify_prompt(self, prompt: str) -> str:
        """Classifies the given prompt.

        Args:
            prompt (str): The prompt to classify.

        Returns:
            str: 'Complicated' or 'Not Complicated' based on the model's output.
        """
        output = model_calling.classify(prompt)
        
        if output == "Complicated":
            return "Complicated"
        else:
            return "Not Complicated"
    
    def get_model