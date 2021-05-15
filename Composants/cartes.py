import dash_bootstrap_components as dbc
import dash_html_components as html
from data.loaddata import data

df = data[5]
cas= "Total Cas"
nvcas = df[cas][len(df)-1]-df[cas][len(df)-2]
datenvcas = str("Le "+str(df["Date"][len(df)-1]))
mean7j = int(round(sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(1,8))/7,0))

delta1 = int(round((nvcas-(df[cas][len(df)-8]-df[cas][len(df)-9]))/(df[cas][len(df)-8]-df[cas][len(df)-9])*100,0))
if delta1 > 0:
    couldelta1 = "#dc3545"
    delta1 = str("+"+str(delta1)+"% ▲")
else:
    couldelta1 = "#4fa746"
    delta1 = str(str(delta1)+"% ▼")
    
delta2 = int(round((sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(1,8))-sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(8,15)))/sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(8,15))*100))
if delta2 > 0:
    couldelta2 = "#dc3545"
    delta2 = str("+"+str(delta2)+"% ▲")
else:
    couldelta2 = "#4fa746"
    delta2 = str(str(delta2)+"% ▼")

card_cas = [
    dbc.CardHeader("Nouveaux cas",style={"background-color":"#007bff", "color":"white"}),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([html.H2(nvcas,style={"margin-bottom":"0px"}),
                        html.P(datenvcas,style={"font-size":"80%"}),
                        html.H2(mean7j,style={"margin-bottom":"0px"}),
                        html.P("Moyenne 7j",style={"font-size":"80%"})
                ]),
                dbc.Col([html.H5(delta1,style={"margin-bottom":"0px","margin-top":"6px","color":couldelta1}),
                         html.P("Delta 7j",style={"font-size":"80%","margin-bottom":"28px"}),
                        html.H5(delta2,style={"margin-bottom":"0px","color":couldelta2}),
                        html.P("Delta 7j",style={"font-size":"80%"}),
                ],style={"padding":"0%"}),
            ]),
        ]
    ),
]

cas= "Nouveaux hospitalises"
nvcas = df[cas][len(df)-2]
datenvcas = str("Le "+str(df["Date"][len(df)-1]))
mean7j = int(round(sum(df[cas][len(df)-a] for a in range(1,8))/7,0))

delta1 = int(round((nvcas-(df[cas][len(df)-8]))/(df[cas][len(df)-9])*100,0))
if delta1 > 0:
    couldelta1 = "#dc3545"
    delta1 = str("+"+str(delta1)+"% ▲")
else:
    couldelta1 = "#4fa746"
    delta1 = str(str(delta1)+"% ▼")
    
delta2 = int(round((sum(df[cas][len(df)-a] for a in range(1,8))-sum(df[cas][len(df)-a] for a in range(8,15)))/sum(df[cas][len(df)-a] for a in range(8,15))*100))
if delta2 > 0:
    couldelta2 = "#dc3545"
    delta2 = str("+"+str(delta2)+"% ▲")
else:
    couldelta2 = "#4fa746"
    delta2 = str(str(delta2)+"% ▼")

card_hospit = [
    dbc.CardHeader("Personnes hospitalisées",style={"background-color":"#6c757d", "color":"white"}),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([html.H2(nvcas,style={"margin-bottom":"0px"}),
                        html.P(datenvcas,style={"font-size":"80%"}),
                        html.H2(mean7j,style={"margin-bottom":"0px"}),
                        html.P("Moyenne 7j",style={"font-size":"80%"})
                ]),
                dbc.Col([html.H5(delta1,style={"margin-bottom":"0px","margin-top":"6px","color":couldelta1}),
                         html.P("Delta 7j",style={"font-size":"80%","margin-bottom":"28px"}),
                        html.H5(delta2,style={"margin-bottom":"0px","color":couldelta2}),
                        html.P("Delta 7j",style={"font-size":"80%"}),
                ],style={"padding":"0%"}),
            ]),
        ]
    ),
]

cas= "Nouveaux Reanimes"
nvcas = df[cas][len(df)-2]
datenvcas = str("Le "+str(df["Date"][len(df)-1]))
mean7j = int(round(sum(df[cas][len(df)-a] for a in range(1,8))/7,0))

delta1 = int(round((nvcas-(df[cas][len(df)-8]))/(df[cas][len(df)-9])*100,0))
if delta1 > 0:
    couldelta1 = "#dc3545"
    delta1 = str("+"+str(delta1)+"% ▲")
else:
    couldelta1 = "#4fa746"
    delta1 = str(str(delta1)+"% ▼")
    
