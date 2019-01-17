import dash as dash
from flask import Flask, render_template
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from src.config import Config, DevelopmentConfig
from src.models.despesas.despesa import Despesas
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_sql_query("""
    SELECT ds_funcao_governo, sum(cast(replace(vl_despesa,',','.') as float)) vl_despesa
    FROM despesas
    WHERE ds_municipio = 'Sertгozinho' AND
           mes_referencia = '4'
    GROUP BY ds_funcao_governo
    """, con=engine)

app_dash = dash.Dash(__name__, server=app, external_stylesheets=external_stylesheets)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app_dash.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

    html.Div(children=[
        html.H4(children='US Agriculture Exports (2011)'),
        generate_table(df)
    ])
])

manager = APIManager(flask_sqlalchemy_db=db)
manager.init_app(app)
manager.create_api(Despesas, app=app, results_per_page=2500)


@app.route('/')
def home():
    print("home")
    despesas = Despesas.query.filter().limit(100).all()
    return render_template('home.html', despesas=despesas)


@app.route('/dash')
def dash():
    print("dash")
    return app_dash


@app.route('/despesas_funcao')
def despesas_funcao():
    sql_command = """
    SELECT ds_funcao_governo, sum(cast(replace(vl_despesa,',','.') as float)) vl_despesa
    FROM despesas
    WHERE ds_municipio = 'Sertгozinho' AND
           mes_referencia = '4'
    GROUP BY ds_funcao_governo
    """
    despesas = db.engine.execute(sql_command)


    d, despesas_list = {}, []
    for row in despesas:
        for column in row.items():
            d = {**d, **{column[0]: column[1]}}
        despesas_list.append(d)

    return render_template('dashboards/despesa_funcao.html', despesas=despesas_list)


if __name__ == "__main__":
    app.run(debug=True)
