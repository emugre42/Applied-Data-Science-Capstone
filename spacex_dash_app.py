# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # Dropdown for Launch Site Selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'}
                 ] + [{'label': i, 'value': i} for i in spacex_df["Launch Site"].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),
    # Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    # Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: f'{i}' for i in range(0, 10001, 2000)},
                    value=[min_payload, max_payload]),
    # Scatter Plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
    return fig

# Callback for Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_plot(entered_site, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) &
                            (spacex_df['Payload Mass (kg)'] <= max_payload)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
                         x="Payload Mass (kg)", 
                         y="class", 
                         color="Booster Version Category",
                         title="Payload vs. Outcome for All Sites")
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                         x="Payload Mass (kg)", 
                         y="class", 
                         color="Booster Version Category",
                         title=f"Payload vs. Outcome for site {entered_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
