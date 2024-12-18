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


def get_model_token_cost(model_name: str) -> float:
    """
    Returns the token cost for a given model.
    """

    # Dictionary mapping model names to their token costs in terms of energy, emissions and primary energy
    model_costs_europe = {
        "llama3-70b-8192": {
            "energy_wh": 0.0125,        # Energy in Watt-hours
            "ghg_co2eq": 0.00665,       # Greenhouse gas emissions in gCO2eq
            "primary_energy_kj": 0.165,
            "token_cost": 0.59e-6   # Primary energy in kJ
        },
        "llama3-8b-8192": {
            "energy_wh": 0.00377,
            "ghg_co2eq": 0.00202,
            "primary_energy_kj": 0.0498,
            "token_cost": 0.05e-6
        },
        "mixtral-8x7b-32768": {
            "energy_wh": 0.00446,
            "ghg_co2eq": 0.00238,
            "primary_energy_kj": 0.0587,
            "token_cost": 0.24e-6
        }
    }
    
    if model_name not in model_costs_europe:
        raise ValueError(f"Unknown model: {model_name}")
        
    return model_costs_europe[model_name]

def get_model_token_cost(model_name: str) -> float:
    """
    Returns the token cost for a given model.
    """

    # Dictionary mapping model names to their token costs in terms of energy, emissions and primary energy
    model_costs_europe = {
        "llama3-70b-8192": {
            "energy_wh": 0.0125,        # Energy in Watt-hours
            "ghg_co2eq": 0.00665,       # Greenhouse gas emissions in gCO2eq
            "primary_energy_kj": 0.165   # Primary energy in kJ
        },
        "llama3-8b-8192": {
            "energy_wh": 0.00377,
            "ghg_co2eq": 0.00202,
            "primary_energy_kj": 0.0498
        },
        "mixtral-8x7b-32768": {
            "energy_wh": 0.00446,
            "ghg_co2eq": 0.00238,
            "primary_energy_kj": 0.0587
        }
    }
    
    if model_name not in model_costs_europe:
        raise ValueError(f"Unknown model: {model_name}")
        
    return model_costs_europe[model_name]
