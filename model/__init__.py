from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, text
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.provider import Provider
from model.activity import Activity
from model.session import Session
from model.provider_activity import ProviderActivity

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco (Session = modelo ORM; não sobrescrever)
SessionLocal = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

# Migração leve: create_all não altera tabelas já existentes (ex.: SQLite antigo sem email)
_insp = inspect(engine)
if _insp.has_table("provider"):
    _provider_cols = {c["name"] for c in _insp.get_columns("provider")}
    if "email" not in _provider_cols:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE provider ADD COLUMN email VARCHAR(255)"))
