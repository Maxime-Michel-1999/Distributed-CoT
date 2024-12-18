import os
from typing import Optional
from groq import Groq
from dotenv import load_dotenv  # Ajouter cet import


class GroqModelCaller:
    def __init__(self, api_key: Optional[str] = None, model: str = "mixtral-8x7b-32768"):
        """
        Initialize the Groq client with an API key.
        
        Args:
            api_key: Groq API key. If not provided, looks for it in .env file
            model: Le modèle à utiliser (par défaut: mixtral-8x7b-32768)
        """
        # Load environment variables from .env
        load_dotenv(dotenv_path="../.env")
        
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("A Groq API key is required in the .env file")
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def get_completion(self, 
                      prompt: str,
                      temperature: float = 0.7,
                      max_tokens: int = 1000) -> str:
        """
        Get a response from the Groq model.
        
        Args:
            prompt: The input text for the model
            temperature: Controls creativity (0.0-1.0)
            max_tokens: Maximum number of output tokens
            
        Returns:
            The response generated by the model
        """
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error calling Groq model: {str(e)}")


"""if __name__ == "__main__":
    # Create a GroqModelCaller instance
    caller = GroqModelCaller(model="mixtral-8x7b-32768")
    
    # Test with a simple prompt
    prompt = "Say hello in English"
    print("Sending prompt:", prompt)
    
    try:
        response = caller.get_completion(prompt)
        print("\nModel response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")"""