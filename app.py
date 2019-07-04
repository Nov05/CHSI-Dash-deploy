
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import colorlover

url = "https://raw.githubusercontent.com/Nov05/CHSI-Dash/master/data/DEMOGRAPHICS.csv"
path = './data/DEMOGRAPHICS.csv'
demogr = pd.read_csv(url)
cols = demogr.columns.tolist()

colorscales = ["Greens", "YlOrRd", "Bluered", "RdBu", "Reds", 
               "Blues", "Picnic", "Rainbow", "Portland", "Jet", 
               "Hot", "Blackbody", "Earth", "Electric", "Viridis", 
               "Cividis"]
portland = [
    [0, 'rgb(12,51,131)'], [0.25, 'rgb(10,136,186)'],
    [0.5, 'rgb(242,211,56)'], [0.75, 'rgb(242,143,56)'],
    [1, 'rgb(217,30,30)']
]
bgcolor = 'rgba(238, 238, 238, 1)'
portland_rgb = [i[1] for i in portland]

#########################################################################
# 3D Scatter
#########################################################################
def display_fig(in_age=0, in_slice=0, in_range=0):
    
  # Age  
  # 19 Under, col 17 = 0
  # 20-64, col 20 = 1
  # 65-84, col 23 = 2
  # 85 Over, col 26 = 3  
  if in_age==0:
    y = demogr[cols[17]]
    titley = "y = Age Under 19"
  elif in_age==1:
    y = demogr[cols[20]]
    titley = "y = Age 20-64"
  elif in_age==2:
    y = demogr[cols[23]]
    titley = "y = Age 65-84"
  elif in_age==3:
    y = demogr[cols[26]]
    titley = "y = Age Above 85"
    
  # log10(population density), poverty
  x = np.log10(demogr[cols[11]].replace([-2222,0], [demogr[cols[11]].mean(),1]))
  z = demogr[cols[14]].replace(-2222.2, demogr[cols[14]].mean())
  d = np.log10(demogr[cols[8]]) # log10(population)

  # slice data
  slicenum = 38
  slices = np.linspace(0, max(z), slicenum)
  
##############  
  if in_slice == 0: 
############## 
# display all data
    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=d*2,
            color=z,                     # set color to an array/list of desired values
            colorscale=colorscales[8],   # choose a colorscale
            opacity=1,
            showscale=True,
            colorbar=dict(x=0.81, len=0.5, 
                          thickness=10,
                          outlinecolor='white', outlinewidth=0,
                          title=dict(text="Poverty", font=dict(size=10))
                         ),
            line=dict(width=0.001, color='black')
        ),
        text='County Level',
        projection=dict(x=dict(show=True, opacity=0.1, scale=0.4),
                        y=dict(show=True, opacity=0.1, scale=0.4),
                        z=dict(show=True, opacity=0.1, scale=0.4),
                       )
    )
    data = [trace1]
##############    
  else: 
##############
# display sliced data
    # slice data
    if in_range<0 or in_range>slicenum: in_range=0
    condition = ((z >= slices[in_range]) & (z < slices[in_range+1]))
    x1 = x[condition]
    y1 = y[condition]
    z1 = [slices[in_range]] * len(x1)
    slicecolor =colorlover.interp(portland_rgb, slicenum)[in_range]

    # create a plane
    p1 = np.linspace(0, max(x), 5)
    p2 = np.linspace(0, max(y), 5)
    p1, p2 = np.meshgrid(p1, p2)
    p3 = [[slices[in_range]] * 5] * 5
    
    ##############
    # plot
    ##############
    # this is all data points in very light gray
    trace1 = go.Scatter3d(
      x=x,
      y=y,
      z=z,
      mode='markers',
      name='county',
      marker=dict(
          size=d*2,
          color="black", 
          opacity=0.01,
          line=dict(width=0.00, color='black'),
          ),
          showlegend=False,
    )
    # this is a plane
    trace2 = go.Surface(
        x=tuple(p1),
        y=tuple(p2),
        z=tuple(p3),
        name='slice',
        colorscale="YlGnBu",
        opacity=0.5,
        showlegend=False,
        showscale=False,
    )
    # this is merely a colorbar
    trace3 = go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        name='',
        mode='markers',
        marker=dict(
            size=0.01,
            color=z, # set color to an array/list of desired values
            colorscale=portland, # choose a colorscale
            opacity=1,
            showscale=True,
            colorbar=dict(x=0.81, len=0.5, 
                          thickness=10,
                          outlinecolor='white', outlinewidth=0,
                          title=dict(text="Poverty", font=dict(size=10))
                         ),
            line=dict(width=0.01, color='gray')
        ),
        showlegend=False,
    )    
    # this is the actual sliced data points
    # why separating data points and colorbar?
    # cause I need only one color from the colorscale
    trace4 = go.Scatter3d(
        x=x1,
        y=y1,
        z=z1,
        name='Poverty',
        mode='markers',
        marker=dict(
            size=d*2,
            color=slicecolor,
            opacity=1,
            showscale=False,
            line=dict(width=0.01, color='gray')
        ),
        projection=dict(x=dict(show=True, opacity=0.1, scale=0.8),
                        y=dict(show=True, opacity=0.1, scale=0.8),
                        z=dict(show=True, opacity=0.1, scale=0.8),
                       ),
        showlegend=False,
    )    
    data = [trace1, trace3, trace4]
