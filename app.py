import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import plotly.express as px

bootstrap_theme=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.9.0/css/all.css']
app = dash.Dash(__name__,external_stylesheets=bootstrap_theme)
server = app.server
app.config.suppress_callback_exceptions = True

from Composants.tabs import Tab

import base64
image_filename = 'assets/logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


banner = html.Div([
    dbc.Row([
        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={'height':'100px', "width":"100px", 'float':'left'}),md=3),
         dbc.Col(html.Div(children=[
                        html.H2("Suivi de l’épidémie COVID-19 en France"),
                        html.H4("Dashboard")
                        ], style={'text-align': 'center'}),style={"align-self": "center"}, md=6), 
            dbc.Col(html.Div(children=[
                        html.Img(
                        id="logo_ilis",
                        src="https://media-exp1.licdn.com/dms/image/C560BAQHKz72cs-Jp_Q/company-logo_200_200/0/1545129729772?e=2159024400&v=beta&t=dUIfbOAKuHiRtz1-6PMFI2JjH-vgidboOxsSkqsNXOo",
                        style={'height':'100px', 'float':'right',
                               "border-radius": "20px"}
                        ),
                        ]), md=3),
        
        ],style={"padding":"20px"})
    ],style={"background-color":"beige"})

pieds = html.Div([
    dbc.Row([
        dbc.Col(html.Div("Auteurs : Enrico Perspicace & Marouane Aboulehadi & Amir Hachicha ©")),
        dbc.Col(html.Div("Sources : covidtracker.fr & Santé publique France"),style={'text-align':'right'})
    ])],style={"padding":"20px"})

app.layout = html.Div([
    banner,
    Tab,
    pieds
])

####### Callback cartographie #######
from Composants.cartographie import fig, depa, depa2, depa3, depa4, depa5, depa6, df_map, df_map1, df_map2, df_map3, df_map4, df_map5, df_map6, cas, cas1, cas2, cas3, cas4, cas5, cas6
import dash_core_components as dcc
@app.callback(
        Output('titre-carte','children'),
        [
         Input('drop-incidence', 'value')])
def update_titrecarte(incidence):
    if incidence == "Pourcentage Couverture Dose 1":
        titre=str("Pourcentage de la couverture vaccinale pour la première dose **("+str(max(df_map["Date"]))+")")
    elif incidence == "Pourcentage Couverture Dose 2":
        titre=str("Pourcentage de la couverture vaccinale pour la deuxième dose **("+str(max(df_map["Date"]))+")")
    else:
        titre = str(incidence+" hebdomadaire pour 100 000 habitants** ("+
                str(max(df_map["Date"]))+")")
    return dcc.Markdown(str("#### **"+titre+""))

@app.callback(
        Output('datatable-paging', 'data'),
        [Input('datatable-paging', "page_current"),
        Input('datatable-paging', "page_size"),
         Input('drop-incidence', 'value')])
def update_tableau(page_current,page_size,incidence):
    if incidence == "Pourcentage Couverture Dose 1":
       dff = df_map[["Departement","departmentName","Population","Couverture Dose 1"]] 
    elif incidence == "Pourcentage Couverture Dose 2":
        dff = df_map[["Departement","departmentName","Population","Couverture complete"]] 
    elif incidence == "Taux d'incidence Cas":
        dff = cas[["Departement","departmentName","Population","Taux d'incidence Cas"]]
    elif incidence == "Taux d'incidence Hospitalisation":
        dff = df_map[["Departement","departmentName","Population","Incidence Hospitalise"]] 
    elif incidence == "Taux d'incidence Reanimation":
        dff = df_map[["Departement","departmentName","Population","Incidence Reanime"]]
    elif incidence == "Taux d'incidence Décès":
        dff = df_map[["Departement","departmentName","Population","Incidence Decede"]]
    elif incidence == "Taux d'incidence Guérison":
        dff = df_map[["Departement","departmentName","Population","Incidence Gueris"]]
    
    dff.columns = ["Departement","Nom Departement","Population","Valeur"]
    dff=dff.sort_values(["Valeur"], ascending=[False])
    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


