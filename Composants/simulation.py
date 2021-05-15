#Import some useful librairies
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from lmfit import Parameters
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px

# Compartments
# S(t): susceptible individuals; 
# E(t): exposed (incubating) population;
# A(t): asymptomatic infective people; 
# I (t): symptomatic infective individuals; 
# R(t): removed persons (i.e. completely and/or temporary recovered from COVID-19); 
# D(t): Dead people.


# Parameters
# α is the fraction of exposed population E progressing to class I , or proportion of symptomatic infections, with 0 < α < 1.
# β is the probability of COVID-19 transmission (i.e, the infection rate).
# δ is the ratio of the infective force in infectious asymptomatic people by the infective force in infectious (symptomatic) people
# γ1 is the recovery probability of infectious people.
# γ2 is the recovery probability of asymptomatic people.
# μ is the progression rate from the exposed class to infective class (i.e. infected symptomatic and asymptomatic people).
# θ is the fatality rate.
# η is the birth and death rate (assumed to be equal here).
# N is the population size of each country.

def ode_model_ema(z, t, beta, delta, eta, mu, gamma1, theta, alpha, gamma2):
    S, E, A, I, R, D = z
    N = S + E + A + I + R + D
    dSdt = N*eta-beta*S*(I+delta*A)/(N-D)-eta*S
    dEdt = beta*S*(I+delta*A)/N-mu*E-eta*E
    dAdt =(1-alpha)*mu*E-gamma2*A-eta*A
    dIdt = alpha*mu*E-(gamma1+theta)*I-eta*I
    dRdt = gamma1*I+gamma2*A-eta*R
    dDdt = theta*I
    return [dSdt, dEdt, dAdt, dIdt, dRdt, dDdt]


def ode_solver_ema(t, initial_conditions, params):
    initE, initA, initI, initR, initN, initD = initial_conditions
    beta, delta, eta, mu, gamma1, theta, alpha, gamma2 = params['beta'].value, params['delta'].value, params['eta'].value, params['mu'].value, params['gamma1'].value, params['theta'].value, params['alpha'].value, params['gamma2'].value
    initS = initN - (initE + initA + initI + initR + initD)
    res = odeint(ode_model_ema, [initS, initE, initA, initI, initR, initD], t, args=(beta, delta, eta, mu, gamma1, theta, alpha, gamma2))
    return res

#Parameters initialization
initN = 10000

#beta = 0.9950 # Probabilité S => E
#delta = 49.8 # rapport entre les forces infectieuses chez les asymptomatiques et les symptomatiques
#eta = 1 # the birth and death rate (assumed to be equal here)
#mu = 0.0005 # progression de E => I
#gamma1 = 0.9997 # Probabilité I => R
#theta = 0.0719 # Probabilité I => D
#alpha = 0.037 # Proportion des infections symptomatiques 0 < alpha < 1
#gamma2 = 0.0009 # Probabilité A => R

#Simulation
def main(initE, initA, initI, initR, initD, initN, beta, delta, eta, mu, gamma1, theta, alpha, gamma2, days):
    params = Parameters()
    params.add('beta', value=beta, min=0, max=1)
    params.add('delta', value=delta, min=0, max=50)
    params.add('eta', value=eta, min=0, max=1)
    params.add('mu', value=mu, min=0, max=10)
    params.add('gamma1', value=gamma1, min=0, max=1)
    params.add('theta', value=theta, min=0, max=1)
    params.add('alpha', value=alpha, min=0, max=1)
    params.add('gamma2', value=gamma2, min=0, max=1)
    initial_conditions = [initE, initA, initI, initR, initN, initD]
    params['beta'].value, params['delta'].value,params['eta'].value, params['mu'].value, params['gamma1'].value, params['theta'].value, params['alpha'].value, params['gamma2'].value = [beta, delta, eta, mu, gamma1, theta, alpha, gamma2]
    tspan = np.arange(0, days, 1)
    #print(tspan)
    sol = ode_solver_ema(tspan, initial_conditions, params)
    S, E, A, I, R, D = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3], sol[:, 4], sol[:, 5]
    
    # Create traces
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=tspan, y=S, mode='lines+markers', name='Susceptible'))
    fig.add_trace(go.Scatter(x=tspan, y=E, mode='lines+markers', name='Exposed'))
    fig.add_trace(go.Scatter(x=tspan, y=A, mode='lines+markers', name='Asymptomatic'))
    fig.add_trace(go.Scatter(x=tspan, y=I, mode='lines+markers', name='Infected'))
    fig.add_trace(go.Scatter(x=tspan, y=R, mode='lines+markers',name='Recovered'))
    fig.add_trace(go.Scatter(x=tspan, y=D, mode='lines+markers',name='Death'))
    
    # Edit the layout
    fig.update_layout(title='Simulation modèle SEAIRD',
                       xaxis_title='Jours',
                       yaxis_title='Nombres',
                      width=900, height=600
                     )
    #fig.write_image("seird_simulation.png")
    return fig
