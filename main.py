import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components.Div import Div
from dash_html_components.Hr import Hr
import plotly.express as px
from dash.dependencies import Input, Output, State
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import packages.utilities as ut
import plotly.figure_factory as ff
import math
import  matplotlib.pyplot  as  plt 



x = np.linspace(-1,1,30)
y = np.linspace(-1,1,30)

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

u = np.arange(  -2*np.pi , 2*np.pi,0.01)
v = np.arange(  -2*np.pi , 2*np.pi,0.01)

u,v = np.meshgrid(u,v)

XP = None
YP = None
ZP = None

pfig = go.Figure(data= [go.Surface(z=ZP,x=XP,y=YP)])
pfig.update_layout(
    margin=dict(l=1, r=4, t=10, b=10),
)

pcontour = go.Figure(data=
    go.Contour(z=ZP,y=YP,x=XP,
        contours_coloring='lines',
        line_width=2,
    )
)


app = dash.Dash(__name__ , suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.LITERA])
app.title="Graficador de Funciones"


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
        return tab_1()

    elif pathname == "/page-1":
        return tab_2()
    elif pathname == "/page-2":
        return tab_3()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"La ruta {pathname} no fue reconocida..."),
        ]
    )

def tab_3():
    return [ 
        html.H1('Sobre la Aplicacion', style={'textAlign':'center'}), 
        html.Div(children=[
            html.Img(src="/assets/espe.png",height="200px",width="200px"),
        ],className="logo"),
        html.H3("UNIVERSIDAD DE LAS FUERZAS ARMADAS ESPE",style={'textAlign':'center'}),
        html.H4("CALCULO VECTORIAL",style={'textAlign':'center'}),

        
    ]

def tab_2():
    return [ 
        html.H1('Ecuacion Parametrica', style={'textAlign':'center'}), 

        dbc.InputGroup(
            [
                dbc.InputGroupAddon("X(u,v)",addon_type="prepend"),

                html.Div(children=[dbc.Input(placeholder="radio",type="number")]),

                dbc.Input(placeholder="Ingresa tu ecuacion aqui", id="FX"),
            ],className="mb-3",
        ),

        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Y(u,v)", addon_type="prepend"),

                html.Div(children=[dbc.Input(placeholder="radio",type="number")]),

                dbc.Input(placeholder="Ingresa tu ecuacion aqui",id="FY"),
            ],className="mb-3",
        ),

        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Z(u,v)", addon_type="prepend"),

                html.Div(children=[dbc.Input(placeholder="radio",type="number")]),

                dbc.Input(placeholder="Ingresa tu ecuacion aqui", id="FZ"),
            ],className="mb-3",
            
        ),


        dbc.Row([ 

            dbc.Col( dbc.Label("   Limites de U: ", html_for="slider",style={'padding-top':20},), width=1.25, ), 
            
            dbc.Col( html.Div(children=[ 
                            dcc.RangeSlider(id="U_limit", min= -2*math.pi , max= 2*math.pi , step=0.01,value=[-2*math.pi,2*math.pi], 
                             tooltip={'placement':'bottom'},
                             marks={ 
                                    -2*math.pi:"-2𝝅", 
                                    -math.pi:"-𝝅", 
                                    0:"0", 
                                    math.pi:"𝝅", 
                                    2*math.pi:"2𝝅", 
                                }
                            ), 
                        ],style={"margin":20}), width=5, ), 
            
            dbc.Col( dbc.Label("Limites de V: ", html_for="slider",style={'padding-top':20},), width=1.25, ), 
            
            dbc.Col( html.Div(children=[ 
                            dcc.RangeSlider(id="V_limit", min= -2*math.pi , max= 2*math.pi, step=0.01,value=[0,math.pi],
                                tooltip={'placement':'bottom'},
                                marks={ 
                                    -2*math.pi:"-2𝝅", 
                                    -math.pi:"-𝝅", 
                                    0:"0", 
                                    math.pi:"𝝅", 
                                    2*math.pi:"2𝝅", 
                                } 
                            ),
                        ],style={"margin":20,}), width=5,align="center" )  ],justify="center"), 
            
            html.Div([ 
                dcc.Graph(id="pgraph",
                    figure=pfig,
                    style={"height":"100%","width":"100%",'margin':50}) 
            ],className="grafico"),  
            
            html.Hr(),  

            dbc.Row([

                dbc.Col(html.Div(children=[ 
                    dcc.Graph(id="pcontour",figure=pcontour) ])),
            
                dbc.Col(html.Div(children=[
                dcc.Graph(id ="quiver", figure=contour) ]))

            ]),

    ]

