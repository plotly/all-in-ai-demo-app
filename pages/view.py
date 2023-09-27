import pickle
import json
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_mantine_components as dmc

import openai

from constants import redis_instance

dash.register_page(__name__)


def layout(layout=None):
    layout = redis_instance.get(layout)
    layout = pickle.loads(layout)

    question = (
        "The following is a Plotly Dash layout with several charts. Summarize "
        "the charts for me and provide some maximums, mimumuns, trends, "
        "notable outliers, etc. Describe the data and content as the user doesn't know it's a layout.\n\n\n"
    )

    figures = [i["props"]["children"][0]["props"]["figure"] for i in layout[1:]]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question + json.dumps(figures)[0:3900]}],
    )

    response = dcc.Markdown(completion.choices[0].message.content)

    return dmc.LoadingOverlay(
        [
            dbc.Button(
                children="Home",
                href="/",
                style={"background-color": "#238BE6", "margin": "10px"},
            ),
            html.Div([response, html.Div(layout[1:])], style={"padding": "40px"}),
        ]
    )
