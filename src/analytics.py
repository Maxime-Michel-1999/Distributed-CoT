import model_details
import streamlit as st
import pandas as pd

def display_model_impact(model_name: str, num_tokens: int):
    """
    Affiche dans Streamlit l'impact environnemental et le coût pour un nombre donné de tokens.
    
    Args:
        model_name: Nom du modèle LLM
        num_tokens: Nombre de tokens utilisés
    """
    # Obtenir les coûts par token pour le modèle
    model_costs = model_details.get_model_token_cost(model_name)
    
    # Calculer les impacts totaux
    total_emissions = model_costs["ghg_co2eq"] * num_tokens
    total_energy = model_costs["energy_wh"] * num_tokens
    total_primary = model_costs["primary_energy_kj"] * num_tokens
    total_cost = model_costs["token_cost"] * num_tokens
    
    # Afficher les résultats dans Streamlit
    st.write("---")
    st.write("### Impact environnemental et coût")
    col1, col2 = st.columns(2)
    
    # Obtenir tous les modèles disponibles
    all_models = model_details.get_available_models()
    
    # Get costs for selected model
    selected_costs = model_details.get_model_token_cost(model_name)
    selected_co2 = selected_costs['ghg_co2eq']
    selected_energy = selected_costs['energy_wh'] 
    selected_primary = selected_costs['primary_energy_kj']
    selected_token_cost = selected_costs['token_cost']

    # Initialize data for DataFrame
    data = []
    metrics = ["Émissions CO2 (gCO2eq/token)", "Énergie (Wh/token)", 
               "Énergie primaire (kJ/token)", "Coût par token ($)"]

    # Add selected model data
    data.append({
        'Métrique': metrics[0],
        model_name: f"{selected_co2:.2e}"
    })
    data.append({
        'Métrique': metrics[1],
        model_name: f"{selected_energy:.2e}"
    })
    data.append({
        'Métrique': metrics[2],
        model_name: f"{selected_primary:.2e}"
    })
    data.append({
        'Métrique': metrics[3],
        model_name: f"{selected_token_cost:.2e}"
    })

    # Add relative differences for other models
    for model in all_models:
        if model != model_name:
            costs = model_details.get_model_token_cost(model)
            
            # Calculate relative differences as percentages
            co2_diff = ((costs['ghg_co2eq'] - selected_co2) / selected_co2) * 100
            energy_diff = ((costs['energy_wh'] - selected_energy) / selected_energy) * 100
            primary_diff = ((costs['primary_energy_kj'] - selected_primary) / selected_primary) * 100
            token_cost_diff = ((costs['token_cost'] - selected_token_cost) / selected_token_cost) * 100
            
            # Add relative differences to data
            data[0][f"{model} (% diff)"] = f"{co2_diff:+.1f}%"
            data[1][f"{model} (% diff)"] = f"{energy_diff:+.1f}%"
            data[2][f"{model} (% diff)"] = f"{primary_diff:+.1f}%"
            data[3][f"{model} (% diff)"] = f"{token_cost_diff:+.1f}%"
    
    # Create and display DataFrame
    df = pd.DataFrame(data)
    st.dataframe(df.set_index('Métrique'), use_container_width=True)
    
    # Display total impact for the used model
    st.markdown("### 📊 Total Impact of this Request")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        #### 🌍 Total Emissions
         ##### {total_emissions:.4f} gCO2eq
        
        #### ⚡ Total Energy  
         ##### {total_energy:.4f} Wh
        """)
        
    with col2:
        st.markdown(f"""
        #### 🔋 Primary Energy
         ##### {total_primary:.4f} kJ
        
        #### 💰 Total Cost
         ##### ${total_cost:.6f}
        """)
