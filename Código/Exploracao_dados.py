# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:17:56 2020

@author: bernardo.vieira
"""
import re
from os import listdir

import pandas as pd
import Constantes_Pos_puc
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

QUANTIDADE_MAIS_COMUNS = 50

def analise_tweets_por_data():
    
    arquivo = open(Constantes_Pos_puc.NOME_ARQUIVO, "r",encoding='utf-8')
    texto = arquivo.read()
    arquivo.close()
    
    arquivos_diretorio = listdir(r'C:/Users/berna/Desktop/TCC-POSPUC/Logs/')
    
    eixo_x = []
    eixo_y = []
    
    for log in arquivos_diretorio:
        if 'log' in log:
            
            data = log[-13:-4]
            
            print(data)
            if data[0] == '_':
                data = data[1:]
            eixo_y.append(data)
            
            arquivo_log = open(r'C:/Users/berna/Desktop/TCC-POSPUC/Logs/'+log,'r')
            
            texto = arquivo_log.read()
            print(len(texto.split('Usuário:')))
            arquivo_log.close()
            
            eixo_x.append(len(texto.split('Usuário:')))
            
    fig = plt.figure(figsize=(8, 5))
    
    ax = fig.add_axes([0,0,1,1])
    
    ax.bar(eixo_y,eixo_x)
    plt.xticks(rotation='vertical')
    plt.show() 
    
    
def top_palavras_cluster(kmeans,vectorizer ):
    
    print("Top Palavras por Cluster")
    
    arquivo_resultado = open("top_palavras_cluster.txt", "a")
    
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    
    for i in range(Constantes_Pos_puc.TOTAL_CLUSTERS):
        #print("Cluster %d:" % i)
        arquivo_resultado.write("Cluster %d:" % i)
        for ind in order_centroids[i, :15]:
            #print(' %s' % terms[ind])
            arquivo_resultado.write(' %s' % terms[ind])
        arquivo_resultado.write('\n')
            
    arquivo_resultado.close()
            
            
def obter_usuarios_base(lista_tweets):
    contador_usuarios = Counter
    usuarios = []
    
    for tweets in lista_tweets:
        palavras = tweets.split()
        
        for palavra in palavras:
            if palavra[0] == '@':
                if palavra[len(palavra)-1] == ':':
                    palavra = palavra[:len(palavra)-1]
                usuarios.append(palavra)
        
    df = pd.DataFrame(usuarios, columns=['USUARIOS'])
    df.to_excel('usuarios_tweets.xlsx',header=True, index=False)
    
    contador_usuarios.update(usuarios)
    obter_grafico_barra_palavras_mais_comuns(Counter(usuarios).most_common(QUANTIDADE_MAIS_COMUNS))
    
def obter_grafico_palavras_mais_comuns(lista_tweets):

    texto_total = ''
    for tweets in lista_tweets:
        texto_total += tweets.replace('PANDEMIA','').replace('CORONA','').replace('COVID','').replace('QUARENTENA','').replace('ISOLAMENTO SOCIAL','').replace('LOCKDOWN','')
            
    #contador_palavras.update(texto_total.split())
    
    obter_grafico_barra_palavras_mais_comuns(Counter(texto_total.split()).
                                             most_common(QUANTIDADE_MAIS_COMUNS))

def obter_grafico_barra_palavras_mais_comuns(lista_mais_comuns):
    
    fig = plt.figure(figsize=(8, 5))
    
    ax = fig.add_axes([0,0,1,1])
    
    eixo_x = []
    eixo_y = []
    
    for tupla in lista_mais_comuns:
        eixo_y.append(tupla[0])
        eixo_x.append(tupla[1])
        
    ax.bar(eixo_y,eixo_x)
    plt.xticks(rotation='vertical')
    plt.show()    
    

def obter_nuvem_de_palavras(lista_texto_sem_duplicados):
    
    texto_todos_tweets = ''
    for texto in lista_texto_sem_duplicados:
        texto_todos_tweets += texto + ' '
        
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(texto_todos_tweets)
    plt.figure(figsize=(8, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()