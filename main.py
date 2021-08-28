import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Label import Label
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components.Div import Div
from dash_html_components.Hr import Hr
from dash_html_components.Source import Source
import plotly.express as px
from dash.dependencies import Input, Output, State
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import packages.utilities as ut
import plotly.figure_factory as ff
import math
import  matplotlib.pyplot  as  plt 
import packages.PDF as file
from scipy.spatial import Delaunay

flagg = True

x = np.linspace(-1,1,30)
y = np.linspace(-1,1,30)

X , Y = np.meshgrid(x,y)

Z = None
Z1 =None

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

contour1 = go.Figure(data=
    go.Contour(z=Z1,
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
    [Input("url", "pathname")])
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
        html.Div(children=[
            html.Img(src="/assets/espe.png",height="150px",width="150px"),
        ],className="logo"),

        html.Div(children=[
            html.Img(src="/assets/ce.jpeg",height="150px",width="150px"),
        ],className="logo1"),

        html.H2("UNIVERSIDAD DE LAS FUERZAS ARMADAS ESPE",style={'fontFamily': 'Times New Roman','textAlign':'center','fontWeight':'bold'} ),
        html.H3("DEPARTEMENTO DE CIENCIAS EXACTAS",style={'fontFamily': 'Times New Roman','textAlign':'center','fontWeight':'bold'}),
        html.H3("CALCULO VECTORIAL",style={'fontFamily': 'Times New Roman','textAlign':'center'}),
        html.Hr(),
        html.H1(" Graficador de funciones ",style={'fontFamily': 'Times New Roman','textAlign':'center'}),
        html.Hr(),
        #html.H5("\a"),
       
        html.H5("✔ INTEGRANTES:", style={'fontFamily': 'Times New Roman','fontWeight':'bold','textAlign':'center'}),
        html.H5("   • Barriga Mateo ",style={'fontFamily': 'Times New Roman'}),
        html.H5("   • Carvajal Lisbeth",style={'fontFamily': 'Times New Roman'}),
        html.H5("   • Cedillo Nicolas",style={'fontFamily': 'Times New Roman'}),
        html.H5("   • López Steve",style={'fontFamily': 'Times New Roman'}),
        
        html.Hr(),
        
        html.H5("✔ DOCENTE:", style={'fontFamily': 'Times New Roman','textAlign':'center'}),
        html.H5("Ing. Nestor Mejía ",style={'fontFamily': 'Times New Roman','textAlign':'center'}),
        html.H5(),
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

            """"
            dbc.Row([
                
                dbc.Col(html.Div(children=[ 
                    html.Img(src="contour.png")     
                ],id="pcontour")
                ),
            
                dbc.Col(html.Div(children=[
                dcc.Graph(id ="quiver", figure=contour) ]))

            ]),
            """
    ]

def tab_1():
    return [ 
        
        html.H1('Ecuacion Z = F(x,y)', style={'textAlign':'center'},id="out"), 

        dbc.Row([

            dbc.Col(
                 dbc.Input(id="funtion",placeholder="Ingresa la ecuación aquí", type="text",bs_size="lg",value=""),
            ),

            dbc.Col(
                 dcc.Slider(
                    id='opacity1',min=0, max=1,
                    step=0.05, value=0.5,
                    marks={
                        0: {'label': '0 %', 'style': {'color': '#ff0000'}},
                        0.25: {'label': '35 %'},
                        0.5: {'label': '50 %'},
                        0.75: {'label': '75 %'},
                        1: {'label': '100 %', 'style': {'color': '#262ce0'}}
                    }
                )
            ),

        ]),


        #html.H1('Ecuacion Z = F(x,y)', style={'textAlign':'center'},id="out"), 
        
        #dbc.Input(id="funtion",placeholder="Ingresa la ecuación aquí", type="text",bs_size="lg",value=""),  
        
        html.Hr(),

        dbc.Button("Añadir otra curva",color="primary",id="both",n_clicks=0),

        dbc.Row(
            [   
                dbc.Col(    
                    dbc.Collapse(
                        dbc.Input(id="funtion2",
                                    placeholder="Ingresa la 2 ecuación aquí", 
                                    type="text",bs_size="lg",value=""
                                ),id="left-collapse",is_open=False,
                    )
                ),

                dbc.Col(
                    dbc.Collapse(

                        dcc.Slider(
                            id='opacity2',min=0, max=1,
                            step=0.05, value=0.5,
                            marks={
                                0: {'label': '0 %', 'style': {'color': '#ff0000'}},
                                0.25: {'label': '35 %'},
                                0.5: {'label': '50 %'},
                                0.75: {'label': '75 %'},
                                1: {'label': '100 %', 'style': {'color': '#262ce0'}}
                            }
                        ),id="right-collapse",is_open=False 
                    )
                ),
            ],className="mt-3"
        ),

        html.Hr(),

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
                dcc.Graph(id ="contour1", figure=contour1) ]))

        ]),

        #html.Div(children=[ 
         #   dcc.Graph(id="contour",figure=contour) ])  
        
        ]


"""Abre el panel para ingresar otra curva"""
@app.callback(
    Output("left-collapse", "is_open"),
    [Input("both", "n_clicks")],
    [State("left-collapse", "is_open")],
)
def toggle_left(n_both, is_open):
    if n_both:
        return not is_open
    return is_open


