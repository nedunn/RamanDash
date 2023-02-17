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
#https://dash.plotly.com/layout

'''Figure features to add:
truncate
peak label size
set y axis range'''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

######################################################
#Layout Functions
######################################################

def slider_layout():
    return {'placement':'bottom','always_visible':True}#,{'padding':20,'flex':1}#{'width':'50%','display':'flex',}

def upload():
    return html.Div(children=[dcc.Upload(id='upload-data',
                      children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                      multiple=True,style={'width': '100%','height': '30px',
                                           'lineHeight': '30px','borderWidth': '1px',
                                           'borderStyle': 'dashed','borderRadius': '5px',
                                           'textAlign': 'center','margin': '1px'}),
            html.Div(id='output-data-upload')])
            #dcc.Graph(id='graph',figure=go.Figure())])

def input_style():
    return{'padding':20,'flex':1}

def input1():
    return html.Div(children=[
        html.Label('Set Title: '),
        dcc.Input(id='title-input',placeholder=''),

        html.Br(),

        html.Label('Set Title Size: '),
        dcc.Slider(10,70,value=40, id='title-size',
                   tooltip=slider_layout()),
        html.Div(id='container'),

        html.Br(),html.Br(),

        html.Label('Enter Raman Spectra details: '),
        dcc.Input(id='details',value=''),
        
        html.Br(),

        html.Label('Set detail size: '),
        dcc.Slider(10,30,value=20,id='det-size',tooltip=slider_layout()),

        html.Br(),

        html.Label('Set detail x,y location: '),
        dcc.Slider(-1,1.5,value=0.95,id='det-ax',tooltip=slider_layout()),
        dcc.Slider(-1,2,value=1.1,id='det-ay',tooltip=slider_layout())

    ],style=input_style())

def input2():
    return html.Div(children=[
        html.Label('Enter Raman peaks: '),
        dcc.Input(id='peaks',placeholder='comma separated values'),
        html.Label('Set peak label size: '),
        dcc.Slider(10,30,value=20,id='peak-size',tooltip=slider_layout()),
        html.Label('Set peak label height: '),
        dcc.Slider(-1,2,value=1.2,id='peak-height',tooltip=slider_layout()),

        html.Br(),html.Br(),

        html.Label('Set legend text size: '),
        dcc.Slider(10,30,value=20,id='legend',tooltip=slider_layout())
        ],
        style=input_style())

def build_inputs():
    return html.Div(html.Div([input1(),input2()],
                    style={'display':'flex','flex-direction':'row'}))

def build_layout():
    return html.Div([upload(),build_inputs()])

######################################################
#Handle input

def parse_contents(content_string):
    decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
    return decoded

######################################################
#Figure Functions
######################################################

def trace(x,y,name,i,fig):
    fig=go.Figure(fig)
    fig.add_trace(go.Scatter(x=x,y=y,name=name.split('.csv')[0]),row=i,col=1)
    fig.update_layout(template='simple_white')
    return fig


######################################################
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = build_layout()

##########################################################
#'details','det-size','det-ax','det-ay',
# 'peaks','peak-size','peak-height','legend'

@app.callback(
    #Output('container','children'),
    Output('output-data-upload','children'),
    [Input('upload-data','contents'),
    Input('upload-data','filename'),
    Input('title-size','value'),
    Input('det-size','value'),
    Input('det-ax','value'),
    Input('det-ay','value'),
    Input('peak-size','value'),
    Input('peak-height','value'),
    Input('legend','value'),
    Input('title-input','value'),
    Input('details','value'),
    Input('peaks','value')]
    )



def update_output(list_of_contents,list_of_filenames, #Input from Files
                  tsize,dsize,dx,dy,psize,ph,lsize, #Input from user variables
                  title,details,peaks #State inputs
                  ):
    
    if list_of_filenames is not None:
        num=len(list_of_filenames) #Get # of files uploaded
        #Initalize empty plot
        fig=sp.make_subplots(rows=num,cols=1,vertical_spacing=0,
                             shared_xaxes=True,
                             x_title='Raman  Shift (cm-1)',
                             y_title='Intensity')
        
        i=1
        children=[]
        
        #Add Traces: Iterate through uploaded files
        for content_string, name in zip(list_of_contents,list_of_filenames):
            content_type, content_string = content_string.split(',')
            decoded = parse_contents(content_string)
            x,y=decoded.iloc[:,0],decoded.iloc[:,1]
            fig=trace(x,y,name,i,fig)
            i=i+1

        #Add Figure Details
        fig.add_annotation(xref='paper',yref='paper',showarrow=False,
                           xanchor='left',x=dx,y=dy,text=details,
                           font_size=dsize)
        fig.update_layout(title_text=title,title_font_size=tsize,
                          legend=dict(yanchor='bottom',y=0),
                          legend_font_size=lsize)
                          #height=fig_h, width=fig_w)

        if peaks is not None:
            numbers=[int(num) for num in peaks.split(',')]
            for n in numbers:
                fig.add_vline(x=n,line_width=0.5,opacity=0.4)
                fig.add_annotation(x=n,y=ph,yref='paper',text=f'{n:.0f}',
                                   showarrow=False,textangle=-50,
                                   font_size=psize)

        children.append(dcc.Graph(id='graph',figure=fig))
        return children

if __name__ == '__main__':
    app.run(debug=True)

#'title-input','title-size','details','det-size','det-ax','det-ay',
# 'peaks','peak-size','peak-height','legend'