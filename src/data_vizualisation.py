import pandas as pd
import plotly.express as px


def model_comparison_plot(data, variable="energy_wh"):
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="model_name",
        y=variable,
    )

    fig.update_traces(
        marker_color="green",
    )

    fig.update_layout(
        title=f"Comparison of {variable.replace('_', ' ')}",
        title_font_size=16,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False,
        xaxis_title="",  # Remove x-axis title
        yaxis_title="",  # Remove y-axis title
        xaxis=dict(showticklabels=True),
        yaxis=dict(showticklabels=True),
    )

    return fig
