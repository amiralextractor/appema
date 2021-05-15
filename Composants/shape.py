import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_html_components as html

from data.loaddata import data

###data1
import pandas as pd

#path = "C:/Users/Marouane/Dropbox/Partage/M2/Projet transversal/dash/"
path=""

df_regions = pd.read_csv(path+"data/departments_regions_france_2016.csv", sep=",")#fichier csv avec la liste des régions en France
print("load df region")
df_reg_pop = pd.read_csv(path+"data/population_grandes_regions.csv", sep=",")
print("load df region pop")
df_dep_pop = pd.read_csv(path+"data/dep-pop.csv", sep=";")
print("load df dep pop")
df_dep_pop.columns = ["Departement","departementPopulation"]

df_incid = data[2]
df_incid["Departement"]=df_incid["Departement"].astype(str)
df_incid = df_incid.merge(df_regions, left_on='Departement', right_on='departmentCode')
df_incid = df_incid.merge(df_reg_pop, left_on='regionName', right_on='regionName')
df_incid = df_incid.merge(df_dep_pop, left_on='Departement', right_on='Departement')


###
df = data[0]
df = df.merge(df_regions, left_on='Departement', right_on='departmentCode')
df = df.merge(df_reg_pop, left_on='regionName', right_on='regionName')
df = df.merge(df_dep_pop, left_on='Departement', right_on='Departement')
df = df[df["Sexe"] == 0]

df_departements = df.groupby(["Date", "departmentName"]).sum().reset_index()
df_incid_departements = df_incid[df_incid["Classe Age"]==0].groupby(["Date", "departmentName", "Departement"]).sum().reset_index()

df_new = data[1]
df_new = df_new.merge(df_regions, left_on='Departement', right_on='departmentCode')
df_new = df_new.merge(df_reg_pop, left_on='regionName', right_on='regionName')
df_new = df_new.merge(df_dep_pop, left_on='Departement', right_on='Departement')
df_new['incid_hosp_nonrea'] = df_new['Nv Hospitalise'] - df_new['Nv Reanime']

df_new_departements = df_new.groupby(["Date", "departmentName"]).sum().reset_index()

departements = list(dict.fromkeys(list(df_departements['departmentName'].values))) 

dates_incid = list(dict.fromkeys(list(df_incid['Date'].values))) 

