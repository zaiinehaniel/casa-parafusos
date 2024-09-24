import json

import pandas as pd
import numpy as np
import base64
from io import BytesIO
import mimetypes

from constantes import PAGARME, MERCADO_PAGO


class ImportadorIntegracao:
    def __init__(self, origem):
        self.origem = origem
        # Mapping file extensions to their corresponding read methods
        self.read_files_mapping = {
            ".csv": self.read_csv,
            ".xls": self.read_excel,
            ".xlsx": self.read_excel,
            ".txt": self.read_text
        }
        self.read_files_origin_mapping = {
            MERCADO_PAGO: self.process_data_origin_mercado_pago
        }

        self.map_function = self.read_files_origin_mapping.get(self.origem)
        self.colunas_numericas_mercado_pago = [
            'VALOR LÍQUIDO CREDITADO', 'VALOR LÍQUIDO DEBITADO',
            'VALOR BRUTO DA OPERAÇÃO', 'TARIFA DO MERCADO PAGO OU DO MERCADO LIVRE',
            'CUSTO DE ENVIO', 'SALDO'
        ]

    def read_csv(self, data):
        # Read the CSV file from decoded data
        return pd.read_csv(BytesIO(data))

    def read_excel(self, data):
        # Read the Excel file from decoded data
        return pd.read_excel(BytesIO(data))

    def read_text(self, data):
        with open(data, 'r') as file:
            return file.read()

    def read_file(self, data, file_extension):
        read_method = self.read_files_mapping.get(file_extension)
        if read_method is None:
            raise ValueError("Unsupported file extension. Only '.csv', '.xls', '.xlsx', and '.txt' are supported.")

        return read_method(data)

    def import_file_from_base64(self, name, file_extension, base64_data):
        if not base64_data:
            return None

        decoded_data = base64.b64decode(base64_data)
        if file_extension not in [".csv", ".xls", ".xlsx"]:
            raise ValueError("Unsupported file type. Only 'csv', 'xlsx', and 'xls' are supported.")

        return self.generate_data_frame_from_imported_data(
            self.read_file(decoded_data, file_extension)
        )

    def generate_data_frame_from_imported_data(self, data):
        return self.map_function(data)

    def process_data_origin_mercado_pago(self, data_frame):
        # Convert relevant columns to numeric and take absolute values
        data_frame = data_frame[data_frame['ID DO PEDIDO'].notna()].copy()

        # Convert columns to numeric and take absolute values
        data_frame[self.colunas_numericas_mercado_pago] = data_frame[self.colunas_numericas_mercado_pago].apply(
            pd.to_numeric, errors='coerce').abs()

        # Convert 'DATA DE LIBERACAO' to datetime and extract the date part
        data_frame['DATA DE LIBERAÇÃO'] = pd.to_datetime(data_frame['DATA DE LIBERAÇÃO']).dt.strftime('%Y-%m-%d')

        # Filter rows where DESCRIÇÃO is either 'payment' or 'shipping'
        data_frame = data_frame[data_frame['DESCRIÇÃO'].isin(['payment', 'shipping'])]

        # Group by 'ID DO PEDIDO' and 'DATA DE LIBERACAO' and aggregate
        agrupador = data_frame.groupby(['ID DO PEDIDO', 'DATA DE LIBERAÇÃO']).agg({
            'VALOR LÍQUIDO CREDITADO': 'sum',
            'VALOR LÍQUIDO DEBITADO': 'sum',
            'VALOR BRUTO DA OPERAÇÃO': 'sum',
            'TARIFA DO MERCADO PAGO OU DO MERCADO LIVRE': 'sum',
            'CUSTO DE ENVIO': 'sum',
            'SALDO': 'sum',
            'DESCRIÇÃO': lambda x: ', '.join(x.unique()),  # Concatenate unique DESCRICAO values
            'ID DO ENVIO': 'first'
        }).reset_index()

        # Convert 'ID DO PEDIDO' and 'ID DO ENVIO' to int64
        agrupador['ID DO PEDIDO'] = agrupador['ID DO PEDIDO'].astype('int64')
        agrupador['ID DO ENVIO'] = agrupador['ID DO ENVIO'].astype('int64')

        # Create 'valor_titulo' as the sum of 'VALOR BRUTO DA OPERAÇÃO' and 'CUSTO DE ENVIO'
        agrupador['VALOR_TITULO'] = agrupador['VALOR BRUTO DA OPERAÇÃO'] + agrupador['CUSTO DE ENVIO']

        # Create 'VALOR_TARIFA' as the sum of 'TARIFA DO MERCADO PAGO OU DO MERCADO LIVRE'
        # Pandas already got this value just making explict here.
        agrupador['VALOR_TARIFA'] = agrupador['TARIFA DO MERCADO PAGO OU DO MERCADO LIVRE']

        # Create 'VALOR_FRETE' as the sum of 'CUSTO DE ENVIO'
        # Pandas already got this value just making explict here.
        agrupador['VALOR_FRETE'] = agrupador['CUSTO DE ENVIO']

        valor_tarifas = agrupador['VALOR_TARIFA'].sum()
        valor_frete = agrupador['VALOR_FRETE'].sum()

        data = agrupador.to_dict(orient="records")

        dados_filtrados = [self.create_objects_to_search_erp_mercado_pago(titulo) for titulo in data]

        return self.get_group_by_objects_from_dados_filtrados(dados_filtrados)

    def create_objects_to_search_erp_mercado_pago(self, obj):
        return {
            'data': obj.get('DATA DE LIBERAÇÃO'),
            'pedido': obj.get('ID DO PEDIDO'),
            'valor': round(obj.get('VALOR_TITULO'), 2),
            'tarifa': round(obj.get('VALOR_TARIFA'), 2),
            'custo_envio': round(obj.get('VALOR_FRETE'), 2),
            'descricao': obj.get('DESCRIÇÃO')
        }

    def get_group_by_objects_from_dados_filtrados(self, dados_filtrados):
        # Group data set, register i do BAIXA and sum Tarifa. And registers i had to sum shipping
        return {
            'baixa_tarifa': [obj for obj in dados_filtrados if 'payment' in obj.get('descricao')],
            'frete': [obj for obj in dados_filtrados if 'shipping' in obj.get('descricao')],
        }

    # PAGAR ME
