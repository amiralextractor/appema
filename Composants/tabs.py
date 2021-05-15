import dash_bootstrap_components as dbc
import dash_html_components as html

Tab = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Courbes", tab_id="tab-1"),
                    dbc.Tab(label="Cartographie", tab_id="tab-2"),
                    dbc.Tab(label="Simulations", tab_id="tab-3"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.Div(id="card-content", className="card-text")),
    ]
)

from Composants.cartes import cards
from Composants.courbes import Courbes
from Composants.cartographie import page_Carto
from Composants.simulation import simulpage

page1 = html.Div([cards, Courbes])
page2 = html.Div(page_Carto)
page3 = html.Div(simulpage)