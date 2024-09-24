from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Integracao(Base):
    __tablename__ = 'integracao'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    forma_pagamento = Column(String)
    conta_contabil = Column(String)
    conta_contabil_contra_partida = Column(String)
    empresa = Column(String)
    cliente_tarifa = Column(String)
    cliente_frete = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Store the hashed password