import pandas as pd
import streamlit as st

import model_details
from data_vizualisation import model_comparison_plot


def display_model_impact(model_name: str, num_tokens: int) -> None:
    """
    Displays the environmental impact, cost of a model, and a cost comparison plot.

    Args:
        model_name: The name of the selected model.
        num_tokens: The number of tokens used in the request.
    """
    model_costs = model_details.get_model_token_cost(model_name)

    # Compute metrics
    total_emissions = model_costs["ghg_co2eq"] * num_tokens
    total_energy = model_costs["energy_wh"] * num_tokens
    total_primary = model_costs["primary_energy_kj"] * num_tokens
    total_cost = model_costs["token_cost"] * num_tokens

    st.write("---")
    st.write("### 🌱 Environmental Impact and Cost")

    # Fetch all models and their details
    all_models = model_details.get_available_models()
    selected_costs = model_details.get_model_token_cost(model_name)
    selected_co2 = selected_costs["ghg_co2eq"]
    selected_energy = selected_costs["energy_wh"]
    selected_primary = selected_costs["primary_energy_kj"]
    selected_token_cost = selected_costs["token_cost"]

    # Prepare comparison data
    data = []
    metrics = [
        "CO2 emissions (gCO2eq/token)",
        "Energy (Wh/token)",
        "Primary Energy (kJ/token)",
        "Cost per token ($)",
    ]

    # Add selected model data
    data.append({"Metric": metrics[0], model_name: f"{selected_co2:.2e}"})
    data.append({"Metric": metrics[1], model_name: f"{selected_energy:.2e}"})
    data.append({"Metric": metrics[2], model_name: f"{selected_primary:.2e}"})
    data.append(
        {"Metric": metrics[3], model_name: f"{selected_token_cost:.2e}"}
    )

    # Add relative differences for other models
    for model in all_models:
        if model != model_name:
            costs = model_details.get_model_token_cost(model)

            co2_diff = (
                (costs["ghg_co2eq"] - selected_co2) / selected_co2
            ) * 100
            energy_diff = (
                (costs["energy_wh"] - selected_energy) / selected_energy
            ) * 100
            primary_diff = (
                (costs["primary_energy_kj"] - selected_primary)
                / selected_primary
            ) * 100
            token_cost_diff = (
                (costs["token_cost"] - selected_token_cost)
                / selected_token_cost
            ) * 100

            data[0][f"{model} (% diff)"] = f"{co2_diff:+.1f}%"
            data[1][f"{model} (% diff)"] = f"{energy_diff:+.1f}%"
            data[2][f"{model} (% diff)"] = f"{primary_diff:+.1f}%"
            data[3][f"{model} (% diff)"] = f"{token_cost_diff:+.1f}%"

    df = pd.DataFrame(data)
    st.dataframe(df.set_index("Metric"), use_container_width=True)

    all_model_costs = model_details.get_model_token_cost()
    all_model_costs_df = (
        pd.DataFrame(all_model_costs)
        .T.reset_index()
        .rename(columns={"index": "model_name"})
    )

    col1, col2 = st.columns(2)
    with col1:
        emission_fig = model_comparison_plot(
            all_model_costs_df, variable="energy_wh"
        )
        st.plotly_chart(emission_fig, use_container_width=True)

    with col2:
        cost_fig = model_comparison_plot(
            all_model_costs_df, variable="token_cost"
        )
        st.plotly_chart(cost_fig, use_container_width=True)

    # Display total impact for the used model
    st.markdown("### 📊 Total Impact of This Request")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        #### 🌍 Total Emissions
         ##### **{total_emissions:.4f} gCO2eq**
        
        #### ⚡ Total Energy  
         ##### **{total_energy:.4f} Wh**
        """
        )

    with col2:
        st.markdown(
            f"""
        #### 🔋 Primary Energy
         ##### **{total_primary:.4f} kJ**
        
        #### 💰 Total Cost
         ##### **${total_cost:.6f}**
        """
        )
