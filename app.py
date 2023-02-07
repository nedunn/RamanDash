import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=True,
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
    html.Div(id='output-data-upload'),
])

def build_fig(df,x,y,name):
    fig=px.line(df,x=x,y=y)
    fig.update_layout(template='simple_white',xaxis_title='Raman Shift (cm-1)',yaxis_title='Intensity')
    fig.add_annotation(xref='paper',yref='paper',showarrow=False,text=name.split('.csv')[0],
                       x=1,y=1.1)
    return fig



def parse_contents(content_string):
    decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
    return decoded

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data','filename')])

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = []
        for content_string, name in zip(list_of_contents,list_of_names):
            content_type, content_string = content_string.split(',')
            decoded = parse_contents(content_string)
            children.append(
                dcc.Graph(
                    figure=build_fig(decoded,decoded.columns[0],decoded.columns[1],name),
                    style={'height': '300px'}
            ))
        return children

if __name__ == '__main__':
    app.run_server(debug=True)



#___CONVERT TO SUBPLOTS___
# import plotly.subplots as sp

# @app.callback(Output('output-data-upload', 'children'),
#               [Input('upload-data', 'contents'),
#                Input('upload-data', 'filename')])
# def update_output(list_of_contents, list_of_names):
#     if list_of_contents is not None:
#         children = []
#         fig = sp.make_subplots(rows=len(list_of_contents), cols=1,
#                                vertical_spacing=0.2)
#         for i, (content_string, name) in enumerate(zip(list_of_contents, list_of_names)):
#             content_type, content_string = content_string.split(',')
#             decoded = parse_contents(content_string)
#             fig.add_trace(px.line(decoded, x=decoded.columns[0], y=decoded.columns[1]),
#                           row=i+1, col=1)
#             fig.update_layout(title=name)
#         children.append(dcc.Graph(figure=fig))
#         return children





