import random

import dash_chart_editor as dce
import dash_mantine_components as dmc
import openai
import pandas as pd
from dash import Input, Output, State, callback, dcc, html, no_update, register_page

import utils

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")


register_page(__name__, path="/")

layout = html.Div(
    [
        dmc.Paper(
            [
                html.Div(
                    [
                        dce.DashChartEditor(
                            id="chart-editor",
                            dataSources=df.to_dict("list"),
                        ),
                        dmc.Affix(
                            dmc.Button("Save this chart", id="add-to-layout"),
                            position={"bottom": 20, "left": 20},
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.P("Ask about the dataset...", className="lead"),
                        dmc.Textarea(
                            placeholder=random.choice(
                                [
                                    '"Are there any outliers in this dataset?"',
                                    '"What trends do you see in this dataset?"',
                                    '"Anything stand out about this dataset?"',
                                    '"Do you recommend specific charts given this dataset?"',
                                    '"What columns should I investigate further?"',
                                ]
                            ),
                            autosize=True,
                            minRows=2,
                            id="question",
                        ),
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Submit",
                                    id="chat-submit",
                                    disabled=True,
                                ),
                            ],
                            position="right",
                        ),
                        dmc.LoadingOverlay(
                            html.Div(
                                id="chat-output",
                            ),
                        ),
                    ],
                    id="chat-container",
                ),
            ],
            shadow="xs",
            id="flex",
        ),
        utils.upload_modal(),
        html.Div(id="current-charts"),
    ],
    id="padded",
)


@callback(
    Output("chat-output", "children"),
    Output("question", "value"),
    Input("chat-submit", "n_clicks"),
    State("chart-editor", "dataSources"),
    State("question", "value"),
    State("chat-output", "children"),
    prevent_initial_call=True,
)
def chat_window(n_clicks, data, question, cur):
    df = pd.DataFrame(data)

    prompt = utils.generate_prompt(df, question)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    question = [
        dcc.Markdown(
            completion.choices[0].message.content, className="chat-item answer"
        ),
        dcc.Markdown(question, className="chat-item question"),
    ]

    return (question + cur if cur else question), None


@callback(
    Output("chart-editor", "saveState"),
    Input("add-to-layout", "n_clicks"),
    prevent_initial_call=True,
)
def save_figure_to_chart_editor(n):
    if n:
        return True


@callback(
    Output("current-charts", "children"),
    Input("chart-editor", "figure"),
    State("chart-editor", "dataSources"),
    State("current-charts", "children"),
    prevent_initial_call=True,
)
def save_figure(figure, data, cur):
    # cleaning data output for unnecessary columns
    figure = dce.cleanDataFromFigure(
        figure,
    )
    df = pd.DataFrame(data)
    # create Figure object from dash-chart-editor figure
    figure = dce.chartToPython(figure, df)

    # Validate there's something to save
    if figure.data:
        item = [dmc.Paper([dcc.Graph(figure=figure)])]

        header = [
            html.Div(
                [
                    html.H2("Saved figures"),
                    dcc.Clipboard(
                        id="save-clip",
                        title="Copy link",
                        style={"margin-left": "10px"},
                    ),
                ],
                style={"display": "flex"},
            )
        ]
        return cur + item if cur else header + item

    return no_update
