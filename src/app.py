import dash as dash
from flask import Flask, render_template
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from src.config import Config, DevelopmentConfig
from src.models.despesas.despesa import Despesas
import dash_core_components as dcc
import dash_html_components as html

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

app_dash = dash.Dash(__name__, server=app)
app_dash.config.requests_pathname_prefix = ''

app_dash.layout = html.Div([
    html.H1('Dash application'),
    dcc.Graph(
        id='basic-graph',
        figure={
            'data':[
                {
                    'x': [0, 1],
                    'y': [0, 1],
                    'type': 'line'
                }
            ],
            'layout': {
                'title': 'Basic Graph'
            }
        }
    )
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
    app.run(debug=DevelopmentConfig.DEBUG)
