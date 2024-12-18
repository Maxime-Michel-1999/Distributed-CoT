def get_available_models():
    """
    Returns a dictionary of available models with their associated complexity capacity.
    
    Returns:
        dict: A dictionary where keys are model names and values are their token context windows,
             indicating the maximum length of text they can effectively process.
             
    Example:
        {
            "mixtral-8x7b-32768": 32768,  # Can handle up to 32k tokens
            "llama3-8b-8192": 8192,       # Can handle up to 8k tokens
            "llama3-70b-8192": 8192       # Can handle up to 8k tokens
        }
    """
    return {
        "mixtral-8x7b-32768": 8,
        "llama3-8b-8192": 8,
        "llama3-70b-8192": 70,
    }