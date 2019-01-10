from flask import Flask, render_template
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from src.config import Config, DevelopmentConfig
from src.models.despesas.despesa import Despesas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

manager = APIManager(flask_sqlalchemy_db=db)
manager.init_app(app)
manager.create_api(Despesas, app=app, results_per_page=2500)

@app.route('/')
def home():
    despesas = Despesas.query.filter().limit(100).all()
    return render_template('home.html', despesas=despesas)

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
    return render_template('dashboards/despesa_funcao.html', despesas=despesas)

if __name__ == "__main__":
    app.run(debug=DevelopmentConfig.DEBUG)