def tab_1():
    return [ 
        
        html.H1('Ecuacion Z = F(x,y)', style={'textAlign':'center'},id="out"), 
        
        dbc.Input(id="funtion",placeholder="Ingresa la ecuación aquí", type="text",bs_size="lg",value=""),  
        
        dbc.Row([ 

            dbc.Col( dbc.Label("Limites del eje X: ", html_for="slider",style={'padding-top':20},), width=1.25, ), 
            
            dbc.Col( html.Div(children=[ 
                            dcc.RangeSlider(id="xlim", min=-10, max=10, step=0.1,value=[-5,5], 
                            marks={x: str(x) for x in [-10, -5, 0, 5,10]}, tooltip={'placement':'bottom'} ), 
                        ],style={"margin":20}), width=4, ), 
            
            dbc.Col( dbc.Label("Limites del eje Y: ", html_for="slider",style={'padding-top':20},), width=1.25, ), 
            
            dbc.Col( html.Div(children=[ 
                            dcc.RangeSlider(id="ylim", min=-10, max=10, step=0.1,value=[-5,5],
                                 marks={x: str(x) for x in [-10, -5, 0, 5,10]}, tooltip={'placement':'bottom'} ), 
                            ],style={"margin":20,}), width=4,align="center" )  ],justify="center"),   
        
        html.Div([ 
            dcc.Graph(id="graph",figure=fig,style={"height":"100%","width":"100%",'margin':50}) ]
            ,className="grafico"),  
        
        html.Hr(),  
        
        html.H2("Curva de nivel"),  
        
        dbc.Row([

            dbc.Col(html.Div(children=[ 
                    dcc.Graph(id="contour",figure=contour) ])),
            
            dbc.Col(html.Div(children=[
                dcc.Graph(id ="quiver", figure=contour) ]))

        ]),

        #html.Div(children=[ 
         #   dcc.Graph(id="contour",figure=contour) ])  
        
        ]

"""Grafica y actualiza la funcion F(X,Y)"""
@app.callback(
    [Output("graph", "figure"),Output("contour", "figure")], 
    [Input('xlim', 'value'),
    Input('ylim', 'value'),
    Input("funtion","value")],  
    [State("graph", "figure")])
def funtion(xlim, ylim,funtion,figure):
    
        x = np.linspace(xlim[0],xlim[1],300)
        y = np.linspace(ylim[0],ylim[1],300)

        X , Y = np.meshgrid(x,y)

        Z = eval( ut.reemplazo(funtion) )

        fig = go.Figure(data= [go.Surface(z=Z,x=X,y=Y)])

        fig.update_layout(
            margin=dict(l=1, r=4, t=10, b=10),
            title={'text':"F(x,y): {}".format(funtion),'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'}
        ) 

        contour = go.Figure(data=
            go.Contour(z=Z,
            contours_coloring='lines',
            line_width=2,
            )
        )   

        #try:
        #    fig.write_image("plot.png")
        #    contour.write_image("contour.png")
        #except:
        #    fig.write_image("plot.png")
        #    contour.write_image("contour.png")


        return [fig,contour]

"""Pone de titulo la funcion que se grafica"""
@app.callback(
    Output("out", "children"), 
    [Input("funtion","value")])
def Funtion(input_value):
    return html.P('''F(x,y) = {}'''.format(input_value)),

"""Grafica y actualiza la funcion parametrica"""
@app.callback(
    Output("pgraph", "figure"), 
    [ #Inputs
    Input('U_limit', 'value'),
    Input('V_limit', 'value'),
    Input("FX","value"),
    Input("FY","value"),
    Input("FZ","value"),    
    ],  
    [State("pgraph", "figure")])
def parametric(u_lim,v_lim ,fx,fy,fz,figure):

    u = np.arange(  u_lim[0] , u_lim[1] ,0.01)
    v = np.arange(  v_lim[0] , v_lim[1] ,0.01)

    u,v = np.meshgrid(u,v)

    XP = eval( ut.reemplazo(fx) )
    YP = eval( ut.reemplazo(fy) )
    ZP = eval( ut.reemplazo(fz) )

    
    pfig = go.Figure(data= [go.Surface(z=ZP,x=XP,y=YP)])

    if np.amax(XP) > np.amax(YP):
        print("X>Y")
        pfig.update_layout(
            margin=dict(l=1, r=4, t=10, b=10),
            yaxis_range=[-15, 15],
            xaxis_range=[-15, 15]
        )
    else:
        print("Y>X")
        pfig.update_layout(
            margin=dict(l=1, r=4, t=10, b=10),
            xaxis_range=[-10, 10],
            yaxis_range=[-10, 10],
            
        )


    return pfig


if __name__=='__main__':
    app.run_server(debug=True, port=5500,use_reloader=True)

    