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
                    "label": "All Launch Sites",
                    "value": "All",
                },
            ]
            + [
                {"label": site, "value": site}
                for site in spacex_df["Launch_Site"].unique()
            ],
            placeholder="Select launch site here",
            searchable=True,
            value='All'
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[spacex_df['Payload Mass (kg)'].min(
            ), spacex_df['Payload Mass (kg)'].max()]
        ),
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
            filtered_df, values="class", names="Launch_Site", title="All Launch Sites", labels={
                'Launch_Site': 'Launch Site',
                'class': 'Number of launches'
            }
        ).update_traces(textposition='inside', textinfo='percent')
    else:
        filtered_df = (
            spacex_df[spacex_df["Launch_Site"] == site]
            .groupby(["Launch_Site", "class"])
            .size()
            .reset_index(name="count")
        )
        return px.pie(
            filtered_df,
            values="count",
            names="class",
            labels={'class': 'Launch result'},
            hover_data=['class'],
            title=f"{site} - Launch Site",
        ).update_traces(textposition='inside', textinfo='percent+label')


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',
           component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(site: str, payload: list):
    print(payload)
    if site == 'All':
        return px.scatter(
            spacex_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
    else:
        filterted = spacex_df[spacex_df["Launch_Site"] == site]
        filterted = filterted[filterted['Payload Mass (kg)'].between(
            payload[0], payload[1], inclusive='both')],
        return px.scatter(
            filterted,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
