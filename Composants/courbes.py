import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px

from Composants.shape import shapegraph

from data.loaddata import data
df = data[0]
from Composants.shape import df_regions
import pandas as pd
dfr = df_regions[["departmentCode","departmentName"]]
dd = pd.DataFrame(sorted(df['Departement'].unique()))
dd = dd.merge(dfr, left_on=0, right_on='departmentCode')
dd["Departement2"] = dd[['departmentName', 'departmentCode']].agg(' - '.join, axis=1)

fig = px.scatter()
fig.update_layout(
    plot_bgcolor='white',
    xaxis=dict(
        showline=False,
    ),
    yaxis=dict(
        showline=False,
    ))

filtres = [
        dbc.Col([html.H6("Sexe:"),
            dcc.Checklist(id="check-sexe",
                options=[
                    {'label': 'Femme', 'value': 2},
                    {'label': 'Homme', 'value': 1}
                ],
                value=[2,1],
                inputStyle={'margin-right': '5px'},
                labelStyle={'display': 'inline-block','margin-right': '10px'}
            )
        ],md=2),
        dbc.Col([html.H6("Département:"),
            dcc.Dropdown(
                id='drop-departement',
                options=[{'label': i, 'value': j} for i, j in zip(dd["Departement2"], dd["departmentCode"])],
                    multi=False,
                    placeholder="Tous les départements",
            )
        ],md=3),
]

Graph1 = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(dcc.Markdown("#### **Cas positifs**")),
            dbc.Col(dcc.RadioItems(id="radio-type-graph1",
                options=[
                    {'label': 'Linéaire', 'value': 1},
                    {'label': 'Logarithmique', 'value': 2}
                ],
                value=1,
                inputStyle={'margin-right': '5px'},
                labelStyle={'display': 'inline-block','margin-right': '10px'})
            ,md=5,style={"align-self": "center"})
        ]),style={"background-color":"#007bff","color":"white"}
    ),
    dbc.CardBody(
        [
            dcc.Graph(id="graph1",figure=fig)
        ]
    ),
]

Graph2 = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(dcc.Markdown("#### **Personnes hospitalisées**")),
            dbc.Col(dcc.RadioItems(id="radio-type-graph2",
                options=[
                    {'label': 'Linéaire', 'value': 1},
                    {'label': 'Logarithmique', 'value': 2}
                ],
                value=1,
                inputStyle={'margin-right': '5px'},
                labelStyle={'display': 'inline-block','margin-right': '10px'})
            ,md=5,style={"align-self": "center"})
        ]),style={"background-color":"#6c757d","color":"white"}
    ),
    dbc.CardBody(
        [
            dcc.Graph(id="graph2",figure=fig)
        ]
    ),
]

Graph3 = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(dcc.Markdown("#### **Personnes en réanimation**")),
            dbc.Col(dcc.RadioItems(id="radio-type-graph3",
                options=[
                    {'label': 'Linéaire', 'value': 1},
                    {'label': 'Logarithmique', 'value': 2}
                ],
                value=1,
                inputStyle={'margin-right': '5px'},
                labelStyle={'display': 'inline-block','margin-right': '10px'})
            ,md=5,style={"align-self": "center"})
        ]),style={"background-color":"#ffc107"}
    ),
    dbc.CardBody(
        [
            dcc.Graph(id="graph3",figure=fig)
        ]
    ),
]

Graph4 = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(dcc.Markdown("#### **Décès hospitaliers**")),
            dbc.Col(dcc.RadioItems(id="radio-type-graph4",
                options=[
                    {'label': 'Linéaire', 'value': 1},
                    {'label': 'Logarithmique', 'value': 2}
                ],
                value=1,
                inputStyle={'margin-right': '5px'},
                labelStyle={'display': 'inline-block','margin-right': '10px'})
            ,md=5,style={"align-self": "center"})
        ]),style={"background-color":"#dc3545","color":"white"}
    ),
    dbc.CardBody(
        [
            dcc.Graph(id="graph4",figure=fig)
        ]
    ),
]

Graph5 = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(dcc.Markdown("#### **Personnes guéries**")),
            dbc.Col(dcc.RadioItems(id="radio-type-graph5",
                options=[
                    {'label': 'Linéaire', 'value': 1},
                    {'label': 'Logarithmique', 'value': 2}
                ],
                value=1,
                inputStyle={'margin-right': '5px'},
                labelStyle={'display': 'inline-block','margin-right': '10px'})
            ,md=5,style={"align-self": "center"})
        ]),style={"background-color":"#4fa746","color":"white"}
    ),
    dbc.CardBody(
        [
            dcc.Graph(id="graph5",figure=fig)
        ]
    ),
]

Courbes = dbc.Row([
        dbc.Row([
            dbc.Col(dbc.Card(Graph1, color="primary", outline=True), md=6),
            dbc.Col(dbc.Card(shapegraph, outline=False), md=6),
        ]),
        dbc.Row(filtres,style={"padding":"20px"}),
        dbc.Row(
        [
            dbc.Col(dbc.Card(Graph2, color="secondary", outline=True), md=6),
            dbc.Col(dbc.Card(Graph3, color="warning", outline=True), md=6)
        ],style={"margin-bottom":"20px"}),
        dbc.Row(
        [
            dbc.Col(dbc.Card(Graph4, color="danger", outline=True), md=6),
            dbc.Col(dbc.Card(Graph5, color="success", outline=True), md=6)
        
        ])
],style={"display":"block"})