##############    
# end of if-else    
##############
    
  layout = go.Layout(
      autosize=False,
      width=700,
      height=600,
      margin=dict(l=0, r=0, b=0, t=0),
      scene=dict(xaxis=dict(title="x = Population Density (lg)"),
                 yaxis=dict(title=titley),
                 zaxis=dict(title="z = Poverty"),
#       bgcolor=bgcolor,
      ),
  )
  fig = go.Figure(data=data, layout=layout)
  return fig
   

fig = display_fig()


#########################################################################
# Dash App
#########################################################################
options1 = [
  {'label': 'All Data', 'value': 0},
  {'label': 'Sliced Data', 'value': 1},
]
options2 = [
  {'label': "Age Under 19", 'value': 0},  
  {'label': "Age 20-64", 'value': 1},  
  {'label': "Age 65-84", 'value': 2},  
  {'label': "Age Above 85", 'value': 3},  
]
marks1 = {
    0:"0", 10:"10", 20:"20", 30:"30"
}
  
app = dash.Dash(__name__)
server = app.server # this works but why?

app.config['suppress_callback_exceptions']=True
app.scripts.config.serve_locally = False
# url_css = "https://codepen.io/chriddyp/pen/bWLwgP.css"
url_css = "https://gist.githubusercontent.com/Nov05/c18c77e022df6a338318512fb3e8d3ef/raw/fdba953c93e3021e409b0857a759656e137b839a/CHSI-Dash.css"  
app._external_stylesheet = [url_css]

app.layout = html.Div(
#     style={'backgroundColor':bgcolor},
    children=[
    html.Div(children=[
      html.H1(children="CHSI Demographic Data",
              style={'padding-left': '10px'}),
      dcc.Dropdown(id="dropdown1", 
          options=options2,
          value=0,
          style = {'width': '300px',
                   'fontSize': '15px',
                   'padding-left': '20px',
                   'display': 'inline-block'},
          ),
      dcc.RadioItems(id='radio1',
          options=options1,
          value=0,
          labelStyle={'display': 'inline-block'},
          style = {'fontSize': '15px',
                   'padding-left': '20px',
                   'padding-top': '5px',
                  },                    
          ),  
      html.Div(id='text-slider1', children=[
        html.Div(children='Slice Data by Poverty Level',
        style = {'fontSize': '15px',
                 'padding-left': '20px',
                 'padding-top': '10px',
                }
        ),    
        html.Div(
        dcc.Slider(id="slider1",
            min=0,
            max=30,
            step=1,
            value=0,
            marks=marks1,
            ),
        style={'height': '20px', 
               'width': '300px',
               'padding-left': '25px',
               'padding-bottom': '10px',
               'display': 'inline-block'},     
        ),
      ], style={'display':'none'}),  
    ],
    style={'width': '100%',
           'marginBottom': 5, 'marginTop': 2,
           'padding-bottom': '10px',
           'border':'1px solid', 'border-radius': 10,
          }    
    ),
    dcc.Graph(id="graph", figure=fig),
])

@app.callback(Output("graph", "figure"), [Input("dropdown1", "value"), Input("radio1", "value"), Input('slider1', "value")])
def cb1(input1, input2, input3):
  return display_fig(in_age=input1, in_slice=input2, in_range=input3)

# hide slider bar if radio button 'Sliced Data' selected
@app.callback(Output('text-slider1','style'), [Input('radio1','value')])
def cb2(input1):
  if input1 in [1]: # Sliced Data
    return {'display': 'block'}
  else: # All Data
    return {'display': 'none'}

if __name__ == '__main__':
  app.run_server(debug=True)
