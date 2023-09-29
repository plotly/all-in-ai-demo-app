import json
import pickle

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import openai
from dash import dcc, html

from constants import redis_instance

dash.register_page(__name__)


def layout(layout=None):
    layout = redis_instance.get(layout)
    layout = pickle.loads(layout)

    figures = [i["props"]["children"][0]["props"]["figure"] for i in layout[1:]]

    question = (
        "The following is a Plotly Dash layout with several charts. Summarize "
        "the charts for me and provide some maximums, mimumuns, trends, "
        "notable outliers, etc. Describe the data and content as the user doesn't know it's a layout."
        "The data may be truncated to comply with a max character count. "
        f"There should be {len(figures)} charts to follow:\n\n\n"
    )

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
