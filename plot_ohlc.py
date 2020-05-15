# -*- coding: utf-8 -*-

import sys
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from stocktools.json_to_df import json_to_df


colors = {
    'background': '#00336c',
    'text': '#e2efff'
}

dropdown_options = [
    {'label': 'Adobe', 'value': 'ADBE'},
    {'label': 'Apple Inc', 'value': 'AAPL'},
    {'label': 'Amazon', 'value': 'AMZN'},
    {'label': 'Netflix', 'value': 'NFLX'},
    {'label': 'Nike', 'value': 'NKE'},
    {'label': 'Nvidia', 'value': 'NVDA'},
    {'label': 'Oracle', 'value': 'ORCL'},
    {'label': 'Starbucks', 'value': 'SBUX'},
    {'label': 'Tesla', 'value': 'TSLA'},
    {'label': 'Intuit', 'value': 'INTU'},
    {'label': 'Johnson & Johnson', 'value': 'JNJ'},
    {'label': 'JP Morgan Chase', 'value': 'JPM'},
]

external_stylesheets = ["/assets/style.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,)

app.layout = html.Div([
    html.Div(
        html.H2(
            children='Stocks Dashboard',
            style={
                'fontSize': 50,
                'fontWeight': 150,
                # 'borderRadius': '15px',
                # 'overflow': 'hidden',
                'font-family': ['Poppins', 'sans-serif'],
                # 'backgroundColor': colors['background'],
                'textAlign': 'center',
                'color': ' #001731',
            }
        ), className="pretty_container"),
    html.Div(
        children=[
            dcc.Tabs(id="side_panel",
                     vertical=True, className='pretty_container',
                     children=[
                         dcc.Tab(className="pretty_container", label="About",
                                 children=html.Div(className="plot_selection_panel pretty_container",
                                                   children=[
                                                             html.H4(
                                                                 "Author: Sergio Chairez"),
                                                             html.Hr(),
                                                             html.P(
                                                                 "I was inspired to make an OHLC chart...")
                                                   ],
                                                   style={'font-family': ['Poppins', 'sans-serif'],
                                                          'fontWeight': 60, }),),
                         dcc.Tab(label="View", className="pretty_container",
                                 children=[html.Div(className="pretty_container",
                                                    children=[
                                                              html.H3("""Choose the company symbol""",
                                                                      style={
                                                                          # 'margin-right': '2em',
                                                                          'fontWeight': 150,
                                                                          'margin': 0,
                                                                          'padding': ['0.5em', '5em'],
                                                                          # 'borderRadius': '15px',
                                                                          'overflow': 'auto',
                                                                          'font-family': ['Poppins', 'sans-serif'],
                                                                          'display':'inline-block',
                                                                          # 'backgroundColor': colors['background'],
                                                                          #    'textAlign': 'center',
                                                                          'color': ' #001731', }),
                                                              dcc.Dropdown(multi=False,
                                                                           clearable=False,
                                                                           style=dict(
                                                                               #   width='40%',
                                                                               #  verticalAlign="middle",
                                                                               display='inline-block',
                                                                           ),
                                                                           id='symbolDropdown',
                                                                           className="horizontal_dropdowns",
                                                                           options=dropdown_options,
                                                                           value='AAPL'
                                                                           )])
                                           ]),
                     ]),

        ], style={'float': 'left', 'margin': 'auto',
                  'display': 'flex', },

    ),
    html.Div(
        [
            dcc.Graph(id='main_graph')
        ],
        className='pretty_container eight columns',
        style={'float': 'right', 'margin': 'auto'}
    ),

])


@app.callback(
    Output('main_graph', 'figure'),
    [Input('symbolDropdown', 'value')],
)
def render_ohlc_graph(symbolDropdown: str):
    print(symbolDropdown)
    co_df = json_to_df(f"data_{symbolDropdown.lower()}.json",
                       path=f"data/data_raw/data_{symbolDropdown.lower()}.json")

    title = f"{symbolDropdown.lower()} Historical Graph"
    hovertext = []
    for i in range(len(co_df['Open'])):
        hovertext.append(
            co_df['Date'][i].strftime("%m/%d/%Y") +
            '<br>O: '+str(round(co_df['AdjOpen'][i], 4)) +
            '\tH: '+str(round(co_df['AdjHigh'][i], 4)) +
            '<br>L: '+str(round(co_df['AdjLow'][i], 4)) +
            '\tC: '+str(co_df['AdjClose'][i]))

    trace_ohlc = go.Candlestick(x=co_df['Date'],
                                open=co_df['AdjOpen'],
                                high=co_df['AdjHigh'],
                                low=co_df['AdjLow'],
                                close=co_df['AdjClose'],
                                text=hovertext,
                                hoverinfo='text',
                                name="OHLC"
                                # increasing_line_color='#0048BA',
                                # decreasing_line_color='#E60000'
                                )
    trace_sma_20_day = go.Scatter(
        x=co_df['Date'], y=co_df['SMA_20day'], name="SMA_20day", visible=True)
    trace_ema_20_day = go.Scatter(
        x=co_df['Date'], y=co_df['EMA_20day'], name="EMA_20day")

    fig = go.Figure(data=[trace_ohlc, trace_sma_20_day, trace_ema_20_day],
                    layout=go.Layout(
        title=title,
        # width=1200,
        # height=600,
        # plot_bgcolor=colors['background'],
        paper_bgcolor='#F9F9F9',
        xaxis_rangeslider_visible=True)
    )
    print(type(fig))

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends
            # hide Christmas and New Year's
            dict(values=["2015-12-25", "2016-01-01"])
        ]
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        )
    )

    return fig


# style={
#     "display": "flex",
#     "flex-direction": "column"
# })

# app.layout = html.Div(
#     style={'backgroundColor': colors['background']},
#     children=[
#         html.H1(
#             children='Historical OHLC Chart',
#             style={
#                 'fontSize': 50,
#                 'text-decoration': 'underline',
#                 'font-family': 'Ubuntu',
#                 'textAlign': 'center',
#                 'color': colors['text']
#             }
#         ),
#         html.Div(children='Choose the company symbol below', style={
#             'textAlign': 'center',
#             'fontSize': 25,
#             'color': colors['text']
#         }),
#         dcc.Graph(
#             id='ohlc_graph',
#             figure=fig), ]
# )
# html.Label('OHLC Graph'),

if __name__ == "__main__":

    app.run_server(debug=True, use_reloader=True)

    # fig.update_layout(title="AAPL Stock", xaxis_rangeslider_visible=False)
    # fig.update_layout(xaxis_rangeslider_visible=False)

    # fig.show()

    # fig.write_image('figure.png')
