from fastapi import FastAPI, HTTPException, Depends
import os
from sqlalchemy.orm import Session

from auth import create_jwt_token
from constantes import FRETE, TARIFA
from database import database, schemas
from database.schemas import IntegracaoSchema, LoginSchema
from models import models
from services.importador import ImportadorIntegracao
from pydantic import BaseModel



# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

from services.integracao_integrin import IntegracaoIntegrin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.post("/read_file")
async def read_file_from_base64(data: dict):
    try:
        arquivo = data.get('file')[0]
        file_name = arquivo.get('fileName')
        base64_data = arquivo.get('base64')
        file_type = os.path.splitext(file_name)[1].lower()
        origem = data.get('origem')

        if file_type not in ['.xlsx', '.csv', '.xls']:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only 'xlsx', 'csv' and 'xls' are supported.")

        importador = ImportadorIntegracao(origem)
        file_data = importador.import_file_from_base64(file_name, file_type, base64_data)

        if not file_data:
            return None

        integrador = IntegracaoIntegrin()
        baixas_reliazadas, baixas_erros = integrador.baixar_titulos_ecommerce(file_data)

        frete = integrador.lancar_valor_frete_importacao(file_data, FRETE)
        tarifa = integrador.lancar_valor_frete_importacao(file_data, TARIFA)

        return {
            'baixas_realizadas': baixas_reliazadas,
            'baixas_erros': baixas_erros,
            'frete': frete,
            'tarifa': tarifa
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to read file. Error: " + str(e))



# Define a request body model
class ParametrosIntegracaoRequestBody(BaseModel):
    name: str
    forma_pagamento: str
    conta_contabil: str
    conta_contabil_contra_partida: str
    empresa: str
    cliente_tarifa: str
    cliente_frete: str

@app.post("/integracao", response_model=schemas.IntegracaoSchema)
def create_or_update_integracao(
    integracao: ParametrosIntegracaoRequestBody,
    db: Session = Depends(get_db)
):
    # Check if an Integracao record already exists
    existing_integracao = db.query(models.Integracao).first()

    if existing_integracao:
        # Update the existing record
        existing_integracao.name = integracao.name
        existing_integracao.forma_pagamento = integracao.forma_pagamento
        existing_integracao.conta_contabil = integracao.conta_contabil
        existing_integracao.conta_contabil_contra_partida = integracao.conta_contabil_contra_partida
        existing_integracao.empresa = integracao.empresa
        existing_integracao.cliente_tarifa = integracao.cliente_tarifa
        existing_integracao.cliente_frete = integracao.cliente_frete
        db.commit()
        db.refresh(existing_integracao)
        return existing_integracao
    else:
        # Create a new record
        new_integracao = models.Integracao(
            name=integracao.name,
            forma_pagamento=integracao.forma_pagamento,
            conta_contabil=integracao.conta_contabil,
            conta_contabil_contra_partida=integracao.conta_contabil_contra_partida,
            empresa=integracao.empresa,
            cliente_tarifa=integracao.cliente_tarifa,
            cliente_frete=integracao.cliente_frete
        )
        db.add(new_integracao)
        db.commit()
        db.refresh(new_integracao)
        return new_integracao

@app.get("/integracao", response_model=schemas.IntegracaoSchema)
def read_integracao(db: Session = Depends(get_db)):
    integracao = db.query(models.Integracao).first()
    if integracao:
        return integracao
    else:
        raise HTTPException(status_code=404, detail="Integracao not found")


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password (for demo purposes, you can use a proper hashing library like bcrypt)
    hashed_password = user.password  # Replace with hash logic
    new_user = models.User(name=user.name, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a token (for example, using JWT)
    token = create_jwt_token({"email": user.email})

    return {"message": "Login successful", "token": token}