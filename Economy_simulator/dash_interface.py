import threading
import time

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from society import Society

# Initialize the society model
society = Society()


def simulation_loop():
    """Continuously advance the society simulation in a background thread."""
    while True:
        society.tick()
        time.sleep(0.8)


def build_market_price_figure():
    market = society.market
    return {
        "data": [
            go.Bar(
                x=["Medicine", "Food", "Plumbing"],
                y=[market.medicine_cost, market.food_cost, market.plumbing_cost],
                marker_color=["#d9534f", "#5cb85c", "#5bc0de"],
            )
        ],
        "layout": go.Layout(
            title="Market Prices",
            yaxis={"title": "Cost"},
            template="plotly_dark",
        ),
    }


def build_market_consumption_figure():
    market = society.market
    return {
        "data": [
            go.Scatter(
                x=list(range(len(market.medicine_history))),
                y=market.medicine_history,
                mode="lines",
                name="Medicine",
                line={"color": "#d9534f"},
            ),
            go.Scatter(
                x=list(range(len(market.plumbing_history))),
                y=market.plumbing_history,
                mode="lines",
                name="Plumbing",
                line={"color": "#0275d8"},
            ),
            go.Scatter(
                x=list(range(len(market.food_history))),
                y=market.food_history,
                mode="lines",
                name="Food",
                line={"color": "#5cb85c"},
            ),
        ],
        "layout": go.Layout(
            title="Market Consumption Over Time",
            xaxis={"title": "Tick"},
            yaxis={"title": "Units"},
            template="plotly_dark",
        ),
    }


def build_population_figure():
    return {
        "data": [
            go.Scatter(
                x=list(range(len(society.population_history))),
                y=society.population_history,
                mode="lines+markers",
                name="Population",
                line={"color": "#f0ad4e"},
            )
        ],
        "layout": go.Layout(
            title="Population Trend",
            xaxis={"title": "Tick"},
            yaxis={"title": "Population"},
            template="plotly_dark",
        ),
    }


def build_profession_figure():
    counts = society.count_professions()
    labels = list(counts.keys())
    values = list(counts.values())

    return {
        "data": [
            go.Pie(labels=labels, values=values, hole=0.4)
        ],
        "layout": go.Layout(
            title="Profession Distribution",
            template="plotly_dark",
        ),
    }


# Start the simulation thread once
sim_thread = threading.Thread(target=simulation_loop, daemon=True)
sim_thread.start()

# Build the Dash application
app = dash.Dash(__name__)
app.title = "Economy Simulation Dashboard"

app.layout = html.Div(
    className="dashboard",
    children=[
        html.H1("Economy Simulation Dashboard"),
        html.Div(
            className="charts-row",
            children=[
                dcc.Graph(id="market-prices", figure=build_market_price_figure()),
                dcc.Graph(id="market-consumption", figure=build_market_consumption_figure()),
            ],
        ),
        html.Div(
            className="charts-row",
            children=[
                dcc.Graph(id="population-trend", figure=build_population_figure()),
                dcc.Graph(id="profession-distribution", figure=build_profession_figure()),
            ],
        ),
        dcc.Interval(id="interval-component", interval=2000, n_intervals=0),
    ],
)


@app.callback(
    [
        Output("market-prices", "figure"),
        Output("market-consumption", "figure"),
        Output("population-trend", "figure"),
        Output("profession-distribution", "figure"),
    ],
    Input("interval-component", "n_intervals"),
)
def update_charts(_):
    return (
        build_market_price_figure(),
        build_market_consumption_figure(),
        build_population_figure(),
        build_profession_figure(),
    )


if __name__ == "__main__":
    app.run(debug=True)
