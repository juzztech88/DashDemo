from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd

'''
 Test no --> Demo concept
 1 --> Simple callback
 2 --> Callbacks with figure and slider
 3 --> Multiple inputs
 4 --> Multiple outputs
 5 --> Chained callback
 6 --> Stately dash app
 7 --> Reference without id
'''
testNo = 7

if testNo == 1:
    app = Dash(__name__)

    app.layout = html.Div([
        html.H6("Change the value in the text box to see callbakcs in action!"),
        html.Div([
            html.Label("Input: "),
            dcc.Input(id='my-input', value='initial value', type='text'),
        ]),
        html.Br(),
        html.Div(id='my-output'),
    ])

    @app.callback(
        Output(component_id='my-output', component_property='children'),
        Input(component_id='my-input', component_property='value')
    )
    def update_output_div(input_value):
        return f"Output: {input_value}"

elif testNo == 2:
    app = Dash(__name__)

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv',
                     )

    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            df['year'].min(),
            df['year'].max(),
            step=None,
            value=df['year'].min(),
            marks={str(year) : str(year) for year in df['year'].unique()},
            id='year-slider'
        )
    ])

    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('year-slider', 'value'))
    def update_figure(selected_year):
        filtered_df = df[df.year == selected_year]

        fig = px.scatter(filtered_df, x='gdpPercap', y='lifeExp',
                         size='pop', color='continent', hover_name='country',
                         log_x=True, size_max=55)
        fig.update_layout(transition_duration=500)
        return fig

elif testNo == 3:
    app = Dash(__name__)

    df = pd.read_csv("https://plotly.github.io/datasets/country_indicators.csv")

    app.layout = html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Fertility rate, total (births per woman)',
                    id='xaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='xaxis-type',
                    inline=True
                )
            ], style={'width' : '48%', 'display' : 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Life expectancy at birth, total (years)',
                    id='yaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='yaxis-type',
                    inline=True
                )
            ], style={'width' : '48%', 'float' : 'right', 'display' : 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic'),

        dcc.Slider(
            df['Year'].min(),
            df['Year'].max(),
            step=None,
            id='year--slider',
            value=df['Year'].max(),
            marks={str(year) : str(year) for year in df['Year'].unique()},
        )
    ])

    @app.callback(
        Output('indicator-graphic', 'figure'),
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value'),
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),
        Input('year--slider', 'value')
    )
    def update_graph(xaxis_column_name, yaxis_column_name,
                     xaxis_type, yaxis_type,
                     year_value):

        dff = df[df['Year'] == year_value]

        fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                         y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                         hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

        fig.update_layout(margin={'l':40, 'b':40, 't':40, 'r':0}, hovermode='closest')

        fig.update_xaxes(title=xaxis_column_name,
                         type='linear' if xaxis_type == 'Linear' else 'log')

        fig.update_yaxes(title=yaxis_column_name,
                         type='linear' if yaxis_type == 'Linear' else 'log')

        return fig

elif testNo == 4:
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        dcc.Input(
            id='num_multi',
            type="number",
            value=5
        ),
        html.Table([
            html.Tr([html.Td(['x', html.Sup(2)]),
                     html.Td(id='square')]),
            html.Tr([html.Td(['x', html.Sup(3)]),
                     html.Td(id='cube')]),
            html.Tr([html.Td([2, html.Sup('x')]),
                     html.Td(id='twos')]),
            html.Tr([html.Td([3, html.Sup('x')]),
                     html.Td(id='threes')]),
            html.Tr([html.Td(['x', html.Sup('x')]),
                     html.Td(id='x^x')]),
        ]),
    ])

    @app.callback(
        Output('square', 'children'),
        Output('cube', 'children'),
        Output('twos', 'children'),
        Output('threes', 'children'),
        Output('x^x', 'children'),
        Input('num_multi', 'value')
    )
    def callback_a(x):
        return x**2, x**3, 2**x, 3**x, x**x

elif testNo == 5:
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = Dash(__name__, external_stylesheets=external_stylesheets)

    all_options = {
        'America' : ['New York City', 'San Francisco', 'Cincinnati'],
        'Canada' : ['Montreal', 'Toronto', 'Ottawa']
    }

    app.layout = html.Div([
        dcc.RadioItems(
            list(all_options.keys()),
            'America',
            id='countries-radio'
        ),

        html.Hr(),

        dcc.RadioItems(id='cities-radio'),

        html.Hr(),

        html.Div(id='display-selected-values'),
    ])

    @app.callback(
        Output('cities-radio', 'options'),
        Input('countries-radio', 'value')
    )
    def set_cities_options(selected_country):
        return [{'label' : i, 'value' : i} for i in all_options[selected_country]]

    @app.callback(
        Output('cities-radio', 'value'),
        Input('cities-radio', 'options')
    )
    def set_cities_value(available_options):
        return available_options[0]['value']

    @app.callback(
        Output('display-selected-values', 'children'),
        Input('countries-radio', 'value'),
        Input('cities-radio', 'value')
    )
    def set_display_children(selected_country, selected_city):
        return u'{} is a city in {}'.format(
            selected_city, selected_country
        )

elif testNo == 6:
    '''
    In form-like application, you want to read the value of an input component only when 
    the user is finished entering all of the information, rather than immediately after 
    it changes.
    '''
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        dcc.Input(id="input-1-state", type="text", value="Montreal"),
        dcc.Input(id="input-2-state", type="text", value="Canada"),
        html.Button(id="submit-button-state", n_clicks=0, children="Submit"),
        html.Div(id="output-state"),
    ])

    @app.callback(
        Output('output-state', 'children'),
        Input('submit-button-state', 'n_clicks'),
        State('input-1-state', 'value'),
        State('input-2-state', 'value')
    )
    def update_output(n_clicks, input1, input2):
        return u'''
            The button has been pressed {} times,
            Input 1 is "{}",
            Input 2 is "{}".
        '''.format(n_clicks, input1, input2)

elif testNo == 7:
    app = Dash(__name__)

    app.layout = html.Div([
        html.H6("Change the value in the text boc to see callbvacks in action!"),
        html.Div([
            "Input: ",
            my_input := dcc.Input(value='initial value', type='text')
        ]),
        html.Br(),
        my_output := html.Div(),
    ])

    @app.callback(
        Output(my_output, component_property='children'),
        Input(my_input, component_property='value')
    )
    def update_output(input_value):
        return f"Output: {input_value}."

if __name__ == '__main__':
    app.run_server(debug=True)