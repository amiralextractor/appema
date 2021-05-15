from data.loaddata import data

dfz = data[1]
dd = data[4]
dd=dd[dd["Classe Age"]==0]
dfz = dd.merge(dfz, left_on=['Departement',"Date"], right_on=['Departement',"Date"])

pop = data[2]
pop=pop[pop["Classe Age"]==0]
pop = pop[["Departement","Population"]]
pop=pop.groupby(["Departement","Population"]).size().reset_index(name='Incidence Hospitalise')
dfz=dfz.merge(pop, on='Departement', how='left')
dfz["Incidence Hospitalise"] = round((100000*dfz["Nv Hospitalise"].rolling(window=7).sum().values)/(dfz["Population"]),1)
dfz["Incidence Reanime"] = round((100000*dfz["Nv Reanime"].rolling(window=7).sum().values)/(dfz["Population"]),1)
dfz["Incidence Gueris"] = round((100000*dfz["Nv Gueris"].rolling(window=7).sum().values)/(dfz["Population"]),1)
dfz["Incidence Decede"] = round((100000*dfz["Nv Decede"].rolling(window=7).sum().values)/(dfz["Population"]),1)

cas = data[2]
cas=cas[cas["Classe Age"]==0]
cas["Departement"]=cas["Departement"].astype(str)
cas["Taux d'incidence Cas"] = round((100000*cas["Test Positif"].rolling(window=7).sum().values)/(cas["Population"]),1)

from Composants.shape import df_regions

dfz = dfz[dfz["Date"]==max(dfz["Date"])]
cas = cas[cas["Date"]==max(cas["Date"])]

dfz = dfz.merge(df_regions, left_on='Departement', right_on='departmentCode')
#dfz["Departement2"] = dfz[['departmentName', 'Departement']].agg(' - '.join, axis=1)

cas = cas.merge(df_regions, left_on='Departement', right_on='departmentCode')
#cas["Departement2"] = cas[['departmentName', 'Departement']].agg(' - '.join, axis=1)

import plotly.express as px

import json
with open('data/dep0.geojson') as response:
    depa = json.load(response)
	
print("load json 0")

with open('data/dep2.geojson') as response:
    depa2 = json.load(response)
	
print("load json 2")
    
with open('data/dep3.geojson') as response:
    depa3 = json.load(response)
	
print("load json 3")
    
with open('data/dep4.geojson') as response:
    depa4 = json.load(response)

print("load json 4")
    
with open('data/dep5.geojson') as response:
    depa5 = json.load(response)
	
print("load json 5")
    
with open('data/dep6.geojson') as response:
    depa6 = json.load(response)
	
print("load json 6")

    
df_map = dfz

menu = ["Taux d'incidence Cas","Taux d'incidence Hospitalisation","Taux d'incidence Reanimation","Taux d'incidence Décès","Taux d'incidence Guérison","Pourcentage Couverture Dose 1","Pourcentage Couverture Dose 2"]

df_map1 = dfz[dfz.Departement != "976"]
df_map1 = df_map1[df_map1.Departement != "974"]
df_map1 = df_map1[df_map1.Departement != "973"]
df_map1 = df_map1[df_map1.Departement != "972"]
df_map1 = df_map1[df_map1.Departement != "971"]

df_map2 = dfz[dfz.Departement == "971"]
df_map3 = dfz[dfz.Departement == "972"]
df_map4 = dfz[dfz.Departement == "973"]
df_map5 = dfz[dfz.Departement == "974"]
df_map6 = dfz[dfz.Departement == "976"]

cas1 = cas[cas.Departement != "976"]
cas1 = cas[cas.Departement != "974"]
cas1 = cas[cas.Departement != "973"]
cas1 = cas[cas.Departement != "972"]
cas1 = cas[cas.Departement != "971"]

cas2 = cas[cas.Departement == "971"]
cas3 = cas[cas.Departement == "972"]
cas4 = cas[cas.Departement == "973"]
cas5 = cas[cas.Departement == "974"]
cas6 = cas[cas.Departement == "976"]

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

fig = px.scatter()
fig.update_layout(
    plot_bgcolor='white',
    xaxis=dict(
        showline=False,
    ),
    yaxis=dict(
        showline=False,
    ))
maps = dbc.Row([
    dbc.Col([
            dcc.RadioItems(
                id='drop-incidence',
                options=[{'label': i, 'value': i} for i in menu],
                    value="Taux d'incidence Cas",
                    inputStyle={'margin-right': '5px'},
                    labelStyle={'margin-right': '10px'},
                    style={'display': 'grid'}
            )
    ],style={"align-self": "center"},md=3),
    dbc.Col(dbc.Card(dcc.Graph(id="graph-carte0",figure=fig,style={"height": "100%"})),style={"display":"grid"},md=7),
    dbc.Col([
            dbc.Row(dbc.Card(dcc.Graph(id="graph-carte1",figure=fig,config={'displayModeBar': False, 'scrollZoom': False},style={'height': '14vh',"width": "20vh"}))),
            dbc.Row(dbc.Card(dcc.Graph(id="graph-carte2",figure=fig,config={'displayModeBar': False, 'scrollZoom': False},style={'height': '14vh',"width": "20vh"}))),
            dbc.Row(dbc.Card(dcc.Graph(id="graph-carte3",figure=fig,config={'displayModeBar': False, 'scrollZoom': False},style={'height': '14vh',"width": "20vh"}))),
            dbc.Row(dbc.Card(dcc.Graph(id="graph-carte4",figure=fig,config={'displayModeBar': False, 'scrollZoom': False},style={'height': '14vh',"width": "20vh"}))),
            dbc.Row(dbc.Card(dcc.Graph(id="graph-carte5",figure=fig,config={'displayModeBar': False, 'scrollZoom': False},style={'height': '14vh',"width": "20vh"}))),
    ],style={"display":"grid"},md=2)
],className="mb-2")

import dash_table
tableau = dbc.Row([
        dbc.Col(md=3),
        dbc.Col([html.H6("Liste des départements en ordre décroissant:"),dash_table.DataTable(
                    id='datatable-paging',
                    columns=[
                        {"name": "Departement", "id": "Departement"},
                        {"name": "Nom Departement", "id": "Nom Departement"},
                        {"name": "Population", "id": "Population"},
                        {"name": "Valeur", "id": "Valeur"},
                    ],
                    page_current=0,
                    page_size=10,
                    page_action='custom',
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'},
                )
        ],md=7),
        dbc.Col(md=2)
    ])

page_Carto = [
    html.Div(id="titre-carte",style={"text-align":"center","margin-bottom":"30px"}),
    html.Div(maps),
    html.Br(),
    html.Div(tableau)
    ]