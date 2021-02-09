import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from intro import process


app = dash.Dash(
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

app.title = 'Suicide Data'

suicides = process()

grouped_by_gender = suicides.groupby(['year', 'sex'], as_index=False)['suicides/100k'].sum()
grouped_by_gdp = suicides.groupby(['gdp_per_capita'], as_index=False)['suicides/100k'].sum()
grouped_by_year_age = suicides.groupby(['year', 'age'], as_index=False)['suicides/100k'].sum()
grouped_by_generation = suicides.groupby(['year', 'generation'], as_index=False)['suicides/100k'].sum()
grouped_by_continent = suicides.groupby(['continent'], as_index=False)['suicides/100k'].sum()
max_country_per_year = suicides[suicides['suicides/100k'] == suicides.groupby('year')['suicides/100k'].transform('max')]

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1("DASHBOARD - SUICIDES OVERVIEW"),
            ],
            style={
                'textAlign': 'center',
                'color': '#456FBV'
            }
        ),
        dcc.Tabs([
            dcc.Tab(label='WORLDWIDE SCALE', children=[
                html.Div(className='row',
                         children=[
                             html.Div(
                                 dcc.Graph(
                                     id='table-data',
                                     figure=go.Figure(data=[go.Table(
                                         header=dict(values=['Country', 'Year', 'Sex', 'Age', 'Population', 'Suicides/100k',
                                                             'Generation', 'GDP per capita', 'Continent'],
                                                     align='left'),
                                         cells=dict(values=[suicides.country, suicides.year, suicides.sex, suicides.age,
                                                            suicides.population, suicides['suicides/100k'],
                                                            suicides.generation, suicides.gdp_per_capita, suicides.continent],
                                                    align='left'))
                                     ])),
                                 className='ten columns')
                         ]),
                html.Div(className='row',
                         children=[
                             html.Div(
                                 dcc.Graph(
                                     id='pie-chart-continent',
                                     figure = go.Figure(data=[go.Pie(labels=grouped_by_continent['continent'], values=grouped_by_continent['suicides/100k'],
                                                                     textposition='inside')])
                                 ), className='six columns'
                             ),
                             html.Div(
                                 dcc.Graph(
                                     id='gender-graph',
                                     figure=px.bar(grouped_by_gender, x='year', y='suicides/100k', color='sex')
                                 ), className='six columns'
                             )
                         ]),
                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            dcc.Graph(
                                id='age-graph',
                                figure=px.line(grouped_by_year_age, x='year', y='suicides/100k', color='age')
                            ), className='six columns'
                        ),

                        html.Div(
                            dcc.Graph(
                                id='generation-graph',
                                figure=px.line(grouped_by_generation, x='year', y='suicides/100k', color='generation')
                            ), className='six columns'
                        )
                    ]
                ),
                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            dcc.Graph(
                                id='max-country-per-year',
                                figure=px.scatter(max_country_per_year, y='suicides/100k', x='country', color='year')
                            ), className='seven columns'
                        ),
                        html.Div(
                            dcc.Graph(
                                id='gdp-graph',
                                figure=px.histogram(suicides, x='gdp_per_capita', y='suicides/100k',
                                                    labels={'x': 'gdp_per_capita', 'y': 'suicides/100k'})
                            ), className='five columns'
                        ),

                    ]
                ),
            ]),
            dcc.Tab(label='CONTINENTAL SCALE', children=[
                html.Div(className='row',
                         children=[
                             html.Div(
                                 html.Div(
                                     dcc.Dropdown(
                                         id='multi-drop-down',
                                         options=[{'label': i, 'value': i} for i in suicides['continent'].unique()],
                                         value=['Europe'],
                                         placeholder="Select a continent",
                                         multi=True
                                     ),
                                     className='six columns'
                                 ),
                                 className='row'
                             ),
                             html.Div(
                                 dcc.Slider(
                                     id='year-slider',
                                     min=suicides['year'].min(),
                                     max=suicides['year'].max(),
                                     value=suicides['year'].min(),
                                     marks={str(year): str(year) for year in suicides['year'].unique()},
                                     step=None
                                 )
                             ),
                             html.Div(
                                 className='row',
                                 children=[
                                     html.Div(
                                         dcc.Graph(id='scatter-plot-gdp'),
                                         className='six columns'
                                     ),
                                     html.Div(
                                         dcc.Graph(id='scatter-plot-ages'),
                                         className='six columns'
                                     )
                                 ],
                             ),
                             html.Div(
                                 className='row',
                                 children=[
                                     html.Div(
                                         dcc.Graph(id='max-year-per-country'),
                                         className='eight columns'
                                     )
                                 ]),
                         ]),
            ])
        ]),
    ],
)


@app.callback(
    Output('scatter-plot-gdp', 'figure'),
    [Input('year-slider', 'value'),
     Input('multi-drop-down', 'value')])
def update_figure(selected_year, selected_continent):
    filtered_master = suicides[suicides.year == selected_year]

    filtered_master = filtered_master[filtered_master['continent'].isin(selected_continent)]

    fig = px.scatter(filtered_master, x='gdp_per_capita',
                     y='suicides/100k',
                     color='continent',
                     hover_name='country')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 10}, hovermode='closest')

    return fig


@app.callback(
    Output('scatter-plot-ages', 'figure'),
    [Input('year-slider', 'value'),
     Input('multi-drop-down', 'value')])
def update_scatter_ages(selected_year, selected_continent):
    filtered_master = suicides[suicides.year == selected_year]

    filtered_master = filtered_master[filtered_master['continent'].isin(selected_continent)]

    fig = px.scatter(filtered_master, x='age',
                     y='suicides/100k',
                     color='continent',
                     hover_name='country')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 10}, hovermode='closest')

    return fig


@app.callback(
    Output('max-year-per-country', 'figure'),
    [Input('multi-drop-down', 'value')]
)
def update_chart(selected_continent):
    df = suicides[suicides.continent.isin(selected_continent)]
    max_year_per_country = df[df['suicides/100k'] == df.groupby('country')['suicides/100k'].transform('max')]
    fig = px.bar(max_year_per_country, y='suicides/100k', x='year', color='country')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
