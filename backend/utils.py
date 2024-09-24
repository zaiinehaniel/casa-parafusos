import calendar
from datetime import datetime

def obtenha_valor_registro_tarifa_ecommerce(lista_titulos_baixados):
    valor_tarifa = 0
    for titulo in lista_titulos_baixados:
        valor_tarifa += titulo.get('tarifa')
    return round(valor_tarifa, 2)

def obtenha_valor_registro_frete_ecommerce(lista_titulos_frete):
    valor_frete = 0
    for titulo in lista_titulos_frete:
        valor_frete+= titulo.get('custo_envio')
    return round(valor_frete, 2)

def obtenha_data_registro_tarifa_ecommerce(lista_titulos_baixados):
    return min([d['data'] for d in lista_titulos_baixados])

def obtenha_data_registro_frete_ecommerce(lista_titulos_frete):
    return min([d['data'] for d in lista_titulos_frete])


def obtenha_ultimo_dia_mes(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
    return date_obj.replace(day=last_day).strftime('%Y-%m-%d')