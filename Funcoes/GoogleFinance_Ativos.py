import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime, timedelta
import pandas as pd
import warnings

def coletar_pagina(link):
    link = urlopen(link)
    
    warnings.filterwarnings('ignore')
    soup = BeautifulSoup(link, parser = 'html.parser')

    return soup

def dados_mercado(link):
    pagina = coletar_pagina(link)
    dados = dict()

    nome = pagina.find('div', attrs = {'class': 'zzDege'}).getText()
    preco_atual = pagina.find('div', attrs = {'class': 'YMlKec fxKbKc'}).getText()

    dados['Name'] = nome
    dados['Current Price'] = preco_atual

    for value in pagina.findAll('div', attrs = {'class': 'gyFHrc'}):
        chave = value.find('div', attrs = {'class': 'mfs7Fc'}).getText()
        dado = value.find('div', attrs = {'class': 'P6K39c'}).getText()
        dados[chave] = dado
    
    return dados

def coletar_informacoes(dataframe):
    informacoes = list()

    for linha in dataframe.values:
        id = linha[0]
        link = linha[4]

        resultado = dados_mercado(link)
        resultado['ID'] = id

        if linha[2] == 'CriptoMoeda':
            print(resultado)
            preco = resultado['Current Price']
            preco = preco.replace(',', ';')
            preco = preco.replace('.', ',')
            preco = preco.replace(';', '.')

            resultado['Current Price'] = preco

            preco = resultado['Previous close']
            preco = preco.replace(',', ';')
            preco = preco.replace('.', ',')
            preco = preco.replace(';', '.')

            resultado['Previous close'] = preco
            print(resultado)
    
        informacoes.append(resultado)
    return pd.DataFrame(informacoes)

dataframe_informacoes = coletar_informacoes(pd.read_excel('C:/Users/Pedro/Documents/Dashboard-Financeiro/InfoEmpresas.xlsx'))
dataframe_informacoes.to_excel('DescricaoEmpresas.xlsx')