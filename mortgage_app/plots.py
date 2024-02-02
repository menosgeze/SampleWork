import plotly.graph_objs as go


def pie_month_distribution(
    n_period: int, 
    monthly_escrow: list,
    monthly_principal: list,
    monthly_interest: list
):
    labels = [
        'escrow',
        'interest',
        'principal'
    ]

    values = [
        monthly_escrow[n_period],
        montly_principal[n_period],
        monthly_interest[n_period],
    ]

    text = [f'${value}' for value in values]

    month_distribution = go.Pie(
        labels=labels,
        values=values,
        text=text,
        hole=0.5
    )
    
    return month_distribution

def combined_plot():
    fig = go.Figure()
    fig.update_layout(
       title="monthly payment distribution",
       height=400, width=400
    )
