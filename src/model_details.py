import json


def get_available_models(
    json_file_path: str = "data/model_info/model_complexity.json",
) -> dict:
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
            "llama3-70b-8192": 70,       # 70B parameter model
            "gpt-4": 1750                # 1.75T parameter model
        }
    """
    with open(json_file_path, "r") as file:
        model_complexity = json.load(file)

    return model_complexity


import json


def get_model_token_cost(
    model_name: str = None,
    json_file_path: str = "data/model_info/model_costs.json",
) -> dict:
    """
    Returns the token cost for a given model, or for all models if no model name is provided.

    Parameters:
        model_name (str): The name of the model. If None, returns costs for all models.
        json_file_path (str): Path to the JSON file containing model costs.

    Returns:
        dict: Dictionary of token costs for all models if no model is specified.
    """
    # Load the dictionary mapping model names to their token costs
    with open(json_file_path, "r") as file:
        model_costs_europe = json.load(file)

    # Return all costs if no model_name is provided
    if model_name is None:
        return model_costs_europe

    if model_name not in model_costs_europe:
        raise ValueError(f"Unknown model: {model_name}")

    return model_costs_europe[model_name]
