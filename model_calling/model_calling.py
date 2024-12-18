import os
from typing import Optional
from groq import Groq

class GroqModelCaller:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le client Groq avec une clé API.
        
        Args:
            api_key: Clé API Groq. Si non fournie, cherche dans les variables d'environnement.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Une clé API Groq est requise")
        self.client = Groq(api_key=self.api_key)

    def get_completion(self, 
                      prompt: str,
                      model: str = "mixtral-8x7b-32768",
                      temperature: float = 0.7,
                      max_tokens: int = 1000) -> str:
        """
        Obtient une réponse du modèle Groq.
        
        Args:
            prompt: Le texte d'entrée pour le modèle
            model: Le modèle à utiliser
            temperature: Contrôle la créativité (0.0-1.0)
            max_tokens: Nombre maximum de tokens en sortie
            
        Returns:
            La réponse générée par le modèle
        """
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'appel au modèle Groq: {str(e)}")
