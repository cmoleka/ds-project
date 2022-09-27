# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("data/spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
spacex_json = spacex_df.to_dict("records")
# print(
#     spacex_df[spacex_df["Launch_Site"] == "CCAFS LC-40"]
#     .groupby(["Launch_Site", "class"], as_index=False)
#     .head()
# )

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {
                    "label": "All Sites",
                    "value": "All",
                },
            ]
            + [
                {"label": site, "value": site}
                for site in spacex_df["Launch_Site"].unique()
            ],
            placeholder="Select launch site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(site):
    filtered_df = spacex_df
    if site == "All":
        return px.pie(
            filtered_df, values="class", names="Launch_Site", title="All Launch Sites"
        )
    else:
        filtered_df = (
            spacex_df[spacex_df["Launch_Site"] == site]
            .groupby(["Launch_Site", "class"])
            .size()
            .reset_index(name="class count")
        )
        return px.pie(
            filtered_df,
            values="class count",
            names="class",
            title=f"{site} - Launch Site",
        )


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
