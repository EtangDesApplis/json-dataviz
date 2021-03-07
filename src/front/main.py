from flatten_json import flatten
import json
import os
import time
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#import pandas as pd
import flask

# reference: https://pypi.org/project/flatten-json/

def is_number(param):
    try:
        float(param)
        return True
    except:
        return False

def safe_load_json(fn):
    try:
        return json.load(open(fn))
    except Exception as e:
        print(str(e))
        return {}

def safe_get_file_timestamp(fn):
    try:
        return time.ctime(os.path.getmtime(fn))
    except:
        return 'file not found'

class jsonDataViz:
    def __init__(self,jsonFile):
        self.jsonFile=jsonFile
        #all indices as many as possible
        self.regexPattern=r'\w+'
        

    def update(self,jsonFile=None):
        #update json database if provided
        if jsonFile!=None:
            self.jsonFile=jsonFile
        #reinit
        self.data_indices=[]
        self.data_types=[]
        self.flatten_dict={}
        self.data_filteredIndices=[]
        self.filer=None
        self.timeStamp=safe_get_file_timestamp(self.jsonFile)

        self.flatten_dict=flatten(safe_load_json(self.jsonFile))
        for key in self.flatten_dict.keys():
            if is_number(self.flatten_dict[key]):
                tmp=key.split("_")
                category=tmp[-1]
                index="_".join(tmp[:-1])
                if category not in self.data_types:
                    self.data_types.append(category)
                if index not in self.data_indices:
                    self.data_indices.append(index)

    def filter(self):
        # ^cluster\d+_vm_\w+
        # ^cluster\d+$
        # \w+
        self.data_filteredIndices=[]
        if self.regexPattern=="":
            # no filer or \w+
            self.data_filteredIndices=self.data_indices
        else:
            p=re.compile(self.regexPattern)
            for key in self.data_indices:
                if p.match(key):
                    self.data_filteredIndices.append(key)

    def get_indices(self):
        return self.data_filteredIndices

    def get_valuesOfType(self,category):
        res=[]
        for key in self.data_filteredIndices:
            try:
                res.append(self.flatten_dict["%s_%s"%(key,category)])
            except:
                res.append(0)
        return res


def render_layout():

    jdv.update()

    return html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children=os.getenv('JSON_DATAVIZ_REPORT_TITLE',jdv.jsonFile),
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(
            children='Last updated : %s'%(jdv.timeStamp),
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(id='my-graph'),
        html.Div([
            dcc.Input(\
                id='my-index-patern',\
                placeholder=os.getenv('JSON_DATAVIZ_FILTER_HINTS','Enter a regex pattern to filter indices'),\
                style={'width': '100%', 'float': 'left', 'display': 'inline-block'},\
                type='text',\
                value=os.getenv('JSON_DATAVIZ_DEFAULT_FILTER',''),\
                debounce=True)
        ],style={'width': '50%', 'float': 'left', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(\
                id='index-hint',\
                placeholder='Available indices',\
                options=[{'label': i, 'value': i} for i in jdv.data_indices],\
                value=None,\
                multi=True)
        ],style={'width': '50%', 'float': 'left', 'display': 'inline-block'})
    ])


jdv=jsonDataViz(os.getenv('JSON_DATAVIZ_DATABASE_FILE','database.json'))
#external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server=flask.Flask(__name__)
#app=dash.Dash(__name__,server=server,external_stylesheets=external_stylesheets)
app=dash.Dash(__name__,server=server)
colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}



app.layout=render_layout

@app.callback(dash.dependencies.Output('my-graph','figure'),\
              [dash.dependencies.Input('my-index-patern','value')])
def update_figure(indexPattern):

    jdv.regexPattern=indexPattern
    jdv.filter()

    #init plotly data
    res={
        'data':[],
        'layout': {
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            },
            'barmode':'stack',
            'xaxis':{'title':os.getenv('JSON_DATAVIZ_XAXIS_TITLE','')},
            'yaxis':{'title':os.getenv('JSON_DATAVIZ_YAXIS_TITLE','')}
        }}
    #fill data
    x=jdv.get_indices()
    #print(x)
    #print(jdv.data_types)
    for legend in jdv.data_types:
        y=jdv.get_valuesOfType(legend)
        #print(legend)
        #print(y)
        res['data'].append({'x':x,'y':y,'type':'bar','name':legend})

    return res

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8080,debug=False)