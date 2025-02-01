from fileinput import filename

from flask import Flask, render_template, request, url_for
import joblib
import numpy as np
import dash
from dash import dcc, html, Dash
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from holoviews.operation import method

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route ('/selectPlayerSkills', methods = ['POST'])
def selectSkills():
    return render_template('playerSkills.html')


@app.route('/prediction',methods=('GET', 'POST'))
def prediction():
    output= 'NONE'
    if request.method == 'POST':
        shooting = int(request.form['shooting'])
        tackling = int(request.form['tackling'])
        crossing = int(request.form['crossing'])
        intercepting = int(request.form['intercepting'])
        aggressive = int(request.form['aggressive'])
        impulse = int(request.form['impulse'])
        assisting = int(request.form['assisting'])
        power = int(request.form['power'])
        height = int(request.form['height'])
        print(shooting,tackling,crossing,intercepting,aggressive,impulse,assisting,power,height)
        input=np.array([[height,shooting,aggressive,impulse,crossing,assisting,tackling,intercepting,power]])
        model=joblib.load('FinalModel.sav')
        scaler=joblib.load('scaler.sav')
        input=scaler.transform(input)
        print(model.get_booster().feature_names)
        prediction=model.predict(input)
        if prediction == 0:
            output='Forward'
        if prediction == 1:
            output='Midfielder'
        if prediction == 2:
            output = 'Defender'

    return render_template('prediction.html',output=output)