delta2 = int(round((sum(df[cas][len(df)-a] for a in range(1,8))-sum(df[cas][len(df)-a] for a in range(8,15)))/sum(df[cas][len(df)-a] for a in range(8,15))*100))
if delta2 > 0:
    couldelta2 = "#dc3545"
    delta2 = str("+"+str(delta2)+"% ▲")
else:
    couldelta2 = "#4fa746"
    delta2 = str(str(delta2)+"% ▼")

card_rea = [
    dbc.CardHeader("Personnes en réanimation",style={"background-color":"#ffc107"}),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([html.H2(nvcas,style={"margin-bottom":"0px"}),
                        html.P(datenvcas,style={"font-size":"80%"}),
                        html.H2(mean7j,style={"margin-bottom":"0px"}),
                        html.P("Moyenne 7j",style={"font-size":"80%"})
                ]),
                dbc.Col([html.H5(delta1,style={"margin-bottom":"0px","margin-top":"6px","color":couldelta1}),
                         html.P("Delta 7j",style={"font-size":"80%","margin-bottom":"28px"}),
                        html.H5(delta2,style={"margin-bottom":"0px","color":couldelta2}),
                        html.P("Delta 7j",style={"font-size":"80%"}),
                ],style={"padding":"0%"}),
            ]),
        ]
    ),
]

cas= "Total Deces"
nvcas = df[cas][len(df)-1]-df[cas][len(df)-2]
datenvcas = str("Le "+str(df["Date"][len(df)-1]))
mean7j = int(round(sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(1,8))/7,0))

delta1 = int(round((nvcas-(df[cas][len(df)-9]-df[cas][len(df)-10]))/(df[cas][len(df)-9]-df[cas][len(df)-10])*100,0))
if delta1 > 0:
    couldelta1 = "#dc3545"
    delta1 = str("+"+str(delta1)+"% ▲")
else:
    couldelta1 = "#4fa746"
    delta1 = str(str(delta1)+"% ▼")
    
delta2 = int(round((sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(1,8))-sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(9,16)))/sum(df[cas][len(df)-a]-df[cas][len(df)-a-1] for a in range(9,16))*100))
if delta2 > 0:
    couldelta2 = "#dc3545"
    delta2 = str("+"+str(delta2)+"% ▲")
else:
    couldelta2 = "#4fa746"
    delta2 = str(str(delta2)+"% ▼")

card_deces = [
    dbc.CardHeader("Nouveaux décès",style={"background-color":"#dc3545", "color":"white"}),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([html.H2(nvcas,style={"margin-bottom":"0px"}),
                        html.P(datenvcas,style={"font-size":"80%"}),
                        html.H2(mean7j,style={"margin-bottom":"0px"}),
                        html.P("Moyenne 7j",style={"font-size":"80%"})
                ]),
                dbc.Col([html.H5(delta1,style={"margin-bottom":"0px","margin-top":"6px","color":couldelta1}),
                         html.P("Delta 7j",style={"font-size":"80%","margin-bottom":"28px"}),
                        html.H5(delta2,style={"margin-bottom":"0px","color":couldelta2}),
                        html.P("Delta 7j",style={"font-size":"80%"}),
                ],style={"padding":"0%"}),
            ]),
        ]
    ),
]

df = data[3]
df = df[df["Classe Age"] == 0]
df = df[df["Date"] == max(df["Date"])]
dose1 = df["Cumul Dose 1"]
dose2 = df["Cumul complet"]
pop = 67407000 # au 29 Mars 2021

card_vacs = [
    dbc.CardHeader("Personnes vaccinées",style={"background-color":"#28a745", "color":"white"}),
    dbc.CardBody(
        [
            dbc.Row([
                html.H2(dose1),
                html.P("Dose 1",style={"margin": "11px"})
            ],style={"display":"flex"}),
            dbc.Row([
                dbc.Progress(str(str(int(round(dose1*100/pop,0)))+"%"), value=dose1*100/pop)
            ], style={"display":"block","margin-bottom":"11px"}),
            dbc.Row([
                html.H2(dose2),
                html.P("Dose 2",style={"margin": "11px"})
            ],style={"display":"flex"}),
            dbc.Row([
                dbc.Progress(str(str(int(round(dose2*100/pop,0)))+"%"), value=dose2*100/pop, color="success")
            ],style={"display":"block","margin-bottom":"10px"})
        ]
    ),
]

cards = dbc.Row(
    [
        dbc.Col(dbc.Card(card_cas, color="primary", outline=True)),
        dbc.Col(dbc.Card(card_hospit, color="secondary", outline=True)),
        dbc.Col(dbc.Card(card_rea, color="warning", outline=True)),
        dbc.Col(dbc.Card(card_deces, color="danger", outline=True)),
        dbc.Col(dbc.Card(card_vacs, color="success", outline=True)),
    ],
    className="mb-5",
)