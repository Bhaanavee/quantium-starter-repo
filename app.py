import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
# Load and preprocess the data
try:
    df = pd.read_csv('processed_data.csv')
    df['date'] = pd.to_datetime(df['date'])
except FileNotFoundError:
    print("Error: The 'processed_data.csv' file was not found.")
    print("Please ensure you have completed the previous task and the file is in the correct directory.")
    raise PreventUpdate

df = df.sort_values(by='date')

# Dash App

app = dash.Dash(__name__)

# Designing Layout

fig = px.line(
    df,
    x="date",
    y="Sales",
    color="region",
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "Sales": "Total Sales ($)",
        "region": "Region"
    }
)

fig.add_vline(
    x='2021-01-15',
    line_width=2,
    line_dash="dash",
    line_color="red"
)

# Customize the layout for better readability.
fig.update_layout(
    plot_bgcolor='#f9f9f9',  
    paper_bgcolor='#ffffff', 
    font_family="Arial",
    font_color="#333",
    title_font_size=24,
    title_x=0.5,
    hovermode="x unified"
)

app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1(
        children='Soul Foods - Pink Morsel Sales Performance',
        style={
            'textAlign': 'center',
            'color': '#333',
            'margin-bottom': '20px'
        }
    ),

    html.Div(
        children='This dashboard visualizes the daily sales of Pink Morsels. The red dashed line indicates the date of the price increase on January 15th, 2021.',
        style={
            'textAlign': 'center',
            'color': '#666',
            'margin-bottom': '30px'
        }
    ),

    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
