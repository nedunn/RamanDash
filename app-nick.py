import pandas as pd
import base64
import io
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
from dash import dash_table


app = dash.Dash(__name__)

#------------------------
# App Layout
app.layout = html.Div([
     html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag or Drop',
                html.A('Select Files')]
            ),
            style ={
                "width": '100%',
                "height": '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle':'dashed',
                'borderRadium': '5px',
                'textAlign':'center',
                'margin':'10px'},
            multiple=True)]),
    html.Div(id='output-data-upload',children=[]),
    html.Div(id='myGraph')
])
# -----------------------

# Deal with file upload and importing
def parseContents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded=base64.b64decode(content_string)
    print(decoded)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),header=None)
    except Exception as e:
        print(e)
        return(html.Div(['There was an error processing the files']))
    
    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name':i,'id':i} for i in df.columns],
            page_size=6),
        html.Hr()
    ])

# Callback section:Process Data and plot
@app.callback(
    [Output(component_property='children',component_id='output-data-upload')],
    # Output(component_id='myGraph', component_property='figure')],
    [Input(component_id='upload-data',component_property='contents')],
    [State(component_id='upload-data',component_property='filename')]
)

def myPlot(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parseContents(c,n) for c,n in zip(list_of_contents, list_of_names)]
        df = pd.DataFrame.from_dict(children)
        fig = px.scatter(data_frame = df , x=children[0],y=children[1])
        return children, fig

if __name__=='__main__':
    app.run_server(debug=True)