@app.callback(
    Output("right-collapse", "is_open"),
    [Input("both", "n_clicks")],
    [State("right-collapse", "is_open")],
)
def toggle_left(n_both, is_open):
    if n_both:
        return not is_open
    return is_open


"""Grafica y actualiza la funcion F(X,Y)"""
@app.callback(
    [
    Output("graph", "figure"),
    Output("contour", "figure"),
    Output("contour1", "figure")
    ], 
    [
    Input('xlim', 'value'),
    Input('ylim', 'value'),
    Input("funtion","value"),
    Input("opacity1","value"),
    Input("both", "n_clicks"),
    Input("funtion2","value"),
    Input("opacity2","value"),
    ],  
    [
    State("graph", "figure"),
    State("left-collapse", "is_open")
    ])
def funtion(xlim, ylim,funtion,opc1,n_both,fun2,opc2,figure,is_open):
    
        x = np.linspace(xlim[0],xlim[1],300)
        y = np.linspace(ylim[0],ylim[1],300)

        X , Y = np.meshgrid(x,y)

        flagg = is_open

        if not flagg:
            #print(flagg)

            Z = eval( ut.reemplazo(funtion) )

            fig = go.Figure(data= [go.Surface(z=Z,x=X,y=Y,opacity=opc1,colorscale='Blues')])

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

            try:
                fig.write_image("plot.png")
                contour.write_image("contour.png")
            except:
                fig.write_image("plot.png")
                contour.write_image("contour.png")

            return [fig,contour,None]

        else: 
            #print(flagg)

            Z = eval( ut.reemplazo(funtion) )
            Z1= eval( ut.reemplazo(fun2) )
            
            #print(ut.reemplazo(fun2))

            fig = go.Figure(data= [
                go.Surface(z=Z,x=X,y=Y,opacity=opc1,colorscale='Electric',showscale=False),
                go.Surface(z=Z1,x=X,y=Y,opacity=opc2,colorscale='YlGnBu',showscale=False),
                ]
            )

            fig.update_layout(
                margin=dict(l=1, r=4, t=10, b=10),
                title={'text':"F1(x,y): {} y F2(x,y): {}".format(funtion,fun2),'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'}
            ) 

            contour = go.Figure(data=
                go.Contour(z=Z,
                contours_coloring='lines',
                line_width=2,
                )
            )

            contour1 = go.Figure(data=
                go.Contour(z=Z1,
                contours_coloring='lines',
                line_width=2,
                )
            )

            try:
                fig.write_image("plot.png")
                contour.write_image("contour.png")
            except:
                fig.write_image("plot.png")
                contour.write_image("contour.png")

            return[fig,contour,contour1]
        

        #pdf = file.PDF("PRUEBA",funtion)
        #pdf.makePDF()

        #return [fig,contour]

"""Pone de titulo la funcion que se grafica"""
@app.callback(
    Output("out", "children"), 
    [Input("funtion","value")])
def Funtion(input_value):
    return html.P('''F(x,y) = {}'''.format(input_value)),


def plot():
    CS = plt.contour(XP,YP,ZP)
    plt.clabel(CS,inline=True,fontsize=10)
    plt.savefig("contour.png")

"""Grafica y actualiza la funcion parametrica"""
@app.callback(
    [Output("pgraph", "figure")], 
    [ #Inputs
    Input('U_limit', 'value'),
    Input('V_limit', 'value'),
    Input("FX","value"),
    Input("FY","value"),
    Input("FZ","value"),    
    ],  
    [State("pgraph", "figure")])
def parametric(u_lim,v_lim ,fx,fy,fz,figure):

    u = np.linspace(  u_lim[0] , u_lim[1] ,20)
    v = np.linspace(  v_lim[0] , v_lim[1] ,20)

    u,v = np.meshgrid(u,v)

    u = u.flatten()
    v = v.flatten()

    XP = eval( ut.reemplazo(fx) )
    YP = eval( ut.reemplazo(fy) )
    ZP = eval( ut.reemplazo(fz) )

    points2D = np.vstack([u,v]).T
    tri = Delaunay(points2D)
    simplices = tri.simplices
    
    #pfig = go.Figure(data= [go.Surface(z=ZP,x=XP,y=YP)], )
    pfig = ff.create_trisurf(x=XP, y=YP, z=ZP,
                        simplices=simplices,
                        width=1000,height=600
                    )

    
    if np.amax(XP) > np.amax(YP):
        
        pfig.update_layout(
            margin=dict(l=1, r=1, t=1, b=1),
            scene = dict(
                yaxis=dict(range=[ -np.amax(XP) , np.amax(XP) ]),
                xaxis=dict(range=[ -np.amax(XP) , np.amax(XP) ]),
                xaxis_title='EJE X',
                yaxis_title='EJE Y',
                zaxis_title='EJE Z',
            ),  
        )
    else:
        pfig.update_layout(
            margin=dict(l=1, r=4, t=1, b=1),
            scene = dict(
                yaxis=dict(range=[ -np.amax(YP) , np.amax(YP) ]),
                xaxis=dict(range=[ -np.amax(YP) , np.amax(YP) ]),
                xaxis_title='EJE X',
                yaxis_title='EJE Y',
                zaxis_title='EJE Z',
            ),  
            
        )
    

    return [pfig]


if __name__=='__main__':
    app.run_server(debug=True, port=5500,use_reloader=True)

    