def createDashApp(flask_server):
    dashApp = Dash(server = flask_server , url_base_pathname= '/playersDashboard/')
    def read_data_country_selection(country):
        df = pd.read_csv('..\\ML Model\\finalData\\data_for_EDA.csv')
        if len(country) == 0:
            return df
        return df[df['country'] == country]

    # Define the layout of the app
    df = read_data_country_selection('')
    countries = df['country'].value_counts().index
    dashApp.layout = (
        html.Div(id = 'full-page', children=[
            html.Link(
            rel='stylesheet',
            href='/static/css/custom.css'
             ),
            html.Link(rel='icon',href = 'static\img\icon.png'),
            html.H1("Players' skills analysis dashboard"),
            # Dropdown to select a dataset
            dcc.Dropdown(
                id='data-dropdown',
                options=
                countries,
                value='Brazil '  # Default value
            )
            ,
            html.Div(id='Numbers-Div', children=([
                html.Div([
                    # Paragraph to display selected dataset
                    html.P(id='display-ratio-of-players')
                ]),
                html.Div([
                    # Paragraph to display selected dataset
                    html.P(id='display-number-of-players')
                ])
            ]), style={'display': 'flex', 'justify-items': 'space-between'})
            ,
            html.Div(children=([
                dcc.Dropdown(
                    id='skill-dropdown',
                    value='shooting',
                    options=['shooting', 'crossing', 'assisting', 'tackling', 'intercepting']
                )
            ]),

            ),
            html.Div(id='interactive-graphs-row1', children=([
                dcc.Graph(id='Map-Graph'),
                dcc.Graph(id='line-graph')
            ]), style={'display': 'grid', 'gridTemplateColumns': '1.5fr 1fr', 'gap': '5px', 'padding-bottom': '5px'}
                     ),

            html.Div(id='interactive-graphs-row2', children=([
                html.Div(id='dropdown-position', children=([
                    dcc.Dropdown(
                        id='position-dropdown',
                        options=
                        ['DF', 'FW', 'MF'],
                        value='FW'  # Default value
                    ),
                    dcc.Graph(id='table-graph', style={'width': '100%'})
                ])),
                dcc.Graph(id='pie-plot'),
                dcc.Graph(id='barchart-graph')
            ]), style={'display': 'grid', 'gridTemplateColumns': '0.90fr 0.6fr 0.7fr', 'gap': '5px'}
                     ),
            html.Div([
                # Paragraph to display selected dataset
                html.P(id='display-selected-value')
            ], style={'width': '100%'}
            )
        ]))

    def position_skills(position):
        if position == 'FW':
            return ['shooting', 'assisting',
                    # 'crossing'
                    ]
        if position == 'MF':
            return ['assisting', 'tackling',
                    # 'intercepting',
                    'crossing'
                    ]
        if position == 'DF':
            return ['intercepting', 'power'
                    # ,'impulse_degree'
                    ]

    def read_table_data(df, position):
        data = df[df['position'] == position]
        player_info_list = ['minutes', 'name', 'month', 'height', 'weight']
        player_info_list.extend(position_skills(position))
        return pd.DataFrame(data[player_info_list]).sort_values(by=position_skills(position),
                                                                ascending=[False] * len(position_skills(position)))[:10]

    def players_numerical_info(df):
        number_of_players = df['position'].size
        all_df = read_data_country_selection('')
        ratio_of_players = df['position'].size / all_df['position'].size * 100
        return number_of_players, ratio_of_players

    def read_data_bar_chart(df):
        barChart_data = df[
            ['shooting', 'crossing', 'assisting', 'tackling', 'intercepting']]
        barChart_data_x = barChart_data.columns
        barChart_data_y = barChart_data.mean()
        return barChart_data_x, barChart_data_y

    # Callback to update the graph and the paragraph based on the dropdown selection
    def read_player_skill(df, selected_skill, key):
        if selected_skill in ['shooting', 'assisting', 'crossing']:
            return df[(df['position'] == 'FW') | (df['position'] == 'MF')][[selected_skill, key]]
        elif selected_skill in ['crossing', 'tackling', 'intercepting']:
            return df[(df['position'] == 'MF') | (df['position'] == 'DF')][[selected_skill, key]]

    def read_map_data(df, selected_skill):
        df = read_player_skill(df, selected_skill, 'country')
        data_list = list()
        for i in df['country'].value_counts().index:
            data_list.append((i, df[df['country'] == i][selected_skill].median()))
        return pd.DataFrame(data_list, columns=['country', 'avg_skill_ratio'])

    def decade_match(category):
        if category == 5:
            return 2000
        elif category == 4:
            return 1990
        elif category == 3:
            return 1980
        elif category == 2:
            return 1970
        else:
            return 1960

    def handle_decade_data(df):
        df['year'] = df['year'].apply(decade_match)

    def handle_skills_data(skills_df, skill):
        skills_Avg_per_decade = list()
        for i in skills_df['year'].value_counts(sort=False).index:
            skills_Avg_per_decade.append((i, skills_df[skills_df['year'] == i][skill].median()))
        skills_Avg_per_decade.sort(key=lambda x: x[0])
        x_axis = [lst[0] for lst in skills_Avg_per_decade]
        y_axis = [lst[1] for lst in skills_Avg_per_decade]

        return x_axis, y_axis

    @dashApp.callback(
        [Output('pie-plot', 'figure'),
         Output('barchart-graph', 'figure'),
         Output('table-graph', 'figure'),
         Output('line-graph', 'figure'),
         Output('Map-Graph', 'figure'),
         Output('display-number-of-players', 'children'),
         Output('display-ratio-of-players', 'children'),
         ],
        [Input('data-dropdown', 'value'),
         Input('position-dropdown', 'value'),
         Input('skill-dropdown', 'value'),
         ]
    )
    def update_graph(selected_dataset, selected_position, selected_skill):
        # Define the datasets
        df = read_data_country_selection('')
        map_data = read_map_data(df, selected_skill)
        df = read_data_country_selection(selected_dataset)
        skills_df = read_player_skill(df, selected_skill, 'year')
        handle_decade_data(skills_df)
        x_axis_line_graph, y_axis_line_graph = handle_skills_data(skills_df, selected_skill)

        table_data = read_table_data(df, selected_position)
        hover_text = [
            [f'{col} : {val}' for val in table_data[col]]
            for col in table_data.columns
        ]
        table_trace = go.Table(
            header=dict(values=list(table_data.columns),
                        fill_color='rgb(25, 25, 51)',
                        font=dict(color='white', size=14)
                        ),
            cells=dict(values=[table_data[col] for col in table_data.columns],
                       fill_color='rgb(44, 42, 87)',
                       font=dict(color='white', size=14)
                       )
        )
        barChart_data_x, barChart_data_y = read_data_bar_chart(df)
        piePlot_data = [
            go.Pie(labels=list(df['position'].value_counts().index), values=list(df['position'].value_counts().values))]
        number_of_players, ratio_of_players = players_numerical_info(df)
        layout = layout = go.Layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Dark background for plot
            paper_bgcolor='rgba(0,0,0,0)',  # Dark background for paper
            font=dict(color='black'),  # font color for titles and labels
            xaxis=dict(showgrid=True, gridcolor='#444444', zerolinecolor='#444444'),  # Gridline colors
            yaxis=dict(showgrid=True, gridcolor='#444444', zerolinecolor='#444444'),
        )
        pie_fig = go.Figure(data=piePlot_data, layout=layout)
        pie_fig.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20,
                              marker=dict(colors=px.colors.sequential.ice, line=dict(color='#000000', width=2)))
        pie_fig.update_layout(title=f"Number of players for each position")
        bar_fig = go.Figure(data=[
            go.Bar(x=barChart_data_x, y=barChart_data_y,
                   marker_color=px.colors.sequential.ice)],
            layout=layout)
        bar_fig.update_layout(title_text=f"Average skills {selected_dataset} developing the most",
                              margin=dict(l=0, r=0, b=40, t=50))
        table_fig = {'data': [table_trace],
                     'layout': {
                         'title': f'best players in {selected_dataset} as {selected_position}',
                         'title_color': 'black',
                         'height': '400',
                         'width': '520',
                         'paper_bgcolor': 'rgba(0,0,0,0)',
                         'font': dict(color='black'),
                         'autosize': True,  # Allow auto-sizing to make it responsive
                         'margin': dict(l=0, r=0, b=0, t=40)
                     }
                     }
        line_fig = px.line(x=x_axis_line_graph, y=y_axis_line_graph, color_discrete_sequence=["#030512"])
        line_fig.update_layout(title=f'skill development over the years in {selected_dataset}',
                               plot_bgcolor='rgba(0,0,0,0)',
                               paper_bgcolor='rgba(0,0,0,0)',
                               font=dict(color='black'),
                               xaxis=dict(showgrid=True, gridcolor='white', zerolinecolor='#030512', title='year'),
                               # Gridline colors
                               yaxis=dict(showgrid=True, gridcolor='white', zerolinecolor='#030512',
                                          title='average skill ratio'),
                               )
        # Create a choropleth map using Plotly Express
        map_fig = px.choropleth(
            map_data,
            locations='country',  # The column with country names
            locationmode='country names',  # Match the country names with Plotly's built-in mapping
            color='avg_skill_ratio',  # The color will be based on the selected skill (e.g., 'Avg_Skill')
            hover_name='avg_skill_ratio',  # Display country names on hover
            color_continuous_scale='Viridis',  # Color scale for the heatmap effect
            projection='natural earth',  # Map projection type
            title='Players\' skills ratio',
        )
        map_fig.update_layout(
            paper_bgcolor='rgb(0,0,0,0)',
            plot_bgcolor='rgb(0,0,0,0)',
            geo=dict(
                showframe=False,  # Remove the frame around the map
                showcoastlines=True,  # Show coastlines
                projection_type='natural earth'  # Keep a natural earth projection
            ),
            autosize=True,
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            font=dict(color='black')
        )
        return pie_fig, bar_fig, table_fig, line_fig, map_fig, f"Total number of players is {number_of_players}", f"Ration of players is {round(ratio_of_players, 1)}%"
    return dashApp

dashApp = createDashApp(app)
