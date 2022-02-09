# Run this app with `python app_layout.py` and
# visit http://127.0.0.1:8050/ in your web browser

'''
1.  The layout is composed of a tree of components.
2.  The Dash HTML Components module has a component for every HTML tag.
3.  Not all components are pure HTML. The Dash Core Components module (dasd.dcc) containes higher-level
    components that are interactive and are generated with JavaScript, HTML and CSS through the React.js library.
4.  The children property is special. By convention, it's always the first attribute which means that you can
    omit it. It can contain a string, a number, a single component or a list of components.
5.  Dash includes "hot-reloading" automatically refresh your browser when you make changes to your code.
    USe `app.run_server(dev_tools_hot_reload=False) to turn off hot-reloading.

'''
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

test = "dcc"
if test == "simple":
    app = Dash(__name__)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    df = pd.DataFrame({
        "Fruit" : ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount" : [10, 1, 2, 2, 4, 5],
        "City" : ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div(
        children = [
            html.H1(children = 'My first Demo Dash!'),
            html.Div(children = '''
                Dash: A web application framework for your data
            '''),
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ]
    )

elif test == "styling":
    app = Dash(__name__)

    colors = {
        'background'    :   '#111111',
        'text'          :   '#7FDBFF',
    }

    # assume you have a "long-form" data frame
    df = pd.DataFrame({
        'Fruits' : ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
        'Amount' : [8,2, 4, 5, 3, 6],
        'City' : ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    })

    # create a figure with plotly
    fig = px.bar(df, x='Fruits', y='Amount', color='City', barmode='group')

    # customize figure style
    fig.update_layout(
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font_color = colors['text']
    )

    # define layout of your dash application
    app.layout = html.Div(
        style = {
            'backgroundColor' : colors['background']
        },
        children = [
            html.H1(
                children = 'My first Dash application!',
                style = {
                    'textAlign' : 'center',
                    'color' : colors['text'],
                    'fontFamily' : 'Verdana, sans-serif'
                }
            ),

            html.Div(
                children = 'The style is even customised!',
                style = {
                    'textAlign' : 'center',
                    'color' : colors['text'],
                    'fontFamily' : 'Verdana, sans-serif'
                }
            ),

            dcc.Graph(
                id = 'example-graph-2',
                figure = fig
            ),
        ]
    )

elif test == "reusable":
    df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv',
                     index_col=[0])
    app = Dash(__name__)
    app.layout = html.Div([
        html.H4(children='US Agriculture Exports (2011)'),
        generate_table(df)
    ])

elif test == "graph":
    app = Dash(__name__)

    df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv',
                     index_col=[0])
    fig  = px.scatter(df, x="gdp per capita", y="life expectancy",
                      size="population", color="continent", hover_name="country",
                      log_x=True, size_max=60)

    app.layout = html.Div([
        generate_table(df, max_rows=20),
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure=fig
        )
    ])

elif test == "markdown":
    app = Dash(__name__)

    markdown_text = '''
    ### Dash and Markdown
    
    Dash apps can be written in Markdown.
    Dash uses the [CommonMark](http://commonmark.org/)
    specification of Markdown.
    Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
    if this is your first introduction to Markdown!
       
    '''
    app.layout = html.Div([
        dcc.Markdown(children=markdown_text)
    ])

elif test == 'dcc':
    app = Dash(__name__)

    app.layout = html.Div([
        html.Div(children=[
            html.Label('Dropdown'),
            dcc.Dropdown(['New York City', 'Montreal', 'San Francisco'], 'Montreal'),

            html.Br(),
            html.Label('Multi-Select Dropdown'),
            dcc.Dropdown(['New York City', 'Montreal', 'San Francisco'],
                         ['Montreal', 'San Francisco'],
                         multi=True),

            html.Br(),
            html.Label('Radio Items'),
            dcc.RadioItems(['New York City', 'Montreal', 'San Francisco'], 'Montreal'),
        ], style={'padding' : 10, 'flex' : 1}),

        html.Div(children=[
            html.Label('Checkboxes'),
            dcc.Checklist(['New York City', 'Montreal', 'San Francisco'],
                          ['Montreal', 'San Francisco']),

            html.Br(),
            html.Label('Text Input'),
            dcc.Input(value='MTL', type='text'),

            html.Br(),
            html.Label('Slider'),
            dcc.Slider(
                min=0,
                max=9,
                marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1,6)},
                value=5
            ),
        ], style={'padding' : 10, 'flex' : 1})
    ],style={'display' : 'flex', 'flex-direction' : 'row'})

if __name__ == '__main__':
    app.run_server(debug=True)