import json
import dash
from dash import Dash, html, dcc, callback
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import numpy as np
import base64

try:
    import fig_layout
    import wrangle
except ImportError as e:
    print(f"Warning: Could not import custom modules: {e}")

    class DummyWrangle:
        toatl_funding = "1,234" 
        toatl_number_unicorn = "567"  
        total_valuation = "890"
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()
        fig5 = go.Figure()
        df = pd.DataFrame({'Industry': ['Fintech', 'E-commerce', 'AI'], 
                        'Founded Year': [2010, 2015, 2020],
                        'Country': ['USA', 'China', 'UK'],
                        'Select Investors': ['Investor A, Investor B', 'Investor C', 'Investor D']})
    class DummyFigLayout:
        my_figlayout = {}
    
    wrangle = DummyWrangle()
    fig_layout = DummyFigLayout()


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],  
    title="Billion Dollar Startups Dashboard"
)
app.layout = dbc.Container([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H1(
                    "Startups Companies",
                    className="custom-heading",
                    style={'fontSize': '4.5rem','fontWeight':'bold'}
                )
            ], className="d-flex align-items-center justify-content-center h-100")
        ], className="compound-card", style={"height": "100px"}),
    ], width=12),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div('Total Funding', style={'fontSize': '1.5rem','fontWeight':'bold'})
                ),
                dbc.CardBody([
                    html.Div(
                        f"{wrangle.toatl_funding} $M",
                        style={'fontSize': '2.5rem','fontWeight':'bold'}
                    )
                ])
            ], className="compound-card", id="banner_funding"),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div('Total Number Unicorn', style={'fontSize': '1.5rem','fontWeight':'bold'})
                ),
                dbc.CardBody([
                    html.Div(
                        f"#{wrangle.toatl_number_unicorn}",
                        style={'fontSize': '2.5rem','fontWeight':'bold'}
                    )
                ])
            ], className="compound-card", id="banner_unicorn"),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div('Total Valuation', style={'fontSize': '1.5rem','fontWeight':'bold'})
                ),
                dbc.CardBody([
                    html.Div(
                        f"~ {wrangle.total_valuation} $B",
                        style={'fontSize': '2.5rem','fontWeight':'bold'}
                    )
                ])
            ], className="compound-card", id="banner_valuation"),
        ], width=4),
    ], className='mb-3'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="figurefour", figure=wrangle.fig4)
                ])
            ], className="compound-card"),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="next-graph", figure=wrangle.fig2)
                ])
            ], className="compound-card"),
        ], width=6),
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        options=[{'label': industry, 'value': industry} 
                                for industry in wrangle.df.Industry.unique().tolist()],
                        value="Fintech", 
                        id='demo-dropdown'
                    ),
                    dcc.Graph(id="figurethree", figure={})
                ])
            ], className="compound-card"),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="figureone", figure=wrangle.fig5)
                ])
            ], className="compound-card"),
        ], width=6),
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="figureFive", figure=wrangle.fig3)
                ])
            ], className="compound-card"),
        ], width=6, className="mx-auto"),  
    ]),
], fluid=True)

@app.callback(
    Output("figurethree", "figure"),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    df = wrangle.df.copy(deep=True)
    fig1 = go.Figure()
    fig1.update_layout(
        title='Select an industry from dropdown',
        xaxis_title='Year',
        yaxis_title='Count'
    )
    if value and value in df['Industry'].values:
        df_filtered = df[df['Industry'] == value]
        df_with_fyear = df_filtered[~df_filtered['Founded Year'].isna()]
        
        if not df_with_fyear.empty:
            num_by_founded_year = df_with_fyear["Founded Year"].value_counts().reset_index()
            num_by_founded_year.columns = ["year", "count"]
            num_by_founded_year["year"] = num_by_founded_year["year"].astype(int)
            num_by_founded_year = num_by_founded_year[num_by_founded_year["year"] >= 1990]
            num_by_founded_year.sort_values(by=["year"], inplace=True)
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=num_by_founded_year["year"],
                y=num_by_founded_year["count"],
                fillcolor='rgba(178, 211, 194,0.11)', 
                fill='tonexty',
                mode='lines+markers',
                line_color='#3DED97',
                name=f'{value} Companies'
            ))
            
            fig1.update_layout(
                title=f'Companies Founded by Year - {value}',
                xaxis_title='Founded Year',
                yaxis_title='Number of Companies'
            )
            if hasattr(fig_layout, 'my_figlayout'):
                fig1.update_layout(fig_layout.my_figlayout)
    
    return fig1
@app.callback(
    Output('next-graph', 'figure'),
    Input('figurefour', 'hoverData')
)
def update_graph(option_slctd):
    df = wrangle.df.copy(deep=True)
    
    title = "Top 10 Investors"
    
    if option_slctd:
        try:
            selected_country = option_slctd['points'][0]['hovertext']
            filtered_df = df[df['Country'] == selected_country]
            title = f"Top Investors in {selected_country}"
        except (KeyError, IndexError):
            filtered_df = df
    else:
        filtered_df = df
    investors = []
    for i, row in filtered_df.iterrows():
        if pd.notna(row.get("Select Investors")):
            investors.extend(row["Select Investors"].split(', '))
    
    if investors:
        investors_series = pd.Series(investors).value_counts()[:10]
        investors_series.sort_values(ascending=True, inplace=True)
        
        fig2 = go.Figure([
            go.Bar(
                x=investors_series.values, 
                y=investors_series.index, 
                orientation='h',
                marker=dict(color='#3DED97')
            )
        ])
    else:
        fig2 = go.Figure()
        fig2.add_annotation(
            text="No investor data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig2.update_layout(
        title=title,
        xaxis_title='Number of Investments',
        yaxis_title='Investors'
    )
    if hasattr(fig_layout, 'my_figlayout'):
        fig2.update_layout(fig_layout.my_figlayout)
    
    return fig2

if __name__ == '__main__':
    app.run(debug=True, port=8001)
