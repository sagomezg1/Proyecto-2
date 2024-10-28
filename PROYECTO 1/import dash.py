import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import base64

# Cargar los datos desde el archivo CSV
df = pd.read_csv('SeoulBikeData_utf8.csv')

# Transformaciones de los datos
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Holiday'] = df['Holiday'].map({'No Holiday': 0, 'Holiday': 1})
df['Functioning Day'] = df['Functioning Day'].map({'Yes': 1, 'No': 0})
df = pd.get_dummies(df, columns=['Seasons'], drop_first=True)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Layout del tablero
app.layout = html.Div(children=[
    html.H1(children='Tablero de Bicicletas Compartidas'),

    html.Div([
        html.Label('Seleccione la Hora del Día:'),
        dcc.Slider(id='input_hour', min=0, max=23, step=1, value=12,
                   marks={i: f'{i}:00' for i in range(0, 24)}),

        html.Label('Seleccione la Temperatura (°C):'),
        dcc.Slider(id='input_temp', min=-10, max=35, step=1, value=20,
                   marks={i: f'{i}°C' for i in range(-10, 36, 5)}),

        html.Label('Seleccione la Humedad (%):'),
        dcc.Slider(id='input_humidity', min=0, max=100, step=1, value=50,
                   marks={i: f'{i}%' for i in range(0, 101, 10)}),

        html.Label('Velocidad del viento (m/s):'),
        dcc.Slider(id='input_wind', min=0, max=10, step=0.5, value=5,
                   marks={i: f'{i} m/s' for i in range(0, 11)}),

        html.Label('¿Es un día festivo?:'),
        dcc.Dropdown(id='input_holiday', options=[{'label': 'Sí', 'value': 1}, {'label': 'No', 'value': 0}],
                     value=0),

        html.Label('¿Es un día hábil?:'),
        dcc.Dropdown(id='input_functioning_day', options=[{'label': 'Sí', 'value': 1}, {'label': 'No', 'value': 0}],
                     value=1)
    ], style={'padding': 20, 'width': '50%'}),

    html.H2('Visualización de datos:'),
    dcc.Graph(id='output_graph'),

    # Botones para mostrar los gráficos adicionales
    html.Div([
        html.Button('Mostrar gráficos estáticos', id='show_static_graphs', n_clicks=0),
        html.Button('Mostrar gráficos movibles', id='show_movable_graphs', n_clicks=0)
    ], style={'padding': 20}),

    html.Div(id='static_graphs_container'),
    html.Div(id='movable_graphs_container')
])

# Callback para actualizar el gráfico
@app.callback(
    Output('output_graph', 'figure'),
    [Input('input_hour', 'value'),
     Input('input_temp', 'value'),
     Input('input_humidity', 'value'),
     Input('input_wind', 'value')]
)
def update_graph(hour, temp, humidity, wind):
    # Crear gráfico de barras para visualización de la demanda por hora
    filtered_df = df[(df['Temperature(C)'] == temp) & (df['Humidity(%)'] == humidity)]
    fig = px.bar(filtered_df, x='Hour', y='Rented Bike Count', title='Bicicletas alquiladas por hora')

    return fig

# Callback para mostrar los gráficos estáticos
@app.callback(
    Output('static_graphs_container', 'children'),
    [Input('show_static_graphs', 'n_clicks')]
)
def show_static_graphs(n_clicks):
    if n_clicks > 0:
        # Rutas de las imágenes
        image_filenames = [
            'static/1.png',  # Imagen 1
            'static/2.png',          # Imagen 2
            'static/3.png',          # Imagen 3
            'static/4.png',          # Imagen 4

        ]

        # Codificar imágenes en base64
        images_encoded = [
            base64.b64encode(open(filename, 'rb').read()).decode('ascii')
            for filename in image_filenames
        ]

        # Crear lista de imágenes en HTML
        images_html = [html.Img(src='data:image/png;base64,{}'.format(encoded_image)) for encoded_image in images_encoded]

        return html.Div([
            html.H3('Gráficos Estáticos de Costos e Ingresos'),
            *images_html  # Agregar todas las imágenes
        ])
    return ''

# Callback para mostrar los gráficos movibles
@app.callback(
    Output('movable_graphs_container', 'children'),
    [Input('show_movable_graphs', 'n_clicks')]
)
def show_movable_graphs(n_clicks):
    if n_clicks > 0:
        # Crear gráficos adicionales
        # Boxplot
        fig1 = px.box(df, x='Holiday', y='Rented Bike Count',
                      title='Diagrama de Caja: Bicicletas Alquiladas en Días Festivos vs No Festivos')

        # Gráfico de barras por estaciones
        seasons_df = df[['Seasons_Winter', 'Seasons_Spring', 'Seasons_Summer']].mean()
        fig2 = go.Figure(data=[go.Bar(x=seasons_df.index, y=seasons_df.values,
                                      marker_color='lightblue')])
        fig2.update_layout(title='Promedio de Bicicletas Alquiladas por Estación',
                           xaxis_title='Estación', yaxis_title='Promedio de Bicicletas Alquiladas')

        # Heatmap
        pivot_table = df.pivot_table(values='Rented Bike Count', index='Hour', columns='Temperature(C)', aggfunc='mean')
        fig3 = go.Figure(data=go.Heatmap(z=pivot_table.values, x=pivot_table.columns, y=pivot_table.index,
                                         colorscale='Viridis'))
        fig3.update_layout(title='Mapa de Calor: Bicicletas Alquiladas según Hora y Temperatura',
                           xaxis_title='Temperatura (C)', yaxis_title='Hora del Día')

        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3)
        ])
    return ''

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)
    