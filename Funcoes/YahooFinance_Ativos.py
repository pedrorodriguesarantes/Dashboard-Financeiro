import pandas as pd
from datetime import datetime, timedelta
import pandas as pd
import warnings
import yfinance as yf

def historico_valores(sigla, comeco, fim, intervalo):
    acao = yf.Ticker(sigla)
    
    dados = acao.history(
        start = comeco,
        end = fim,
        interval = intervalo
    )

    return dados

def coletar_acoes(dataframe):
    hoje = datetime.today().strftime('%Y-%m-%d')
    
    uma_semana = datetime.today() - timedelta(days = 6)
    uma_semana = uma_semana.strftime('%Y-%m-%d')

    um_mes = datetime.today() - timedelta(days = 31)
    um_mes = um_mes.strftime('%Y-%m-%d')

    um_ano = datetime.today() - timedelta(days = 365)
    um_ano = um_ano.strftime('%Y-%m-%d')

    dataframe_final = pd.DataFrame()

    for linha in dataframe.values:
        nome_acao = linha[3]
        id_acao = linha[0]
        lista = pd.DataFrame()

        try:
            warnings.filterwarnings('ignore')

            semana = historico_valores(nome_acao, uma_semana, hoje, '90m')
            semana['ID'] = [id_acao] * len(semana)
            semana['Periodo'] = ['Semanal'] * len(semana)

            lista = lista.append(semana)

            mes = historico_valores(nome_acao, um_mes, uma_semana, '1d')
            mes['ID'] = [id_acao] * len(mes)
            mes['Periodo'] = ['Mensal'] * len(mes)

            lista = lista.append(mes)

            ano = historico_valores(nome_acao, um_ano, um_mes, '1wk')
            ano['ID'] = [id_acao] * len(ano)
            ano['Periodo'] = ['Anual'] * len(ano)

            lista = lista.append(ano)
            dataframe_final = dataframe_final.append(lista)

        except:
            pass
    
    dataframe_final = dataframe_final.reset_index().rename(columns = {'index': 'Data'})
    return dataframe_final

def coletar_informacoes(dataframe):
    informacoes = list()
    for linha in dataframe.values:
        id = linha[0]
        link = linha[4]

        resultado = dados_mercado(link)
        resultado['ID'] = id
        
        informacoes.append(resultado)
    
    return pd.DataFrame(informacoes)

dataframe = coletar_acoes(pd.read_excel('C:/Users\Pedro/Documents/Dashboard-Financeiro/InfoEmpresas.xlsx'))
print(dataframe)
dataframe.to_csv('Precos.csv')
