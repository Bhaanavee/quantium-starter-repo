import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

try:
    df = pd.read_csv('processed_data.csv')
    df['date'] = pd.to_datetime(df['date'])
except FileNotFoundError:
    print("Error: The 'processed_data.csv' file was not found.")
    print("Please ensure you have completed the previous task and the file is in the correct directory.")
    raise PreventUpdate

df = df.sort_values(by='date')

app = dash.Dash(__name__)

app.layout = html.Div(style={
    'backgroundColor': '#2c3e50', 
    'font-family': 'Arial, sans-serif',
    'padding': '40px',
    'textAlign': 'center',
    'color': '#ecf0f1'
}, children=[
    html.H1(
        children='3D Pink Morsel Sales Analysis',
        style={
            'color': '#ecf0f1',
            'marginBottom': '20px',
            'fontSize': '40px',
            'textShadow': '2px 2px 4px #000000'
        }
    ),

    html.Div(
        children='Explore daily sales in a 3D landscape and see the effect of the price change.',
        style={
            'color': '#bdc3c7',
            'marginBottom': '30px',
            'fontSize': '18px'
        }
    ),

    html.Div(style={'marginBottom': '30px'}, children=[
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px', 'fontSize': '16px', 'color': '#ecf0f1'}
        )
    ]),
    dcc.Graph(
        id='sales-3d-chart',
        style={'height': '800px'}
    )
])

@app.callback(
    Output('sales-3d-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    fig = px.line_3d(
        filtered_df,
        x="date",
        y="Sales",
        z="region",
        color="region",
        title="Pink Morsel Sales Over Time",
        labels={
            "date": "Date",
            "Sales": "Total Sales ($)",
            "region": "Region"
        }
    )

    price_increase_date = '2021-01-15'
    
    max_sales = filtered_df['Sales'].max() if not filtered_df.empty else 0
    min_sales = filtered_df['Sales'].min() if not filtered_df.empty else 0
    regions_to_draw = filtered_df['region'].unique()

    for region in regions_to_draw:
        fig.add_trace(go.Scatter3d(
            x=[price_increase_date, price_increase_date],
            y=[min_sales, max_sales],
            z=[region, region],
            mode='lines',
            line=dict(color='red', width=4, dash='dash'),
            name='Price Increase',
            showlegend=False,
            hoverinfo='text',
            text=f"Price Increase: {price_increase_date}"
        ))

    fig.update_layout(
        plot_bgcolor='#2c3e50',
        paper_bgcolor='#2c3e50',
        margin=dict(l=0, r=0, b=0, t=50),
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.5, y=-1.5, z=1.5)
        ),
        font=dict(family="Arial", size=12, color="#ecf0f1"),
        title_font_size=24,
        title_x=0.5,
        scene=dict(
            xaxis=dict(backgroundcolor="#34495e", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            yaxis=dict(backgroundcolor="#34495e", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
            zaxis=dict(backgroundcolor="#34495e", gridcolor="rgba(255,255,255,0.1)", showbackground=True),
        )
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
