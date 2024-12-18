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
    
    with col1:
        st.metric("Émissions totales de CO2", f"{total_emissions:.4f} gCO2eq", 
                 f"{model_costs['ghg_co2eq']:.2e} par token")
        st.metric("Consommation totale d'énergie", f"{total_energy:.4f} Wh",
                 f"{model_costs['energy_wh']:.2e} par token")
    
    with col2:
        st.metric("Énergie primaire totale", f"{total_primary:.4f} kJ",
                 f"{model_costs['primary_energy_kj']:.2e} par token")
        st.metric("Coût total", f"{total_cost:.2e} $",
                 f"{model_costs['token_cost']:.2e} $ par token")

