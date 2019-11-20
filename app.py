#!/usr/bin/env python
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import data_handler as dh
import plotly.graph_objs as go

app = dash.Dash()

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

app.layout = html.Div([ 
    html.Label('Country: '),
    dcc.Dropdown(
        id='country-input',
        options=[
            {'label': u'United States', 'value': 'US'},
            {'label': u'Germany', 'value': 'DE'},
        ],
        value=['US']
    ),

    html.Label('Ticker: '),
    dcc.Input(id='ticker-input', value='AAPL', type='text'),
    html.Button(id='update-input', type='Update', children='Update'),
    html.Div(dcc.Graph(id='graph-output'))

])

@app.callback(
    Output('graph-output', 'figure'),
    [Input('update-input', 'n_clicks')],
    [State('ticker-input', 'value'),
     State('country-input','value')]
    )

def update_graph_output(n_clicks, ticker, country):
    df_daily = dh.get_daily_stock_data(ticker, country)
    df_date =df_daily['date']
    df_closing = df_daily['close']

    trace1 = go.Scatter(y=df_closing, x=df_date, mode='lines', name="AAPL", marker={"size": 3})
    return {"data": [trace1],
             "layout": go.Layout(title="Wage Rigidity",
                    yaxis={"title": "% of Jobstayers With a Wage Change of Zero", "range": [df_closing.min()*0.9, df_closing.max()*1.1],
                            "tick0": 0, "dtick": 50},
                    xaxis={"title": "Year",
                            'rangeselector': {'buttons': list([
                                {'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                {'step': 'all'}]) }})}
if __name__ == '__main__':
    app.run_server(debug=True)