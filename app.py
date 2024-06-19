from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio
from prep_data import total_cert, year, month, fig1, fig2, fig3, table4, MAIN_COLOR
from flask import Flask

load_figure_template("lumen")
pio.templates.default = "lumen+seaborn"
flask_server = Flask(__name__)
dash_app = Dash(__name__,
                server=flask_server,
                external_stylesheets=[dbc.themes.LUMEN],
                title="DoHoangLam Certificates")
app = dash_app.server

# Header
header = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Do Hoang Lam",
                    className='mx-2 mt-2',
                    style={'font-size': '52px',
                           'color': MAIN_COLOR}),
            html.H4("Production Engineer", className='mx-2'),
            html.H6("Email: lamdohoang24@gmail.com", className='mx-2'),
            html.H6("Phone: (+84) 935 903 612", className='mx-2'),
            html.H6([
                html.Span("LinkedIn: "),
                html.A("https://www.linkedin.com/in/loodinon/",
                       href="https://www.linkedin.com/in/loodinon/", target='_blank')
            ], className='mx-2'),
        ], width=6),
        dbc.Col([
            html.Div([
                html.Span(total_cert,
                          style={'font-size': '60px', 'color': MAIN_COLOR}),
                html.Span(" Certificates",
                          style={'font-size': '40px'})
            ], style={'textAlign': 'right'}, className='mx-2 mt-4'),
            html.Div([
                html.Span("over ",
                          style={'font-size': '24px'}),
                html.Span(f"{year} Years",
                          style={'font-size': '38px', 'color': MAIN_COLOR}),
                html.Span(" and ",
                          style={'font-size': '24px'}),
                html.Span(f"{month} Months",
                          style={'font-size': '38px', 'color': MAIN_COLOR}),
            ], style={'textAlign': 'right'}),
        ], width=6),
    ], justify="between"),
    html.Hr(className='m-1')
])


table_btn = html.Div([
    dbc.Button(html.Img(src='assets/table.png', height='20px'),
               className="btn mx-1 mb-1",
               n_clicks=0,
               id='table-button',
               style={"float": "right",
                      'background-color': MAIN_COLOR, 'color': 'white'}
               ),
])

graph_data = dbc.Row([
    dbc.Col(
        dcc.Graph(figure=fig1, id="graph_1", style={
                  'height': '100%'}, config={'displayModeBar': False}),
        width=8,
        style={'display': 'flex', 'flex-direction': 'column', 'height': '70vh'}
    ),
    dbc.Col([
        dcc.Graph(figure=fig2, id="graph_2", style={
                  'height': '50%'}, config={'displayModeBar': False}),
        dcc.Graph(figure=fig3, id="graph_3", style={'height': '50%'}, config={'displayModeBar': False})],
        width=4,
        style={'display': 'flex', 'flex-direction': 'column', 'height': '70vh'})
], style={'height': '70vh'})

table_data = table4

graph = html.Div([
    dbc.Row(table_btn),
    html.Div(graph_data, id="graph")
])

# Layout
dash_app.layout = dbc.Container([header, graph], className='dbc', fluid=True)

# Callback


@dash_app.callback(
    Output("graph", "children"),
    Input('table-button', 'n_clicks')
)
def swap(n):
    if n is None:
        return graph_data
    elif n % 2 == 0:
        return graph_data
    else:
        return table_data


# Run
if __name__ == '__main__':
    dash_app.run_server(debug=False)
