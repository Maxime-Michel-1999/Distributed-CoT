import pandas as pd
import streamlit as st
import plotly.graph_objects as go
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

def display_concise_comparison_analytics(model_name, num_tokens):
    # Create subplots for each metric
    fig = go.Figure()
    
    metrics = ['Cost', 'Energy', 'Emissions']
    models = list(model_details.get_available_models().keys())
    
    # Generate distinct colors for each model
    model_colors = {
        model: '#90EE90' if model == model_name else f'rgba({hash(model) % 255}, {(hash(model) >> 8) % 255}, {(hash(model) >> 16) % 255}, 0.7)'
        for model in models
    }
    # Collect data for each metric
    metric_data = {metric: [] for metric in metrics}
    
    # Add selected model first
    costs = model_details.get_model_token_cost(model_name)
    metric_data['Cost'].append(costs['token_cost'] * num_tokens * 10000)
    metric_data['Energy'].append(costs['energy_wh'] * num_tokens)
    metric_data['Emissions'].append(costs['ghg_co2eq'] * num_tokens)
    
    # Add remaining models
    for model in [m for m in models if m != model_name]:
        costs = model_details.get_model_token_cost(model)
        metric_data['Cost'].append(costs['token_cost'] * num_tokens * 10000)
        metric_data['Energy'].append(costs['energy_wh'] * num_tokens)
        metric_data['Emissions'].append(costs['ghg_co2eq'] * num_tokens)

    # Create a subplot for each metric
    for i, metric in enumerate(metrics):
        for j, model in enumerate(models):
            opacity = 1.0 if model == model_name else 0.7
            fig.add_trace(go.Bar(
                name=model if i == 0 else None,  # Only add to legend once
                x=[i],  # Use numeric index for x-axis positioning
                y=[metric_data[metric][j]],
                marker_color=model_colors[model].replace('0.7', str(opacity)),
                marker_line_width=2 if model == model_name else 0,
                marker_line_color='rgb(0, 0, 0)',
                showlegend=i == 0,
                legendgroup=model,
            ))

    # Update layout
    fig.update_layout(
        height=150,
        barmode='group',
        showlegend=True,
        legend_title='Models',
        xaxis={
            'tickmode': 'array',
            'ticktext': metrics,
            'tickvals': [0, 1, 2],
            'range': [-0.8, 2.8],  # Modified range to give more space on both sides
            'tickangle': 0,
            'fixedrange': True,    # Prevents x-axis zooming
        },
        yaxis={'showticklabels': False},
        bargap=0.15,
        bargroupgap=0.1,
        margin=dict(l=20, r=20, t=0, b=0.1)  # Added left and right margins
    )
    
    st.plotly_chart(fig, use_container_width=True)




def display_gain(model_name, num_tokens):
    model_costs = model_details.get_model_token_cost(model_name)
    gpt4_costs = model_details.get_model_token_cost("gpt-4")
    
    total_cost = model_costs["token_cost"] * num_tokens
    total_emissions = model_costs["ghg_co2eq"] * num_tokens 
    total_energy = model_costs["energy_wh"] * num_tokens
    
    gpt4_cost = gpt4_costs["token_cost"] * num_tokens
    gpt4_emissions = gpt4_costs["ghg_co2eq"] * num_tokens
    gpt4_energy = gpt4_costs["energy_wh"] * num_tokens
    
    cost_gain = ((gpt4_cost - total_cost) / gpt4_cost) * 100
    emissions_gain = ((gpt4_emissions - total_emissions) / gpt4_emissions) * 100
    energy_gain = ((gpt4_energy - total_energy) / gpt4_energy) * 100
    # Create columns for better visual organization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Cost", f"{cost_gain:.1f}%", delta="saved")
    
    with col2:
        st.metric("🌱 Emissions", f"{emissions_gain:.1f}%", delta="reduced") 
    
    with col3:
        st.metric("⚡ Energy", f"{energy_gain:.1f}%", delta="saved")
