'''upload file, view dataframe and line plot'''

import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
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


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
    
    fig=px.line(decoded,x=decoded.columns[0],y=decoded.columns[1])
    
    return html.Div([
        html.H5(filename),

        dcc.Graph(figure=fig),

        # Use the DataTable for easy rendering of the uploaded content
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in decoded.columns])] +

            # Body
            [html.Tr([
                html.Td(decoded.iloc[i][col]) for col in decoded.columns
            ]) for i in range(min(len(decoded), 5))]
        ),

        
        html.Hr(),
        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

    
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        children = parse_contents(contents, filename)
        return children

if __name__ == '__main__':
    app.run_server(debug=True)
