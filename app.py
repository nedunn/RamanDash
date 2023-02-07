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
import plotly.subplots as sp

#__________
#Set up initial app
#__________
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

    html.Div([html.Label('Enter Title: '),
              dcc.Input(id='title-input',placeholder='')]),
    

    html.Div([html.Label('Set Title Text Size: '),
              dcc.Input(id='title-size',value=40,type='number')],
              style={'margin-top':'10px'}),
    
    html.Div([html.Label('Enter Raman Spectra details: '),
              dcc.Input(id='details',value=' ',placeholder='separate with comma')],
              style={'margin-top':'10px'}),
    
    html.Div([html.Label('Enter peak values: '),
              dcc.Input(id='peaks', placeholder='comma separated values')
            #html.Button('Update Plot', id='submit'),
            ],
            style={'margin-top':'10px'}),
    
    html.Div([html.Button('Update Plot',id='submit')])
    #html.Div([html.Button('Clear',id='clear')])
])

#__________
#Figure Making Functions
#__________
def build_fig(df,x,y,name):
    fig=px.line(df,x=x,y=y)
    fig.update_layout(template='simple_white',xaxis_title='Raman Shift (cm-1)',yaxis_title='Intensity')
    fig.add_annotation(xref='paper',yref='paper',showarrow=False,text=name.split('.csv')[0],
                       x=1,y=1.1)
    return fig

def trace(x,y,name,i,fig):
    fig.add_trace(go.Scatter(x=x,y=y,name=name.split('.csv')[0]),row=i,col=1)
    fig.update_layout(template='simple_white')
    return fig

def data_grab(x,y,name):
    #x,y=pd.Series(x),pd.Series(y)
    df=pd.DataFrame([x,y]).T
    #df['name']=name.split('.csv')[0]
    print(df)

#__________
#Read Input Data
#__________
def parse_contents(content_string):
    decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
    return decoded

# @app.callback(Output('output-data-upload', 'children'),
#               [Input('upload-data', 'contents'),
#                Input('upload-data','filename'),
#                Input('title-input','value'),
#                Input('details','value'),
#                Input('title-size','value'),
#                Input('peaks','value')])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data','filename'),
               Input('submit','n_clicks')],
               [State('title-input','value'),
               State('details','value'),
               State('title-size','value'),
               State('peaks','value')])

#__________
#Apply Update
#__________
def update_output(list_of_contents, list_of_names,n_clicks,title,details,tsize,peaks):
    if list_of_contents is not None:
        num=len(list_of_contents) #Number of files uploaded
        fig=sp.make_subplots(rows=num,cols=1,vertical_spacing=0, #initialize figure
                             shared_xaxes=True,
                             x_title='Raman Shift (cm-1)',
                             y_title='Intensity') 
        i=1
        children=[]
        for content_string, name in zip(list_of_contents,list_of_names):
            content_type, content_string = content_string.split(',')
            decoded = parse_contents(content_string)
            x,y=decoded.iloc[:,0],decoded.iloc[:,1]
            fig=trace(x,y,name,i,fig)
            i=i+1
        fig.add_annotation(xref='paper',yref='paper',showarrow=False,
                           xanchor='left',x=1,y=1.02,text=details)
        fig.update_layout(title_text=title,title_font_size=tsize,
                          legend=dict(yanchor='bottom',y=0))
        
        if peaks is not None:
            numbers=[int(num) for num in peaks.split(',')]
            for n in numbers:

                fig.add_vline(x=n,line_width=0.5,opacity=0.4)
                fig.add_annotation(x=n,y=1.1,yref='paper',text=f'{n:.0f}',showarrow=False,textangle=-50)

        
        children.append(dcc.Graph(id='graph',figure=fig))
        return children


    
#__________
#Run it!
#__________
if __name__ == '__main__':
    app.run_server(debug=True)



#__________
#multip call backs
#__________
# app = dash.Dash()

# app.layout = html.Div([
#     html.Div([
#         dcc.Input(id='title-input', type='text', value='Default Title'),
#     ]),
#     html.Button('Submit', id='submit'),
#     html.Button('Clear', id='clear'),
#     html.Div(id='output-data-upload'),
# ])

# @app.callback(
#     Output(component_id='output-data-upload', component_property='children'),
#     [Input(component_id='submit', component_property='n_clicks')],
#     [State(component_id='title-input', component_property='value')]
# )
# def update_output(n_clicks, value):
#     return html.Div([
#         html.H1(value)
#     ])

# @app.callback(
#     Output(component_id='title-input', component_property='value'),
#     [Input(component_id='clear', component_property='n_clicks')]
# )
# def clear_title(n_clicks):
#     return ''

# if __name__ == '__main__':
#     app.run_server()


#___Attempt at adding traces___

# figure=go.Figure()

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Upload(
#         id='upload-data',
#         children=html.Div([
#             'Drag and Drop or ',
#             html.A('Select Files')
#         ]),
#         multiple=True,
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         }
#     ),
#     html.Div(id='output-data-upload')
# ])

# def trace(x,y,name,current_fig):
#     fig=go.Figure(current_fig)
#     fig.add_trace(go.Scatter(x=x,y=y,name=name))
#     return fig

# def parse_contents(content_string):
#     decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
#     return decoded

# @app.callback(Output('graph','figure'),
#               [Input('upload-data', 'contents'),
#                Input('upload-data','filename')])
# # def update_output(list_of_contents, list_of_names,figure):
# #     if list_of_contents is not None:
# #         for content_string, name in zip(list_of_contents,list_of_names):
# #             content_type, content_string=content_string.split(',')
# #             df=parse_contents(content_string)
# #             figure=trace(df.iloc[:,0],df.iloc[:,1],name,figure)
# #         return figure

# def update_output(list_of_contents, list_of_names, figure):
#     if list_of_contents is not None:
#         dcc.Graph(id='graph', figure=go.Figure())
#         for content_string, name in zip(list_of_contents,list_of_names):
#             content_type, content_string=content_string.split(',')
#             df=parse_contents(content_string)
#             figure=trace(df.iloc[:,0],df.iloc[:,1],name,figure)
        
#     return figure

# if __name__ == '__main__':
#     app.run_server(debug=True)

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