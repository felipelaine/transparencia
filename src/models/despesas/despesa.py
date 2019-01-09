from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Despesas(db.Model):
    id_despesa_detalhe = db.Column(db.Text, primary_key=True)
    ano_exercicio = db.Column(db.Text)
    ds_municipio = db.Column(db.Text)
    ds_orgao = db.Column(db.Text)
    mes_referencia = db.Column(db.Text)
    mes_ref_extenso = db.Column(db.Text)
    tp_despesa = db.Column(db.Text)
    nr_empenho = db.Column(db.Text)
    identificador_despesa = db.Column(db.Text)
    ds_despesa = db.Column(db.Text)
    dt_emissao_despesa = db.Column(db.Text)
    vl_despesa = db.Column(db.Text)
    ds_funcao_governo = db.Column(db.Text)
    ds_subfuncao_governo = db.Column(db.Text)
    cd_programa = db.Column(db.Text)
    ds_programa = db.Column(db.Text)
    cd_acao = db.Column(db.Text)
    ds_acao = db.Column(db.Text)
    ds_fonte_recurso = db.Column(db.Text)
    ds_cd_aplicacao_fixo = db.Column(db.Text)
    ds_modalidade_lic = db.Column(db.Text)
    ds_elemento = db.Column(db.Text)
    historico_despesa = db.Column(db.Text)

class DespesasSchema(ma.ModelSchema):
    class Meta:
        model = Despesas
