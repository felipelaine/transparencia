from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.config import Config, DevelopmentConfig
from src.models.despesas.despesa import DespesasSchema, Despesas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

despesas_schema = DespesasSchema(many=True)

@app.route('/')
def home():
    return "Hello, world!"

@app.route('/despesas')
def get_despesas():
    #despesas = db.engine.execute('select * from despesas limit 1000')
    despesas = Despesas.query.filter().limit(1000).all()
    output = despesas_schema.dump(despesas).data
    return jsonify({'despesas': output})

@app.route('/despesas_teste')
def get_despesas_teste():
    #despesas = db.engine.execute('select * from despesas limit 1000')
    despesas = Despesas.query.filter().limit(1000).all()

    output = []

    for despesa in despesas:
        despesa_data = {}
        despesa_data['id_despesa_detalhe'] = despesa.id_despesa_detalhe
        despesa_data['ano_exercicio'] = despesa.ano_exercicio
        despesa_data['ds_municipio'] = despesa.ds_municipio
        despesa_data['ds_orgao'] = despesa.ds_orgao
        despesa_data['mes_referencia'] = despesa.mes_referencia
        despesa_data['mes_ref_extenso'] = despesa.mes_ref_extenso
        despesa_data['identificador_despesa'] = despesa.identificador_despesa
        despesa_data['ds_despesa'] = despesa.ds_despesa
        despesa_data['dt_emissao_despesa'] = despesa.dt_emissao_despesa
        despesa_data['vl_despesa'] = despesa.vl_despesa
        despesa_data['ds_funcao_governo'] = despesa.ds_funcao_governo
        despesa_data['ds_subfuncao_governo'] = despesa.ds_subfuncao_governo
        despesa_data['cd_programa'] = despesa.cd_programa
        despesa_data['ds_programa'] = despesa.ds_programa
        despesa_data['cd_acao'] = despesa.cd_acao
        despesa_data['ds_acao'] = despesa.ds_acao
        despesa_data['ds_fonte_recurso'] = despesa.ds_fonte_recurso
        despesa_data['ds_cd_aplicacao_fixo'] = despesa.ds_cd_aplicacao_fixo
        despesa_data['ds_modalidade_lic'] = despesa.ds_modalidade_lic
        despesa_data['ds_elemento'] = despesa.ds_elemento
        despesa_data['historico_despesa'] = despesa.historico_despesa

        output.append(despesa_data)

    return jsonify({'despesas': output})


if __name__ == "__main__":
    app.run(debug=DevelopmentConfig.DEBUG)
