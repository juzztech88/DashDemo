import json

from dash import Dash, Input, Output, State
from dash import html, dcc
import pandas as pd
import plotly.express as px

'''
testNo --> demo concept
1 --> hoverData
2 --> overall
'''
testNo = 2

if testNo == 1:
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

    app.layout = html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Fertility rate, total (births per woman)',
                    id='crossfilter-xaxis-column',
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='crossfilter-xaxis-type',
                    labelStyle={'display' : 'inline-block', 'marginTop' : '5px'}
                )
            ],
            style={'width'  : '49%', 'display' : 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Life expectancy at birth, total (years)',
                    id='crossfilter-yaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='crossfilter-yaxis-type',
                    labelStyle={'display' : 'inline-block', 'marginTop' : '5px'}
                )
            ],
            style={'width' : '49%', 'float' : 'right', 'display' : 'inline-block'})
        ],
        style = {'padding' : '10px 5px'}),

        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points':[{'customdata':'Japan'}]}
            )
        ],
        style={'width':'49%', 'display':'inline-block', 'padding':'0 20p'}),

        html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
        ],
        style={'display':'inline-block', 'width' : '49%'}),

        html.Div([
            dcc.Slider(
                df['Year'].min(),
                df['Year'].max(),
                step=None,
                id='crossfilter--year--slider',
                value=df['Year'].max(),
                marks={str(year) : str(year) for year in df['Year'].unique()}
            )
        ],
        style={'width':'49%', 'padding':'0px 20px 20px 20px'})
    ])

    @app.callback(
        Output('crossfilter-indicator-scatter', 'figure'),
        Input('crossfilter-xaxis-column', 'value'),
        Input('crossfilter-yaxis-column', 'value'),
        Input('crossfilter-xaxis-type', 'value'),
        Input('crossfilter-yaxis-type', 'value'),
        Input('crossfilter--year--slider', 'value')
    )
    def update_graph(xaxis_column_name, yaxis_column_name,
                     xaxis_type, yaxis_type,
                     year_value):
        dff = df[df['Year']==year_value]
        fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                         y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                         hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

        fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

        fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type=='Linear' else 'log')
        fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type=='Linear' else 'log')
        fig.update_layout(margin={'l':40, 'b':40, 't':10, 'r':0},
                          hovermode='closest')
        return fig

    def create_time_series(dff, axis_type, title):
        fig = px.scatter(dff, x='Year', y='Value')
        fig.update_traces(mode='lines+markers')
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
        fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                           xref='paper', yref='paper', showarrow=False, align='left',
                           text=title)
        fig.update_layout(height=225, margin={'l':20, 'b':30, 'r':10, 't':10})
        return fig

    @app.callback(
        Output('x-time-series', 'figure'),
        Input('crossfilter-indicator-scatter', 'hoverData'),
        Input('crossfilter-xaxis-column', 'value'),
        Input('crossfilter-xaxis-type', 'value')
    )
    def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
        country_name = hoverData['points'][0]['customdata']
        dff = df[df['Country Name']==country_name]
        dff = dff[dff['Indicator Name']==xaxis_column_name]
        title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
        return create_time_series(dff, axis_type, title)

    @app.callback(
        Output('y-time-series', 'figure'),
        Input('crossfilter-indicator-scatter', 'hoverData'),
        Input('crossfilter-yaxis-column', 'value'),
        Input('crossfilter-yaxis-type', 'value')
    )
    def update_y_timeseries(hoverData, yaxis_column_name, yaxis_type):
        country_name = hoverData['points'][0]['customdata']
        dff = df[df['Country Name']==country_name]
        dff = dff[dff['Indicator Name'] == yaxis_column_name]
        return create_time_series(dff, yaxis_type, yaxis_column_name)

elif testNo == 2:
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    styles ={
        'pre' : {
            'border' : 'thin lightgrey solid',
            'overflowX' : 'scroll'
        }
    }

    df = pd.DataFrame({
        "x" : [1, 2, 1, 2],
        "y" : [1, 2, 3, 4],
        "customdata" : [1, 2, 3, 4],
        "fruit" : ["apple", "apple", "orange", "orange"]
    })

    fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
    fig.update_layout(clickmode='event+select')
    fig.update_traces(marker_size=20)

    app.layout = html.Div([
        dcc.Graph(
            id='basic-interactions',
            figure=fig
        ),

        html.Div(className='row', children=[
            html.Div([
                dcc.Markdown("""
                **Hover Data**
                
                Mouse over values in the graph.
                """),
                html.Pre(id='hover-data', style=styles['pre'])
            ],
            className='three columns'),

            html.Div([
                dcc.Markdown("""
                **Click Data**
                
                Click on points in the graph.
                """),
                html.Pre(id='click-data', style=styles['pre'])
            ],
            className='three columns'),

            html.Div([
                dcc.Markdown("""
                **Selection Data**
                
                Choose the lasso or rectangle tool in the graph's menu 
                bar and then select points in the graph.
                
                Note that if `layout.clickmode` = `event+select`, selection
                data also accumulates (or un-accumulate) selected data if you
                hold down the shift button while clicking.
                """),
                html.Pre(id='selected-data', style=styles['pre'])
            ],
            className='three columns'),

            html.Div([
                dcc.Markdown("""
                **Zoom and Relayout Data**
                
                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire this event.
                """),
                html.Pre(id='relayout-data', style=styles['pre'])
            ],
            className='three columns'),
        ])
    ])

    @app.callback(
        Output('hover-data', 'children'),
        Input('basic-interactions', 'hoverData')
    )
    def display_hover_data(hoverData):
        return json.dumps(hoverData, indent=2)

    @app.callback(
        Output('click-data', 'children'),
        Input('basic-interactions', 'clickData')
    )
    def display_click_data(clickData):
        return json.dumps(clickData, indent=2)

    @app.callback(
        Output('selected-data', 'children'),
        Input('basic-interactions', 'selectedData')
    )
    def display_selected_data(selectedData):
        return json.dumps(selectedData, indent=2)

    @app.callback(
        Output('relayout-data', 'children'),
        Input('basic-interactions', 'relayoutData')
    )
    def display_relayout_data(relayoutData):
        return json.dumps(relayoutData, indent=2)

if __name__ == "__main__":
    app.run_server(debug=True)