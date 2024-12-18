def get_available_models():
    """
    Returns a dictionary of available models with their associated complexity capacity.
    
    Returns:
        dict: A dictionary where keys are model names and values are their complexity scores (in billions),
             indicating their ability to handle complex prompts and tasks. Higher values mean the model
             can handle more complex instructions and reasoning.
             
    Example:
        {
            "mixtral-8x7b-32768": 12.9,  # 12.9B parameter model
            "llama3-8b-8192": 8,         # 8B parameter model  
            "llama3-70b-8192": 70        # 70B parameter model
        }
    """
    return {
        "mixtral-8x7b-32768": 12.9,
        "llama3-8b-8192": 8,
        "llama3-70b-8192": 70,
    }