# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:53:13 2020

@author: bernardo.vieira

"""
import time
import pandas as pd
from datetime import date
import Arquivo_Log
import tweepy

termos = ['Pandemia','COVID','Corona','Quarentena','Isolamento Social','Lockdown']

def tratar_arquivo_log():
    pass

OBTER_SEGUIDORES = True
OBTER_TUITES = True

arquivo_log = Arquivo_Log.ArquivoLog()
arquivo_log.definir_caminho_log('./Logs/')
arquivo_log.definir_nome_log('log_tweets')

chave_consumidor = 'TESTE'
segredo_consumidor = 'TESTE'
token_acesso = 'TESTE'
token_acesso_segredo = 'TESTE'

autenticacao = tweepy.OAuthHandler(chave_consumidor, segredo_consumidor)
autenticacao.set_access_token(token_acesso, token_acesso_segredo)

data_hoje = date.today()
data_hoje = '{}/{}/{}'.format(data_hoje.day, data_hoje.month,data_hoje.year)

twitter = tweepy.API(autenticacao)

if OBTER_TUITES:
    
    for palavra in termos:
        resultados = twitter.search(q=palavra,lang='pt',count = 100,tweet_mode="extended",result_type="mixed")
        arquivo_log.escrever_log('Data: ' + str(data_hoje))
        for tweet in resultados:
             try:
                 texto = (f'Usuário: {tweet.full_text}')
                 texto = texto.encode('utf-8').decode('utf-8')
                 arquivo_log.escrever_log(str(texto))
             except Exception as E:
                 pass
    

if OBTER_SEGUIDORES:
    
    df_usuarios_seguidores = pd.read_excel('usuarios_seguidores.xlsx')
    
    usuarios_ja_obtidos = []
    usuarios_seguidores_ja_obtidos = []
    
    for indice, linha in df_usuarios_seguidores.iterrows():
        usuario = linha[0]
        seguidores = linha[1]
        usuarios_seguidores_ja_obtidos.append([usuario,seguidores])
        if usuario not in usuarios_ja_obtidos:
            usuarios_ja_obtidos.append(usuario)
            
    #Retorna quem ele segue
    
    df_usuarios = pd.read_excel('usuarios_tweets.xlsx')
    lista_usuario_seguidores = []
    
    for indice, linha in df_usuarios.iterrows():
        try:
            if linha[0] not in usuarios_ja_obtidos:
                resultados = twitter.friends_ids(id=linha[0].strip())
                print(linha[0])
                #print(len(resultados))
                for seguindo in resultados:
                    lista_usuario_seguidores.append([linha[0],str(seguindo)])
                
        except Exception as E:
            print(str(E))
            lista_usuario_seguidores.append([linha[0],'NAO EXISTE'])
            if str(E) == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                #time.sleep(900)
                break 
                
    lista_usuario_seguidores.extend(usuarios_seguidores_ja_obtidos)
    df = pd.DataFrame(lista_usuario_seguidores, columns=['USUARIO','SEGUINDO'])
    df.to_excel('usuarios_seguidores.xlsx',header=True, index=False)