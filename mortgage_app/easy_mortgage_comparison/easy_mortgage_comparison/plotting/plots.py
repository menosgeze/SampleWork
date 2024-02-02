import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def generate_graph(
    payments: pd.DataFrame,
    output: str,
    sample_period: int = 24,
    escrow_column: str = "escrow",
    principal_column: str = "monthly_principal_expense",
    interest_column: str = "monthly_interest_expense",
):
    monthly_escrow = payments[escrow_column]
    monthly_principal = payments[principal_column]
    monthly_interest = payments[interest_column]

    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "domain"}], [{}]],
        shared_xaxes=False,
        shared_yaxes=False,
        vertical_spacing=0.01,
        subplot_titles=(
            "Month Payment Distribution",
            "Timeseries of Principal, Interest and Escrow",
        ),
    )

    sample_values = [
        monthly_escrow[sample_period],
        monthly_principal[sample_period],
        monthly_interest[sample_period],
    ]

    fig.add_trace(
        go.Pie(
            labels=["escrow", "principal", "interest"],
            values=sample_values,
            text=[f"${value}" for value in sample_values],
            hole=0.5,
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_principal.index,
            y=monthly_principal,
            name="principal",
            mode="lines+markers",
            marker={"size": 1, "color": "DarkBlue"},
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_interest.index,
            y=monthly_interest,
            name="interest",
            mode="lines+markers",
            marker={"size": 1, "color": "DarkRed"},
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_escrow.index,
            y=monthly_escrow,
            name="escrow growth",
            mode="lines+markers",
            marker={"size": 1, "color": "DarkGreen"},
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        title="Mortgage Monthly Payments History",
        height=800,
        width=400
    )

    fig.write_html()
