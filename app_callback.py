from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

testNo = 3

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


if __name__ == '__main__':
    app.run_server(debug=True)