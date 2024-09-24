from pydantic import BaseModel, EmailStr

class IntegracaoSchema(BaseModel):
    name: str
    forma_pagamento: str
    conta_contabil: str
    conta_contabil_contra_partida: str
    empresa: str
    cliente_tarifa: str
    cliente_frete: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True