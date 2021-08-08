import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components.Hr import Hr
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go

MATHJAX_CDN = '''
https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/
MathJax.js?config=TeX-MML-AM_CHTML'''

external_scripts = [
                    {'type': 'text/javascript',
                     'id': 'MathJax-script',
                     'src': MATHJAX_CDN,
                     },
                    ]


x = np.linspace(-1,1,300)
y = np.linspace(-1,1,300)

X , Y = np.meshgrid(x,y)

Z = None

fig = go.Figure(data= [go.Surface(z=Z,x=X,y=Y)])
fig.update_layout(
    margin=dict(l=1, r=4, t=10, b=10),
    #paper_bgcolor="LightSteelBlue",
)

contour = go.Figure(data=
    go.Contour(z=Z,
        contours_coloring='lines',
        line_width=2,
    )
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA],suppress_callback_exceptions=True,external_scripts=external_scripts)


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f9f8fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Graficador de funciones", className="display-4"),
        html.Hr(),
        html.P(
            "Selecciona tu tipo de entrada", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Funcion F(x,y)", href="/", active="exact"),
                dbc.NavLink("Ecuación parametrica", href="/page-1", active="exact"),
                dbc.NavLink("Sobre la aplicación", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Ecuacion Z = F(x,y)',
                        style={'textAlign':'center'},id="out"),
                dbc.Input(id="funtion",placeholder="Ingresa la ecuación aquí", type="text",bs_size="lg",value=""),

                dbc.Row([
                    dbc.Col(
                        dbc.Label("Limites del eje X: ", html_for="slider",style={'padding-top':20},),
                        width=1.25,
                    ),
                    dbc.Col(
                        html.Div(children=[
                            dcc.RangeSlider(id="xlim", min=-10, max=10, step=0.1,value=[-5,5],
                                marks={x: str(x) for x in [-10, -5, 0, 5,10]},
                                tooltip={'placement':'bottom'}
                                ),
                        ],style={"margin":20}),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Label("Limites del eje Y: ", html_for="slider",style={'padding-top':20},),
                        width=1.25,
                    ),
                    dbc.Col(
                        html.Div(children=[
                            dcc.RangeSlider(id="ylim", min=-10, max=10, step=0.1,value=[-5,5],
                                marks={x: str(x) for x in [-10, -5, 0, 5,10]},
                                tooltip={'placement':'bottom'}
                                ),
                        ],style={"margin":20,}),
                        width=4,align="center"
                    )
                    
                ],justify="center"),


                html.Div([
                    dcc.Graph(id="graph",figure=fig,style={"height":"100%","width":"100%",'margin':50})
                    ],className="grafico"),

                html.Hr(),

                html.H2("Curva de nivel"),

                html.Div(children=[
                    dcc.Graph(id="contour",figure=contour)        
                ])

                ]



    elif pathname == "/page-1":
        return [
                html.H1('Ecuacion Parametrica',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=fig)
                ]
    elif pathname == "/page-2":
        return [
                html.H1('Sobre la Aplicacion',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=fig)
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"La ruta {pathname} no fue reconocida..."),
        ]
    )

@app.callback(
    [Output("graph", "figure"),Output("contour", "figure")], 
    [Input('xlim', 'value'),Input('ylim', 'value'),Input("funtion","value")],  
    [State("graph", "figure")])
def x_limit(xlim, ylim,funtion,figure):
    
        x = np.linspace(xlim[0],xlim[1],300)
        y = np.linspace(ylim[0],ylim[1],300)

        X , Y = np.meshgrid(x,y)

        Z = eval(funtion)

        fig = go.Figure(data= [go.Surface(z=Z,x=X,y=Y)])

        fig.update_layout(
            margin=dict(l=1, r=4, t=10, b=10)
        ) 

        contour = go.Figure(data=
            go.Contour(z=Z,
            contours_coloring='lines',
            line_width=2,
        )
)

        return [fig,contour]

@app.callback(
    Output("out", "children"), 
    [Input("funtion","value")])
def x_limit(input_value):
    return html.P('''F(x,y) = {}'''.format(input_value)),


if __name__=='__main__':
    app.run_server(debug=True, port=3000)

    