@app.callback(
        Output('graph-carte0','figure'),
        [
         Input('drop-incidence', 'value')])
def update_carte0(incidence):
    if incidence:
        if incidence == "Taux d'incidence Hospitalisation":
            types = "Incidence Hospitalise"
            fig1 = px.choropleth(geojson=depa, 
                                locations=df_map1['Departement'],
                                color=df_map1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="reds",
                                range_color=(min(df_map[types]), max(df_map[types])),
                                hover_data={"Departement":df_map1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
        elif incidence == "Taux d'incidence Cas":
            types = "Taux d'incidence Cas"
            fig1 = px.choropleth(geojson=depa, 
                                locations=cas1['Departement'], 
                                color=cas1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="reds",
                                range_color=(min(cas[types]), max(cas[types])),
                                hover_data={"Departement":cas1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
        elif incidence == "Taux d'incidence Reanimation":
            types = "Incidence Reanime"
            fig1 = px.choropleth(geojson=depa, 
                                locations=df_map1['Departement'], 
                                color=df_map1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="reds",
                                range_color=(min(df_map[types]), max(df_map[types])),
                                hover_data={"Departement":df_map1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
        elif incidence == "Taux d'incidence Décès":
            types = "Incidence Decede"
            fig1 = px.choropleth(geojson=depa, 
                                locations=df_map1['Departement'], 
                                color=df_map1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="reds",
                                range_color=(min(df_map[types]), max(df_map[types])),
                                hover_data={"Departement":df_map1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
        elif incidence == "Taux d'incidence Guérison":
            types = "Incidence Gueris"
            fig1 = px.choropleth(geojson=depa, 
                                locations=df_map1['Departement'], 
                                color=df_map1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="greens",
                                range_color=(min(df_map[types]), max(df_map[types])),
                                hover_data={"Departement":df_map1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
        elif incidence == "Pourcentage Couverture Dose 1":
            types = 'Couverture Dose 1'
            fig1 = px.choropleth(geojson=depa, 
                                locations=df_map1['Departement'], 
                                color=df_map1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="greens",
                                range_color=(min(df_map[types]), max(df_map[types])),
                                hover_data={"Departement":df_map1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
        elif incidence == "Pourcentage Couverture Dose 2":
            types = 'Couverture complete'
            fig1 = px.choropleth(geojson=depa, 
                                locations=df_map1['Departement'], 
                                color=df_map1[types],
                                featureidkey="properties.code",
                                color_continuous_scale="greens",
                                range_color=(min(df_map[types]), max(df_map[types])),
                                hover_data={"Departement":df_map1['departmentName']},
                                labels={"color": "Valeur","locations":"N° Dep"},
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            fig1.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            )
                 )
            return fig1
    else:
        return fig
    
@app.callback(
        Output('graph-carte1','figure'),
        [
         Input('drop-incidence', 'value')])
def update_carte1(incidence):
    if incidence:
        if incidence == "Taux d'incidence Hospitalisation":
            types = "Incidence Hospitalise"
            fig2 = px.choropleth(geojson=depa2, 
                            locations=df_map2['Departement'], 
                            color=df_map2[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
        elif incidence == "Taux d'incidence Cas":
            types = "Taux d'incidence Cas"
            fig2 = px.choropleth(geojson=depa2, 
                            locations=cas2['Departement'], 
                            color=cas2[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(cas[types]), max(cas[types])),
                            hover_data={"Dep":cas2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
        elif incidence == "Taux d'incidence Reanimation":
            types = "Incidence Reanime"
            fig2 = px.choropleth(geojson=depa2, 
                            locations=df_map2['Departement'], 
                            color=df_map2[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
        elif incidence == "Taux d'incidence Décès":
            types = "Incidence Decede"
            fig2 = px.choropleth(geojson=depa2, 
                            locations=df_map2['Departement'], 
                            color=df_map2[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
        elif incidence == "Taux d'incidence Guérison":
            types = "Incidence Gueris"
            fig2 = px.choropleth(geojson=depa2, 
                            locations=df_map2['Departement'], 
                            color=df_map2[types],
                            featureidkey="properties.code",
                            color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
        elif incidence == "Pourcentage Couverture Dose 1":
            types = 'Couverture Dose 1'
            fig2 = px.choropleth(geojson=depa2, 
                            locations=df_map2['Departement'], 
                            color=df_map2[types],
                            featureidkey="properties.code",
                            color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
        elif incidence == "Pourcentage Couverture Dose 2":
            types = 'Couverture complete'
            fig2 = px.choropleth(geojson=depa2, 
                            locations=df_map2['Departement'], 
                            color=df_map2[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map2['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig2.update_geos(fitbounds="locations", visible=False)
            fig2.update_layout(coloraxis_showscale=False)
            fig2.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig2
    else:
        return fig    

@app.callback(
        Output('graph-carte2','figure'),
        [
         Input('drop-incidence', 'value')])
def update_carte2(incidence):
    if incidence:
        if incidence == "Taux d'incidence Hospitalisation":
            types = "Incidence Hospitalise"
            fig3 = px.choropleth(geojson=depa3, 
                            locations=df_map3['Departement'], 
                            color=df_map3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
        elif incidence == "Taux d'incidence Cas":
            types = "Taux d'incidence Cas"
            fig3 = px.choropleth(geojson=depa3, 
                            locations=cas3['Departement'], 
                            color=cas3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(cas[types]), max(cas[types])),
                            hover_data={"Dep":cas3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
        elif incidence == "Taux d'incidence Reanimation":
            types = "Incidence Reanime"
            fig3 = px.choropleth(geojson=depa3, 
                            locations=df_map3['Departement'], 
                            color=df_map3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
        elif incidence == "Taux d'incidence Décès":
            types = "Incidence Decede"
            fig3 = px.choropleth(geojson=depa3, 
                            locations=df_map3['Departement'], 
                            color=df_map3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
        elif incidence == "Taux d'incidence Guérison":
            types = "Incidence Gueris"
            fig3 = px.choropleth(geojson=depa3, 
                            locations=df_map3['Departement'], 
                            color=df_map3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
        elif incidence == "Pourcentage Couverture Dose 1":
            types = 'Couverture Dose 1'
            fig3 = px.choropleth(geojson=depa3, 
                            locations=df_map3['Departement'], 
                            color=df_map3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
        elif incidence == "Pourcentage Couverture Dose 2":
            types = 'Couverture complete'
            fig3 = px.choropleth(geojson=depa3, 
                            locations=df_map3['Departement'], 
                            color=df_map3[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map3['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
            #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig3.update_geos(fitbounds="locations", visible=False)
            fig3.update_layout(coloraxis_showscale=False)
            fig3.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig3
    else:
        return fig
    
@app.callback(
        Output('graph-carte3','figure'),
        [
         Input('drop-incidence', 'value')])
def update_carte3(incidence):
    if incidence:
        if incidence == "Taux d'incidence Hospitalisation":
            types = "Incidence Hospitalise"
            fig4 = px.choropleth(geojson=depa4, 
                            locations=df_map4['Departement'], 
                            color=df_map4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
        elif incidence == "Taux d'incidence Cas":
            types = "Taux d'incidence Cas"
            fig4 = px.choropleth(geojson=depa4, 
                            locations=cas4['Departement'], 
                            color=cas4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(cas[types]), max(cas[types])),
                            hover_data={"Dep":cas4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
        elif incidence == "Taux d'incidence Reanimation":
            types = "Incidence Reanime"
            fig4 = px.choropleth(geojson=depa4, 
                            locations=df_map4['Departement'], 
                            color=df_map4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
        elif incidence == "Taux d'incidence Décès":
            types = "Incidence Decede"
            fig4 = px.choropleth(geojson=depa4, 
                            locations=df_map4['Departement'], 
                            color=df_map4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
        elif incidence == "Taux d'incidence Guérison":
            types = "Incidence Gueris"
            fig4 = px.choropleth(geojson=depa4, 
                            locations=df_map4['Departement'], 
                            color=df_map4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
        elif incidence == "Pourcentage Couverture Dose 1":
            types = 'Couverture Dose 1'
            fig4 = px.choropleth(geojson=depa4, 
                            locations=df_map4['Departement'], 
                            color=df_map4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
        elif incidence == "Pourcentage Couverture Dose 2":
            types = 'Couverture complete'
            fig4 = px.choropleth(geojson=depa4, 
                            locations=df_map4['Departement'], 
                            color=df_map4[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map4['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig4.update_geos(fitbounds="locations", visible=False)
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig4
    else:
        return fig
    
@app.callback(
        Output('graph-carte4','figure'),
        [
         Input('drop-incidence', 'value')])
def update_carte4(incidence):
    if incidence:
        if incidence == "Taux d'incidence Hospitalisation":
            types = "Incidence Hospitalise"
            fig5 = px.choropleth(geojson=depa5, 
                            locations=df_map5['Departement'], 
                            color=df_map5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
        elif incidence == "Taux d'incidence Cas":
            types = "Taux d'incidence Cas"
            fig5 = px.choropleth(geojson=depa5, 
                            locations=cas5['Departement'], 
                            color=cas5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(cas[types]), max(cas[types])),
                            hover_data={"Dep":cas5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
        elif incidence == "Taux d'incidence Reanimation":
            types = "Incidence Reanime"
            fig5 = px.choropleth(geojson=depa5, 
                            locations=df_map5['Departement'], 
                            color=df_map5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
        elif incidence == "Taux d'incidence Décès":
            types = "Incidence Decede"
            fig5 = px.choropleth(geojson=depa5, 
                            locations=df_map5['Departement'], 
                            color=df_map5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
        elif incidence == "Taux d'incidence Guérison":
            types = "Incidence Gueris"
            fig5 = px.choropleth(geojson=depa5, 
                            locations=df_map5['Departement'], 
                            color=df_map5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
        elif incidence == "Pourcentage Couverture Dose 1":
            types = 'Couverture Dose 1'
            fig5 = px.choropleth(geojson=depa5, 
                            locations=df_map5['Departement'], 
                            color=df_map5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
        elif incidence == "Pourcentage Couverture Dose 2":
            types = 'Couverture complete'
            fig5 = px.choropleth(geojson=depa5, 
                            locations=df_map5['Departement'], 
                            color=df_map5[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map5['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig5.update_geos(fitbounds="locations", visible=False)
            fig5.update_layout(coloraxis_showscale=False)
            fig5.update_layout(
                hovermode='closest',
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig5
    else:
        return fig
    
@app.callback(
        Output('graph-carte5','figure'),
        [
         Input('drop-incidence', 'value')])
def update_carte5(incidence):
    if incidence:
        if incidence == "Taux d'incidence Hospitalisation":
            types = "Incidence Hospitalise"
            fig6 = px.choropleth(geojson=depa6, 
                            locations=df_map6['Departement'], 
                            color=df_map6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
        elif incidence == "Taux d'incidence Cas":
            types = "Taux d'incidence Cas"
            fig6 = px.choropleth(geojson=depa6, 
                            locations=cas6['Departement'], 
                            color=cas6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(cas[types]), max(cas[types])),
                            hover_data={"Dep":cas6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
        elif incidence == "Taux d'incidence Reanimation":
            types = "Incidence Reanime"
            fig6 = px.choropleth(geojson=depa6, 
                            locations=df_map6['Departement'], 
                            color=df_map6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
        elif incidence == "Taux d'incidence Décès":
            types = "Incidence Decede"
            fig6 = px.choropleth(geojson=depa6, 
                            locations=df_map6['Departement'], 
                            color=df_map6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="reds",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
        elif incidence == "Taux d'incidence Guérison":
            types = "Incidence Gueris"
            fig6 = px.choropleth(geojson=depa6, 
                            locations=df_map6['Departement'], 
                            color=df_map6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
        elif incidence == "Pourcentage Couverture Dose 1":
            types = 'Couverture Dose 1'
            fig6 = px.choropleth(geojson=depa6, 
                            locations=df_map6['Departement'], 
                            color=df_map6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
        elif incidence == "Pourcentage Couverture Dose 2":
            types = 'Couverture complete'
            fig6 = px.choropleth(geojson=depa6, 
                            locations=df_map6['Departement'], 
                            color=df_map6[types],
                            featureidkey="properties.code",
                                color_continuous_scale="greens",
                            #color_continuous_scale = colorscale,
                            range_color=(min(df_map[types]), max(df_map[types])),
                            hover_data={"Dep":df_map6['departmentName']},
                            labels={"color": "Valeur","locations":"N° Dep"},
                                  )
                    #date_title = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            fig6.update_geos(fitbounds="locations", visible=False)
            fig6.update_layout(coloraxis_showscale=False)
            fig6.update_layout(
                autosize=True,
                 margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                autoexpand=True
                            ),
            )
            return fig6
    else:
        return fig


####### Callback courbes #######
from data.loaddata import data
import plotly.graph_objects as go
import numpy as np
@app.callback(
        Output('graph1','figure'),
        [Input('radio-type-graph1', 'value'),
         ])
def update_dist1(typegraph):
    val=data[5]
    val=val.sort_values(["Date"], ascending=[False])
    val=val.reset_index(drop=True)
    nouveau=[]
    for i in range(0,len(val)):
        if i == (len(val)-1):
            nouveau.append(val["Total Cas"][i])
        else:
            types = "Total Cas"
            r=i+1
            calc = val[types][i]-val[types][r]
            while calc < 0:
                if r == (len(val)-1):
                    calc = val[types][r]
                else:
                    calc = val[types][i]-val[types][r]
                    r=r+1
                
            nouveau.append(calc)
    val["Nouveau"]=nouveau
    val=val.sort_values(["Date"], ascending=[True])
    val["meanNouv"] = val["Nouveau"].rolling(window=7).mean().values
    if typegraph == 1:
        #lin
        fig = px.bar(val,x="Date",y="Nouveau",labels={'Nouveau':'Nouveaux cas'})
        fig.add_trace(go.Scatter(x=val["Date"], y=val["meanNouv"],mode='lines',name='Moyenne',line = dict(color='royalblue')))
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Nouveaux cas positifs Covid')
    else:
        val["meanNouv"]=np.log10(val["meanNouv"])
        fig = px.line(val,x="Date",y="meanNouv",labels={'meanNouv':'Log moyenne nouveaux cas'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Log moyenne nouveaux cas positifs Covid')

    fig.update_layout(
    autosize=True,
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
    yaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
     margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=20,
                    autoexpand=True
                ),
     )
    return fig

@app.callback(
        Output('graph2','figure'),
        [Input('radio-type-graph2', 'value'),
         Input('check-sexe', 'value'),
         Input('drop-departement', 'value')])
def update_dist2(typegraph,sexe,dep):
    df = data[0]
    types = "Hospitalise"
    if(len(sexe)==1):
        df = df[df['Sexe']==sexe[0]]
    else:
        df = df[df['Sexe']==0]
    if dep:
        df = df[df['Departement']==dep]
    val=df.groupby("Date", as_index=False).agg({types: "sum"})
    if typegraph == 1:
        #lin
        fig = px.line(val,x="Date",y=types,labels={'Hospitalise':'Personnes hospitalisées'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Personnes hospitalisées')
    else:
        val[types]=np.log10(val[types])
        fig = px.line(val,x="Date",y=types,labels={'Hospitalise':'Log personnes hospitalisées'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Log personnes hospitalisées')
    fig.update_layout(
    autosize=True,
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
    yaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
     margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=20,
                    autoexpand=True
                ),
     )
    return fig

@app.callback(
        Output('graph3','figure'),
        [Input('radio-type-graph3', 'value'),
         Input('check-sexe', 'value'),
         Input('drop-departement', 'value')])
def update_dist3(typegraph,sexe,dep):
    df = data[0]
    types = "Reanime"
    if(len(sexe)==1):
        df = df[df['Sexe']==sexe[0]]
    else:
        df = df[df['Sexe']==0]
    if dep:
        df = df[df['Departement']==dep]
    val=df.groupby("Date", as_index=False).agg({types: "sum"})
    if typegraph == 1:
        #lin
        fig = px.line(val,x="Date",y=types,labels={'Reanime':'Personnes en réanimation'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Personnes en réanimation')
    else:
        val[types]=np.log10(val[types])
        fig = px.line(val,x="Date",y=types,labels={'Reanime':'Log personnes en réanimation'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Log personnes en réanimation')
    fig.update_layout(
    autosize=True,
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
    yaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
     margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=20,
                    autoexpand=True
                ),
     )
    return fig

@app.callback(
        Output('graph4','figure'),
        [Input('radio-type-graph4', 'value'),
         Input('check-sexe', 'value'),
         Input('drop-departement', 'value')])
def update_dist4(typegraph,sexe,dep):
    df = data[0]
    types = "Decede"
    if(len(sexe)==1):
        df = df[df['Sexe']==sexe[0]]
    else:
        df = df[df['Sexe']==0]
    if dep:
        df = df[df['Departement']==dep]
    val=df.groupby("Date", as_index=False).agg({types: "sum"})
    
    val=val.sort_values(["Date"], ascending=[False])
    val=val.reset_index(drop=True)
    nouveau=[]
    for i in range(0,len(val)):
        if i == (len(val)-1):
            nouveau.append(val[types][i])
        else:
            r=i+1
            calc = val[types][i]-val[types][r]
            while calc < 0:
                if r == (len(val)-1):
                    calc = val[types][r]
                else:
                    calc = val[types][i]-val[types][r]
                    r=r+1
            nouveau.append(calc)
    val["Nouveau"]=nouveau
    val=val.sort_values(["Date"], ascending=[True])
    val["meanNouv"] = val["Nouveau"].rolling(window=7).mean().values
    if typegraph == 1:
        #lin
        fig = px.bar(val,x="Date",y="Nouveau",labels={'Nouveau':'Nouveaux Décès'})
        fig.add_trace(go.Scatter(x=val["Date"], y=val["meanNouv"],mode='lines',name='Moyenne',line = dict(color='royalblue')))
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Nouveaux décès Covid')
    else:
        val["meanNouv"]=np.log10(val["meanNouv"])
        fig = px.line(val,x="Date",y="meanNouv",labels={'meanNouv':'Log moyenne nouveaux décès'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Log moyenne nouveaux décès')
    fig.update_layout(
    autosize=True,
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
    yaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
     margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=20,
                    autoexpand=True
                ),
     )
    return fig

@app.callback(
        Output('graph5','figure'),
        [Input('radio-type-graph5', 'value'),
         Input('check-sexe', 'value'),
         Input('drop-departement', 'value')])
def update_dist5(typegraph,sexe,dep):
    df = data[0]
    types = "Gueris"
    if(len(sexe)==1):
        df = df[df['Sexe']==sexe[0]]
    else:
        df = df[df['Sexe']==0]
    if dep:
        df = df[df['Departement']==dep]
    val=df.groupby("Date", as_index=False).agg({types: "sum"})
    
    val=val.sort_values(["Date"], ascending=[False])
    val=val.reset_index(drop=True)
    nouveau=[]
    for i in range(0,len(val)):
        if i == (len(val)-1):
            nouveau.append(val[types][i])
        else:
            r=i+1
            calc = val[types][i]-val[types][r]
            while calc < 0:
                if r == (len(val)-1):
                    calc = val[types][r]
                else:
                    calc = val[types][i]-val[types][r]
                    r=r+1
            nouveau.append(calc)
    val["Nouveau"]=nouveau
    val=val.sort_values(["Date"], ascending=[True])
    val["meanNouv"] = val["Nouveau"].rolling(window=7).mean().values
    if typegraph == 1:
        #lin
        fig = px.bar(val,x="Date",y="Nouveau",labels={'Nouveau':'Nouveaux gueris'})
        fig.add_trace(go.Scatter(x=val["Date"], y=val["meanNouv"],mode='lines',name='Moyenne',line = dict(color='royalblue')))
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Nouveaux gueris Covid')
    else:
        val["meanNouv"]=np.log10(val["meanNouv"])
        fig = px.line(val,x="Date",y="meanNouv",labels={'meanNouv':'Log moyenne nouveaux gueris'})
        fig.update_layout(showlegend=False,
                   xaxis_title='',
                   yaxis_title='Log moyenne nouveaux gueris')
    fig.update_layout(
    autosize=True,
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
    yaxis=dict(
        showline=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
     margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=20,
                    autoexpand=True
                ),
     )
    return fig

####### Callback shape #######
@app.callback(
    Output("modal-xl", "is_open"),
    [Input("open-xl", "n_clicks"), Input("close-xl", "n_clicks")],
    [State("modal-xl", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

####### Callback tabs #######
from Composants.tabs import page1, page2, page3
@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "tab-1":
        return page1
    elif active_tab == "tab-2":
        return page2
    else:
        return page3

####### Callback simulation #######
from Composants.simulation import initN, main

@app.callback(
    Output('output1', 'children'),
    [Input('beta', 'value')])
def update_output1(value):
    return 'Beta: "{}"'.format(value)
@app.callback(
    Output('output2', 'children'),
    [Input('days_sim', 'value')])
def update_output2(value):
    return 'Jours: "{}"'.format(value)
@app.callback(
    Output('output3', 'children'),
    [Input('delta', 'value')])
def update_output3(value):
    return 'Delta: "{}"'.format(value)
@app.callback(
    Output('output4', 'children'),
    [Input('mu', 'value')])
def update_output4(value):
    return 'Mu: "{}"'.format(value)
@app.callback(
    Output('output5', 'children'),
    [Input('gamma1', 'value')])
def update_output5(value):
    return 'Gamma 1: "{}"'.format(value)
@app.callback(
    Output('output6', 'children'),
    [Input('theta', 'value')])
def update_output6(value):
    return 'Theta: "{}"'.format(value)
@app.callback(
    Output('output7', 'children'),
    [Input('alpha', 'value')])
def update_output7(value):
    return 'Alpha: "{}"'.format(value)
@app.callback(
    Output('output8', 'children'),
    [Input('gamma2', 'value')])
def update_output8(value):
    return 'Gamma 2: "{}"'.format(value)

@app.callback(
        Output('graph-simulation','figure'),
        [Input('beta', 'value'),
         Input('delta', 'value'),
         Input('days_sim', 'value'),
         Input('mu', 'value'),
         Input('gamma1', 'value'),
         Input('theta', 'value'),
         Input('alpha', 'value'),
         Input('gamma2', 'value'),
         Input('init_expo', 'value'),
         Input('init_asymp', 'value'),
         Input('init_inf', 'value'),
         Input('init_recov', 'value'),
         Input('init_dece', 'value'),
         ])
def update_graph(beta, delta, days, mu, gamma1, theta, alpha, gamma2,initE, initA, initI, initR, initD):
    eta=1
    if initE is None:
        initE=0
    if initA is None:
        initA=0
    if initI is None:
        initI=0
    if initR is None:
        initR=0
    if initD is None:
        initD=0
    return main(initE, initA, initI, initR, initD, initN, beta, delta, eta, mu, gamma1, theta, alpha, gamma2, days)

app.title = 'EMA Covid Dashboard'
if __name__ == '__main__':     
   app.run_server(debug=True, use_reloader=False)