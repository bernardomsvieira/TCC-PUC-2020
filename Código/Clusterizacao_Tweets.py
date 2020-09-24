# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:47:55 2020

@author: bernardo.vieira
"""
import Constantes_Pos_puc
import Analise_Sentimento
import Exploracao_dados
import Realizar_Limpeza_Tweets
import datetime

import pickle
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import matplotlib.cm as cm


TRATAMENTO_TEXTO = True
OBTER_SSE_KMEANS = False
CARREGAR_MODELO = True
TREINAR_MODELO_KMEANS = False
TREINAR_MODELO_AGLOMERATIVE_CLUSTERING = False
OBTER_ORIENTACAO_SEMANTICA = True
CONTAR_PALAVRAS_CLUSTERS = True
EXPLORACAO_DADOS = False
MODELO = 'AGGLO' #AGGLO, KMEANS

DATA_DIA = str(datetime.datetime.today())

def obter_num_cluster_otimizado(data, max_k):
    
    iters = range(1, max_k + 1, 2)
    iters_labels = range(1, max_k + 1, 4)
    sse = []
    for k in iters:
        sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(data).inertia_)
        print('Fit {} clusters'.format(k))
        
    f, ax = plt.subplots(1, 1,figsize=(25, 15 ))
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters_labels)
    ax.set_xticklabels(iters_labels, rotation=90)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')

 
def obter_tweets_por_cluster(lista_texto_sem_duplicados,clusters):
    
    indice_planilha = 0
    dicionario_clusters = {}
    for cluster in clusters.labels_:
        lista = dicionario_clusters.get(cluster)
        if lista == None:
            lista = [lista_texto_sem_duplicados[indice_planilha]]
            dicionario_clusters[cluster] = lista
        else:
            lista.append(lista_texto_sem_duplicados[indice_planilha])
            dicionario_clusters[cluster] = lista
        indice_planilha+=1    
    return dicionario_clusters

def contar_palavras_por_cluster(df_tweets):
    
    lista_palavras_cluster = []
    cluster = 1
    for indice,linha in df_tweets.iterrows():
        tweet = linha[0]
        cluster = linha[1]    
        
        palavras_texto = tweet.split()
            
        for palavra in palavras_texto:
            lista_palavras_cluster.append([palavra,str(cluster)])
                
    df = pd.DataFrame(lista_palavras_cluster, columns=['PALAVRA', 'CLUSTER'])
    
    if MODELO == 'KMEANS':  
        df.to_excel('palavras_cluster_kmeans.xlsx',header=True, index=False)
    else:
        df.to_excel('palavras_cluster_AC.xlsx',header=True, index=False)
    
def main():
     
    kmeans = None
    agglo_clustering = None
    
    #OBTER TWEETS NAO DUPLICADOS
    lista_texto_sem_duplicados = Realizar_Limpeza_Tweets.obter_tweets_nao_duplicados()

    #LIMPEZA DOS TWEETS
    if TRATAMENTO_TEXTO:
        lista_texto_sem_duplicados = Realizar_Limpeza_Tweets.tratar_texto(lista_texto_sem_duplicados)

    vectorizer = TfidfVectorizer()    
    vectors = vectorizer.fit_transform(lista_texto_sem_duplicados)
    df_tweets = pd.DataFrame(lista_texto_sem_duplicados,columns =['Tweet'])
     
    #TREINAR MODELO
    if TREINAR_MODELO_KMEANS:
        
        kmeans = KMeans(n_clusters=Constantes_Pos_puc.TOTAL_CLUSTERS,init='k-means++',n_init=10, random_state=1234).fit(vectors)#MiniBatchKMeans(n_clusters=30, init_size=1024, batch_size=2048, random_state=10).fit_predict(vectors)       
        df_tweets["clusters"] = kmeans.fit_predict(vectors)
        
        pickle.dump(kmeans, open("modelo_kmeans_37.pkl", "wb"))
    
    if TREINAR_MODELO_AGLOMERATIVE_CLUSTERING:
        agglo_clustering = AgglomerativeClustering(n_clusters=Constantes_Pos_puc.TOTAL_CLUSTERS, affinity='euclidean', linkage='ward').fit(vectors.toarray())
        df_tweets["clusters"] = agglo_clustering.fit_predict(vectors.toarray())

        pickle.dump(agglo_clustering, open("modelo_agllomerative_37.pkl", "wb"))
              
    #CARREGA O MODELO
    if CARREGAR_MODELO:
        kmeans = pickle.load(open("modelo_kmeans_37.pkl", "rb"))    
        agglo_clustering = pickle.load(open("modelo_agllomerative_37.pkl", "rb"))  
        
        if MODELO == 'KMEANS':
            df_tweets["clusters"] = kmeans.fit_predict(vectors)
        else:
            df_tweets["clusters"] = agglo_clustering.fit_predict(vectors.toarray())

    #OBTEM ERRO
    if OBTER_SSE_KMEANS:
        obter_num_cluster_otimizado(vectors,200)
      
    if (CONTAR_PALAVRAS_CLUSTERS and CARREGAR_MODELO) or\
    (CONTAR_PALAVRAS_CLUSTERS and TREINAR_MODELO_KMEANS) or\
    (CONTAR_PALAVRAS_CLUSTERS and TREINAR_MODELO_AGLOMERATIVE_CLUSTERING):
        contar_palavras_por_cluster(df_tweets)

    #EXPLORACAO DOS DADOS
    modelo = None
    if EXPLORACAO_DADOS:
        if MODELO == 'KMEANS':
            modelo = kmeans        
        else:
            modelo = agglo_clustering
                 
        Exploracao_dados.obter_grafico_palavras_mais_comuns(lista_texto_sem_duplicados)
        Exploracao_dados.obter_nuvem_de_palavras(lista_texto_sem_duplicados)
        Exploracao_dados.obter_usuarios_base(lista_texto_sem_duplicados)
       
        if modelo != None:
            Exploracao_dados.top_palavras_cluster(modelo,vectorizer)
            Exploracao_dados.analise_tweets_por_data()
        
    #ORIENTACAO SEMANTICA
    if OBTER_ORIENTACAO_SEMANTICA:       
        dicionario_Orientacao_Semantica = Analise_Sentimento.realizar_analise_sentimento(lista_texto_sem_duplicados)
        Analise_Sentimento.analise_sentimento_por_cluster(Constantes_Pos_puc.TOTAL_CLUSTERS,dicionario_Orientacao_Semantica, df_tweets)  

if __name__ == "__main__":
    main()
