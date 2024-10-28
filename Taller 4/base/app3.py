import dash
from dash import dcc  # dash core components 
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
print(df.columns)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.bar(
        filtered_df,
        x="continent",  # Continente en el eje X
        y="lifeExp",  # Expectativa de vida en el eje Y
        color="continent",
        hover_name="country",
        labels={
            "continent": "Continent",
            "lifeExp": "Life Expectancy"
        },
        title=f"Life Expectancy by Continent in {selected_year}"
    )

    fig.update_layout(transition_duration=500)
    return fig

print(df.columns)

if __name__ == '__main__':
    app.run_server(debug=True)
