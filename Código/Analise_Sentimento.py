# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:53:45 2020

@author: bernardo.vieira
"""
import Constantes_Pos_puc
import pandas as pd

import random
from collections import Counter
from collections import defaultdict
import math
import operator

OBTER_TOP_ANALISE_SENTIMENTOS = True

VOCABULARIO_POSITIVO = []
VOCABULARIO_NEGATIVO = []

def carregar_termos_positivos_negativos():    
    df_positivo = pd.read_excel('termos_positivos.xlsx')
    df_negativo = pd.read_excel('termos_negativos.xlsx')
    
    lista_todos_negativos = []
    indices_sorteados = []
    
    num_randomico = 0
    
    for indice, linha in df_positivo.iterrows():
        VOCABULARIO_POSITIVO.append(linha[0])
    VOCABULARIO_POSITIVO.extend(Constantes_Pos_puc.VOCABULARIO_POSITIVO_ADICIONAL)
           
    for indice, linha in df_negativo.iterrows():
        # lista_todos_negativos.append(linha[0])
        VOCABULARIO_NEGATIVO.append(linha[0])

    # quantidade_positivas = len(VOCABULARIO_POSITIVO)
    # for i in range(quantidade_positivas):
        
    #     while(num_randomico in indices_sorteados):
    #         num_randomico = random.randrange(0,len(lista_todos_negativos))
        
    #     indices_sorteados.append(num_randomico)
    #     VOCABULARIO_NEGATIVO.append(lista_todos_negativos[num_randomico])       
        
    
    VOCABULARIO_NEGATIVO.extend(Constantes_Pos_puc.VOCABULARIO_NEGATIVO_ADICIONAL)
    
def realizar_steaming_vetores_palavras(vetor_pos, vetor_neg):
    for i in range(len(vetor_pos)):
        palavra = vetor_pos[i]
        palavra_steaming = Constantes_Pos_puc.stemmer.stem(palavra)
    

def realizar_analise_sentimento(lista_tweets):
    print('Iniciando Analise de Sentimento')
    carregar_termos_positivos_negativos()
    contador, com = obter_matriz_co_ocorrencia(lista_tweets)
    p_t, p_t_com = obter_probabilidade_palavra(len(lista_tweets),contador,com)
    dicionario_analise_sentimento = obter_PMO(p_t, p_t_com,com)
    return dicionario_analise_sentimento
    
def obter_matriz_co_ocorrencia(lista_tweets):
    contador = Counter()
    com = defaultdict(lambda : defaultdict(int))
    
    for tweet in lista_tweets:
        
        palavras = tweet.split()
        
        contador.update(palavras)
               
        for i in range(len(palavras)-1):            
            for j in range(i+1, len(palavras)):
                w1, w2 = sorted([palavras[i], palavras[j]])                
                if w1 != w2:
                    com[w1][w2] += 1
                                    
    return contador, com

def obter_probabilidade_palavra(total_tweets,contador,com):
    
    p_t = {}
    p_t_com = defaultdict(lambda : defaultdict(int))
    n_docs = total_tweets
    
    #computing the probability of a word
    for term, n in contador.items():
        p_t[term] = n / n_docs
        for t2 in com[term]:
            p_t_com[term][t2] = com[term][t2] / n_docs
            
    return p_t, p_t_com

            
def obter_PMO(p_t,p_t_com,com):      
        
    pmi = defaultdict(lambda : defaultdict(int))
    for t1 in p_t:
        for t2 in com[t1]:
            denom = p_t[t1] * p_t[t2]
            pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)
     
    semantic_orientation = {}
    
    if Constantes_Pos_puc.USAR_STEMMING:
        realizar_steaming_vetores_palavras(Constantes_Pos_puc.VOCABULARIO_POSITIVO,Constantes_Pos_puc.VOCABULARIO_NEGATIVO)
    
    for term, n in p_t.items():
        positive_assoc = sum(pmi[term][tx] for tx in VOCABULARIO_POSITIVO)
        negative_assoc = sum(pmi[term][tx] for tx in VOCABULARIO_NEGATIVO)
        semantic_orientation[term] = positive_assoc - negative_assoc
    
    semantic_sorted = sorted(semantic_orientation.items(), 
                             key=operator.itemgetter(1), 
                             reverse=True)
    
    
    dicionario_Orientacao_Semantica = {}
    
    arquivo_resultado_OS = open('resultado_OS.txt','w')
    
    for tupla in semantic_sorted:
        palavra = tupla[0]
        nota = tupla[1]
        
        dicionario_Orientacao_Semantica[palavra] = nota
        arquivo_resultado_OS.write(str(palavra)+':'+str(nota)+'\n')
      
    arquivo_resultado_OS.close()
    
    if OBTER_TOP_ANALISE_SENTIMENTOS:
        
        top_pos = semantic_sorted[:15]
        top_neg = semantic_sorted[-15:]
        
        palavras_pos = 0
        palavras_neg = 0
        palavras_neutras = 0
        
        for tupla in semantic_sorted:
            palavra = tupla[0]
            nota = tupla[1]
            
            if nota > 0:
                palavras_pos += 1
            elif nota == 0:
                palavras_neutras += 1
            else:
                palavras_neg += 1
                
        print('QUANTIDADE DE POSITIVAS: ' + str(palavras_pos))
        print('QUANTIDADE DE NEGATIVAS: ' + str(palavras_neg))
        print('QUANTIDADE DE NEUTRAS: ' + str(palavras_neutras))
        
        print("TOP POSITIVAS " + str(top_pos))
        print("TOP NEGATIVAS " + str(top_neg))

    return dicionario_Orientacao_Semantica


def analise_sentimento_por_cluster(total_clusters,dicionario_Orientacao_Semantica, df_cluster):
    
    nota_mais_negativa = 0
    tweet_mais_negativo = ''
    
    nota_mais_positiva = 0
    tweet_mais_positivo = ''
    
    
    lista_positivo_negativo_por_cluster = []
    
    for i in range(total_clusters):
        
        tweet_positivo = 0
        tweet_negativo = 0
        
        for indice, linha in df_cluster.iterrows():
            
            tweeter = linha['Tweet']
            cluster = linha['clusters']
            
            if cluster == i:
                palavras = tweeter.split()
            
                nota_tweeter = 0
            
                for palavra in palavras:
                    nota = dicionario_Orientacao_Semantica.get(palavra)
                
                    nota_tweeter += nota
                    
                #print(tweeter)
                if nota_tweeter < 0:
                    #print('Negativo')
                    tweet_negativo+=1
                    if nota_tweeter < nota_mais_negativa:
                        nota_mais_negativa = nota_tweeter
                        tweet_mais_negativo = tweeter
                else:
                    #print('Positivo')
                    tweet_positivo+=1
                    if nota_tweeter > nota_mais_positiva:
                        nota_mais_positiva = nota_tweeter
                        tweet_mais_positivo = tweeter
    
        lista_positivo_negativo_por_cluster.append((tweet_positivo,tweet_negativo))
    
    print(lista_positivo_negativo_por_cluster)
    
    print(str(nota_mais_positiva) + '-' + tweet_mais_positivo)
    print(str(nota_mais_negativa) + '-' + tweet_mais_negativo)