'''
def error(params, initial_conditions, tspan, data):
    sol = ode_solver_ema(tspan, initial_conditions, params)
    j=(sol[:,[2,5]] - data)
    return j.ravel()

initial_conditions = [initE, initA, initI, initR, initN, initD]

params = Parameters()
params.add('beta', value=beta, min=0, max=10)
params.add('delta', value=delta, min=0, max=10)
params.add('eta', value=eta, min=0, max=10)
params.add('mu', value=mu, min=0, max=10)
params.add('gamma1', value=gamma1, min=0, max=10)
params.add('theta', value=theta, min=0, max=10)
params.add('alpha', value=alpha, min=0, max=10)
params.add('gamma2', value=gamma2, min=0, max=10)
params['beta'].value = beta
params['delta'].value = delta
params['eta'].value = eta
params['mu'].value = mu
params['gamma1'].value = gamma1
params['theta'].value = theta
params['alpha'].value = alpha
params['gamma2'].value = gamma2

tspan = np.arange(0, days, 1)
data = df.loc[0:(days-1), ['Total Cas', 'Total Deces']].values

# fit model and find predicted values
result = minimize(error, params, args=(initial_conditions, tspan, data), method='leastsq', full_output = 1)

# display fitted statistics
report_fit(result)
print(result.params)'''

sl_beta=html.Div([
    html.Div(id='output1',style={"margin-left":"25px"}),
    dcc.Slider(
        id='beta',
        min=0,
        max=1,
        step=0.001,
        value=0.991
    )
])
days=html.Div([
    html.Div(id='output2',style={"margin-left":"25px"}),
    dcc.Slider(
        id='days_sim',
        min=1,
        max=150,
        step=1,
        value=37
    )
])

sl_delta=html.Div([
    html.Div(id='output3',style={"margin-left":"25px"}),
    dcc.Slider(
        id='delta',
        min=0,
        max=60,
        step=0.1,
        value=10.3
    )
])
sl_mu=html.Div([
    html.Div(id='output4',style={"margin-left":"25px"}),
    dcc.Slider(
        id='mu',
        min=0,
        max=1,
        step=0.0001,
        value=0.3903
    )
])
sl_gamma1=html.Div([
    html.Div(id='output5',style={"margin-left":"25px"}),
    dcc.Slider(
        id='gamma1',
        min=0,
        max=1,
        step=0.001,
        value=0.96
    )
])
sl_theta=html.Div([
    html.Div(id='output6',style={"margin-left":"25px"}),
    dcc.Slider(
        id='theta',
        min=0,
        max=1,
        step=0.01,
        value=0.11
    )
])
sl_alpha=html.Div([
    html.Div(id='output7',style={"margin-left":"25px"}),
    dcc.Slider(
        id='alpha',
        min=0,
        max=1,
        step=0.01,
        value=0.02
    )
])
sl_gamma2=html.Div([
    html.Div(id='output8',style={"margin-left":"25px"}),
    dcc.Slider(
        id='gamma2',
        min=0,
        max=1,
        step=0.01,
        value=0.3
    )
])

sl_expo=html.Div([
    html.Div("Nombre des exposés",style={"font-size":"12px"}),
    dcc.Input(id="init_expo", type="number",value=100),
])
sl_inf=html.Div([
    html.Div("Nombre des infectés",style={"font-size":"12px"}),
    dcc.Input(id="init_inf", type="number",value=10),
])
sl_asymp=html.Div([
    html.Div("Nombre des asymptomatiques",style={"font-size":"12px"}),
    dcc.Input(id="init_asymp", type="number",value=1),
])
sl_recov=html.Div([
    html.Div("Nombre des guéris",style={"font-size":"12px"}),
    dcc.Input(id="init_recov", type="number",value=1),
])
sl_Deced=html.Div([
    html.Div("Nombre des décédés",style={"font-size":"12px"}),
    dcc.Input(id="init_dece", type="number",value=1),
])

simulpage=html.Div([
    dbc.Row([
            dbc.Col(md=1),
            dbc.Col(sl_expo,md=2),
            dbc.Col(sl_inf,md=2),
            dbc.Col(sl_asymp,md=2),
            dbc.Col(sl_recov,md=2),
            dbc.Col(sl_Deced,md=2),
            dbc.Col(md=1)
        ],style={"margin-top":"20px"}),
    html.Br(),
    dbc.Row([
        dbc.Col([days,sl_alpha,sl_beta,sl_delta],md=6),
        dbc.Col([sl_gamma1,sl_gamma2,sl_mu,sl_theta],md=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(md=2),
        dbc.Col(dcc.Graph(id="graph-simulation",figure=px.scatter()),md=8),
        dbc.Col(md=2),
    ]),
])