n_tot=1
for i in range(0, n_tot):
    evol_tests_deps, evol_hosp_deps = [], []

    fig = go.Figure()
    fig.add_shape(type="rect",
            x0=-1000, y0=0, x1=0, y1=1000,
            line=dict(color="orange",width=0.5, dash="dot"), fillcolor="orange", opacity=0.2,
            layer="below"
        )
    fig.add_shape(type="rect",
            x0=0, y0=-1000, x1=1000, y1=0,
            line=dict(color="orange",width=0.5, dash="dot"), fillcolor="orange", opacity=0.2,
            layer="below"
        )

    fig.add_shape(type="rect",
            x0=0, y0=0, x1=1000, y1=1000,
            line=dict(color="Red",width=0.5, dash="dot"), fillcolor="red", opacity=0.2,
            layer="below"
        )

    fig.add_shape(type="rect",
            x0=-1000, y0=-1000, x1=0, y1=0,
            line=dict(color="red",width=0.5, dash="dot"), fillcolor="green", opacity=0.2,
            layer="below"
        )

    deps_vert, deps_orange, deps_rouge = [], [], []
    nb_vert, nb_orange, nb_rouge = 0, 0, 0
    for dep in departements:
        df_incid_dep = df_incid_departements[df_incid_departements["departmentName"]==dep]
        tests_dep_rolling = df_incid_dep["Test Positif"].rolling(window=7).mean().values
        evol_tests_dep = (tests_dep_rolling[-1-i] - tests_dep_rolling[-8-i]) / tests_dep_rolling[-8] * 100
        evol_tests_deps += [evol_tests_dep]

        hosp_dep_rolling = df_new_departements[df_new_departements["departmentName"]==dep]["Nv Hospitalise"].rolling(window=7).mean().values
        evol_hosp_dep = ( hosp_dep_rolling[-1-i] - hosp_dep_rolling[-8-i]) / hosp_dep_rolling[-8] * 100
        evol_hosp_deps += [evol_hosp_dep]

        if (evol_tests_dep < 0) & (evol_hosp_dep<0):
            color = "green"
            deps_vert += [df_incid_dep["Departement"].values[0]]
            nb_vert += 1

        elif (evol_tests_dep > 0) & (evol_hosp_dep > 0):
            color = "red"
            deps_rouge += [df_incid_dep["Departement"].values[0]]
            nb_rouge += 1

        else:
            color = "orange"
            deps_orange += [df_incid_dep["Departement"].values[0]]
            nb_orange += 1

        fig.add_trace(go.Scatter(
            x = [evol_tests_dep],
            y = [evol_hosp_dep],
            name = dep,
            text=["<b>"+df_incid_dep["Departement"].values[0]+"</b>"],
            textfont=dict(size=10),
            marker=dict(size=15,
                        color = color,
                        line=dict(width=0.3,
                            color='DarkSlateGrey')),
            line_width=8,
            opacity=0.8,
            fill='tozeroy',
            mode='markers+text',
            fillcolor="rgba(8, 115, 191, 0.3)",
            textfont_color="white",
            showlegend=False,
            textposition="middle center"
        ))
    
    def make_string_deps(deps_list):
        deps_list = sorted(deps_list)
        list_string = [""]
        
        for idx,dep in enumerate(deps_list):
            list_string[-1] += dep

            if (idx==len(deps_list)-1) or (len(list_string[-1])/150 >= 1):
                list_string += [""]
            else:
                list_string[-1] += ", "
                
        return_string=""    
        for idx,liste in enumerate(list_string):
            return_string += liste
            if idx < len(list_string)-1:
                return_string += "<br>"
                
        if len(return_string)==0:
            return_string = "aucun"
            
        return return_string
    
    #liste_deps_str = "{} en <b>vert</b> : {}<br><br>{} en <b>orange</b> : {}<br><br>{} en <b>rouge</b> : {}".format(nb_vert, make_string_deps(deps_vert), nb_orange, make_string_deps(deps_orange), nb_rouge, make_string_deps(deps_rouge))
    liste_deps_str_vert = "<span style='color: green;'>Vert ({})</span> : {}<br>".format(nb_vert, make_string_deps(deps_vert))
    liste_deps_str_orange = "<span style='color: orange;'>Orange ({})</span> : {}<br>".format(nb_orange, make_string_deps(deps_orange))
    liste_deps_str_rouge = "<span style='color: red;'>Rouge ({})</span> : {}<br>".format(nb_rouge, make_string_deps(deps_rouge))
    
    liste_deps_str = liste_deps_str_vert + liste_deps_str_orange + liste_deps_str_rouge
    
    Dates = str("("+str(max(df_incid_dep["Date"]))+")")
    
    fig['layout']['annotations'] += (dict(
            x = 100, y = 100, # annotation point
            xref='x1', yref='y1',
            text="Les cas augmentent.<br>Les admissions à l'hôpital augmentent.",
            xanchor="center",align='center',
            font=dict(
                color="black", size=13
                ),
            showarrow=False
        ),dict(
            x = -50, y = -50, # annotation point
            xref='x1', yref='y1',
            text="Les cas baissent.<br>Les admissions à l'hôpital baissent.",
            xanchor="center",align='center',
            font=dict(
                color="black", size=13
                ),
            showarrow=False
        ),dict(
            x = -50, y = 100, # annotation point
            xref='x1', yref='y1',
            text="Les cas baissent.<br>Les admissions à l'hôpital augmentent.",
            xanchor="center",align='center',
            font=dict(
                color="black", size=13
                ),
            showarrow=False
        ),dict(
            x = 100, y = -50, # annotation point
            xref='x1', yref='y1',
            text="Les cas augmentent.<br>Les admissions à l'hôpital baissent.",
            xanchor="center",align='center',
            font=dict(
                color="black", size=13
                ),
            showarrow=False
        ),dict(
                x=0.5,
                y=1.05,
                xref='paper',
                yref='paper',
                font=dict(size=14),
                text=Dates,
                showarrow = False
                        ),
            dict(
                x=-0.08,
                y=-0.3,
                xref='paper',
                yref='paper',
                font=dict(size=14),
                align="left",
                text=liste_deps_str, showarrow = False
          ),)

    fig.update_xaxes(title="Évolution hebdomadaire des cas positifs", range=[-100, 200], ticksuffix="%")
    fig.update_yaxes(title="Évolution hedbomadaire des admissions à l'hôpital", range=[-100, 200], ticksuffix="%")
    fig.update_layout(
         title={
                        'text': "Evolution des cas et des hospitalisations dans les départements",
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
        titlefont = dict(
                    size=20),
        margin=dict(
            l=110,
            b=200
        ),
        )
    fig.write_image("assets/deps0.png", scale=3, width=1200, height=900)

import base64
image_filename = 'assets/deps0.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
print("save image")

shapegraph = [
                dbc.CardHeader([
                    dbc.Button([
                        html.Div(
                            html.Div([
                                "Zoom",dbc.CardImg(
                                    src=["assets/zoom.png"], top=True,style={'width': '20px',"margin-left":"10px","filter": "invert(0.9)"})
                                ])
                            )],id="open-xl",style={"width":"100%"}),
                    dbc.Modal(
                    [
                        dbc.ModalHeader("Zoom"),
                        dbc.ModalBody(dbc.Card([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    height=800)])),
                        dbc.ModalFooter(
                            dbc.Button("Fermer", id="close-xl", className="ml-auto")
                        ),
                    ],
                    id="modal-xl",
                    size="xl",
                )],style={"text-align":"end"}),
                dbc.CardBody(
                    dbc.Card(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    height=447))
                )
              ]