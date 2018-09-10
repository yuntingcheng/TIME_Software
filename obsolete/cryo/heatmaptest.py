import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import fakedata
import fakedataall
import random

print('Hello!')

app = dash.Dash()

app.layout = html.Div([
    html.Button('Show Heatmap', id='showHeatmap'),
    html.Div([
        dcc.RadioItems(
                id='heatmapOptions',
                options=[
                    {'label': 'MCE 1 RC 1', 'value': 1},
                    {'label': 'MCE 1 RC 2', 'value': 2},
                    {'label': 'MCE 1 RC 3', 'value': 3},
                    {'label': 'MCE 1 RC 4', 'value': 4},
                    {'label': 'MCE 2 RC 1', 'value': 5},
                    {'label': 'MCE 2 RC 2', 'value': 6},
                    {'label': 'MCE 2 RC 3', 'value': 7},
                    {'label': 'MCE 2 RC 4', 'value': 8},
                ],
                value=1
            ),
        dcc.Dropdown(
            id='readoutcard',
            options=[
                {'label': 'Select an Option', 'value': ''},
                {'label': 'MCE 1 RC 1', 'value': 1},
                {'label': 'MCE 1 RC 2', 'value': 2},
                {'label': 'MCE 1 RC 3', 'value': 3},
                {'label': 'MCE 1 RC 4', 'value': 4},
                {'label': 'MCE 2 RC 1', 'value': 5},
                {'label': 'MCE 2 RC 2', 'value': 6},
                {'label': 'MCE 2 RC 3', 'value': 7},
                {'label': 'MCE 2 RC 4', 'value': 8},
                {'label': 'RC All', 'value': 9}
            ],
            value=''
        )]),
    dcc.Graph(id='heatmap'),
    dcc.Interval(
        id='heatInterval',
        interval=1*5000,
        n_intervals=0
    )
    ])

def modZData(z, rc):
    new_z = []

    #1 -> 0-7, 2 -> 8-15, 3 -> 16-23, 4 -> 24-31
    if rc % 4 == 1:
        for i in range(32):
            new_z.append(z[i][:8])
    elif rc % 4 == 2:
        for i in range(32):
            new_z.append(z[i][8:16])
    elif rc % 4 == 3:
        for i in range(32):
            new_z.append(z[i][16:24])
    elif rc % 4 == 0:
        for i in range(32):
            new_z.append(z[i][24:])

    return new_z

@app.callback(
    Output('heatmap', 'figure'),
    [Input('showHeatmap', 'n_clicks'),
     Input('heatInterval', 'n_intervals'),
     Input('heatmapOptions', 'value'),
     Input('readoutcard', 'value')])
def initHeatmap(n_clicks, n_intervals, heatmapOptions, readoutcard):
    parameters = [1, 2, 9]
    parameters[2] = readoutcard
    if parameters[2] == 9:
        parameters[2] = 'All'

    if parameters[2] == 'All':
        print('All Readout Cards')
        tempfile = open('tempzdata.txt', 'r')
        #z = [[ [] for i in range(32)] for j in range(32)]
        z = []
        for line in tempfile:
            x = line.strip().split()
            for i in range(len(x)):
                x[i] = int(x[i])
            z.append(x)
        tempfile.close()

        new_z = modZData(z, heatmapOptions)

        data = [
                go.Heatmap(z=new_z,
                           x=['CH1', 'CH2', 'CH3', 'CH4', 'CH5','CH6','CH7','CH8'],
                           y=['Row1','Row2','Row3','Row4','Row5','Row6','Row7',\
                              'Row8','Row9','Row13','Row11','Row12','Row13','Row14',\
                              'Row15','Row16','Row17','Row18','Row19','Row23','Row21',\
                              'Row22','Row23','Row24','Row25','Row26','Row27','Row28',\
                              'Row29','Row33','Row31','Row32','Row33'])
        ]

        if heatmapOptions == 1:
            layout = go.Layout(title = 'MCE 1 RC 1',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 2:
            layout = go.Layout(title = 'MCE 1 RC 2',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 3:
            layout = go.Layout(title = 'MCE 1 RC 3',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 4:
            layout = go.Layout(title = 'MCE 1 RC 4',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 5:
            layout = go.Layout(title = 'MCE 2 RC 1',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 6:
            layout = go.Layout(title = 'MCE 2 RC 2',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 7:
            layout = go.Layout(title = 'MCE 2 RC 3',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif heatmapOptions == 8:
            layout = go.Layout(title = 'MCE 2 RC 4',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

    else:
        print('Readout Card', parameters[2])
        z = fakedata.getMCEData()

        data = [
                go.Heatmap(z=z,
                           x=['CH1', 'CH2', 'CH3', 'CH4', 'CH5','CH6','CH7','CH8'],
                           y=['Row1','Row2','Row3','Row4','Row5','Row6','Row7',\
                              'Row8','Row9','Row13','Row11','Row12','Row13','Row14',\
                              'Row15','Row16','Row17','Row18','Row19','Row23','Row21',\
                              'Row22','Row23','Row24','Row25','Row26','Row27','Row28',\
                              'Row29','Row33','Row31','Row32','Row33'])
        ]

        if parameters[2] == 1:
            layout = go.Layout(title = 'MCE 1 RC 1',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 2:
            layout = go.Layout(title = 'MCE 1 RC 2',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 3:
            layout = go.Layout(title = 'MCE 1 RC 3',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 4:
            layout = go.Layout(title = 'MCE 1 RC 4',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 5:
            layout = go.Layout(title = 'MCE 2 RC 1',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 6:
            layout = go.Layout(title = 'MCE 2 RC 2',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 7:
            layout = go.Layout(title = 'MCE 2 RC 3',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

        elif parameters[2] == 8:
            layout = go.Layout(title = 'MCE 2 RC 4',
                          xaxis = dict(title = 'Channel'),
                          yaxis = dict(title = 'Row'))

    fig = go.Figure(data=data, layout=layout)

    return fig


if __name__ == '__main__':
	app.run_server(debug=True)
