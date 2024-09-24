import requests
from fastapi import HTTPException
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
import json

import utils
from constantes import FRETE, TARIFA
from database import database, schemas
from models import models


class OAuthTokenError(Exception):
    """Base class for OAuth token errors"""
    pass

class UnauthorizedError(OAuthTokenError):
    """Raised when the request is unauthorized (401)"""
    pass

class BadRequestError(OAuthTokenError):
    """Raised when the request is bad (400)"""
    pass

class ForbiddenError(OAuthTokenError):
    """Raised when the request is forbidden (403)"""
    pass

class NotFoundError(OAuthTokenError):
    """Raised when the resource is not found (404)"""
    pass

class InternalServerError(OAuthTokenError):
    """Raised when the server encounters an internal error (500)"""
    pass

class IntegracaoIntegrin:

    def __init__(self):
        self.base_url = 'http://10.0.247.5:4664'
        self.password = '1nt3gr@'
        self.username = 'INTEGRA'
        self.grant_type = 'password'
        self.client_secret = 'poder7547'
        self.client_id = 'cisspoder-oauth'
        self.token = self._get_auth_token()
        self.requisicao_titulos = []
        self.sispoder_titulos = []
        self.titulos_baixados = []
        self.titulos_baixados_erro = []
        self.db_session = next(self.get_db())
        self.configuracao_integracao = self.db_session.query(models.Integracao).first()

    def get_db(self):
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()


    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": self.token
        }

    def _check_response_status(self, response):
        if response.status_code == 401:
            raise UnauthorizedError("Unauthorized: Check your credentials and try again.")
        elif response.status_code == 400:
            raise BadRequestError("Bad Request: The server could not understand the request due to invalid syntax.")
        elif response.status_code == 403:
            raise ForbiddenError("Forbidden: You do not have permission to access this resource.")
        elif response.status_code == 404:
            raise NotFoundError("Not Found: The requested resource could not be found.")
        elif response.status_code == 500:
            raise InternalServerError("Internal Server Error: The server encountered an internal error.")
        else:
            raise OAuthTokenError(f"Unexpected status code: {response.status_code}")

    # Auxiliar
    def create_request_search_titulo_on_sispoder(self, dado_importacao):
        pass
        # if not dado_importacao:
        #     return None
        #
        # return {
        #     "page:": 1,
        #     "clausulas": [
        #         {
        #             "campo": "obspedido",
        #             "valor": str(int(dado_importacao.get('titulo'))),
        #             "operadorlogico": "AND",
        #             "operador": "LIKE"
        #         }
        #     ],
        #     "ordenacoes": []
        # }


    def _get_auth_token(self):
        url = f"{self.base_url}/cisspoder-auth/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "password": self.password,
            "username": self.username,
            "grant_type": self.grant_type,
            "client_secret": self.client_secret,
            "client_id": self.client_id,
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            try:
                data = response.json()
                return f"Bearer {data.get('access_token')}"
            except ValueError:
                raise OAuthTokenError("Response content is not valid JSON")
        except requests.exceptions.HTTPError as http_err:
            raise OAuthTokenError(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as e:
            raise OAuthTokenError(f"An error occurred: {e}")

    def baixar_titulos_ecommerce(self, lista_titulos):
        for titulo in lista_titulos:
            self.baixar_titulo_ecommerce(titulo)

        return self.titulos_baixados, self.titulos_baixados_erro

    def baixar_titulo_ecommerce(self, titulo):
        url = f"{self.base_url}/cisspoder-service/baixatituloecommerce"
        headers = self._get_headers()
        try:
            data = {
                "PEDIDOECOMMERCE": titulo.get('pedido'),
                "DATAPAGAMENTO": titulo.get('data'),
                "VALORPAGAMENTO": float(titulo.get('valor')),
                "CONTACONTABIL": self.configuracao_integracao.conta_contabil
            }

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                res = response.json()
                self.titulos_baixados.append(data)
            else:
                # Tratar aqui casos onde nao foi possivel baixar o titulo
                self.titulos_baixados_erro.append(data)
                raise HTTPError(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except requests.exceptions.RequestException as req_err:
            raise HTTPException(status_code=500, detail=str(req_err))

        return self.sispoder_titulos

    def lancar_valor_frete_importacao(self, file_data, tipo):
        url = f"{self.base_url}/cisspoder-service/lancatitulostaxafrete"
        headers = self._get_headers()

        if tipo == FRETE:
            valor = utils.obtenha_valor_registro_frete_ecommerce(file_data.get('frete'))
            data = utils.obtenha_data_registro_frete_ecommerce(file_data.get('frete'))
            cliente = self.configuracao_integracao.cliente_frete
        else:
            valor = utils.obtenha_valor_registro_tarifa_ecommerce(file_data.get('baixa_tarifa'))
            data = utils.obtenha_data_registro_tarifa_ecommerce(file_data.get('baixa_tarifa'))
            cliente = self.configuracao_integracao.cliente_tarifa

        try:
            data = {
                "CLIENTE": cliente,
                "EMPRESA": self.configuracao_integracao.empresa,
                "VALORTITULO": float(valor),
                "CONTACONTABIL": self.configuracao_integracao.conta_contabil,
                "DATAMOVIMENTO": data,
                "FORMAPAGAMENTO": self.configuracao_integracao.forma_pagamento,
                "DATAVENCIMENTO": utils.obtenha_ultimo_dia_mes(data),
                "CONTACONTABILCONTRAPARTIDA": self.configuracao_integracao.conta_contabil_contra_partida,
            }
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                resdd = response.json()
                self.titulos_baixados.append(data)
            else:
                # Tratar aqui casos onde nao foi possivel baixar o titulo
                self.titulos_baixados_erro.append(data)
                raise HTTPError(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except requests.exceptions.RequestException as req_err:
            raise HTTPException(status_code=500, detail=str(req_err))




    def get_titulo_data(self, titulos: list):
        url = f"{self.base_url}/cisspoder-service/cp/consultatitulo"
        headers = self._get_headers()

        return None

        # if not titulos:
        #     return None
        #
        # titulos_request = [self.create_request_search_titulo_on_sispoder(titulo) for titulo in titulos]
        #
        # try:
        #     for req in titulos_request:
        #         response = requests.post(url, json=req, headers=headers)
        #         response.raise_for_status()
        #
        #         if response.status_code == 200:
        #             ciss_titulo = response.json().get('data')[0] if len(response.json().get('data')) else None
        #             self.sispoder_titulos.append(ciss_titulo)
        #         else:
        #             raise HTTPError(f"Unexpected status code: {response.status_code}")
        #
        # except requests.exceptions.HTTPError as http_err:
        #     raise HTTPException(status_code=response.status_code, detail=str(http_err))
        # except requests.exceptions.RequestException as req_err:
        #     raise HTTPException(status_code=500, detail=str(req_err))
        #
        # return self.sispoder_titulos
