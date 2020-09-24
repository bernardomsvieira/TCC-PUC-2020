# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:37:19 2020

@author: bernardo.vieira
"""
import nltk

TOTAL_CLUSTERS = 37

USAR_STEMMING = False

NOME_ARQUIVO = "Logs/resultado_25_7_a_17_8.txt"

RISADAS = ['KKK','HAHA','RSRS','AHAH','AHUAHU']

PALAVRAS_BAIXO_CALAO = ['FDP','FPD','CARALHO','VIADO','RETARDADO','BURRO','PORRA','POHA','MERDA','VADIA','FODASE',
                        'PUTA','CORNO','BUCETA','CORNA','BOSTA','SACO','CU','VADIA','CUZAO','CARAIO','OTARIO',
                        'BOIOLA','FURICO','VTNC']

VOCABULARIO_POSITIVO_ADICIONAL = ['BOM','BONS','BOA','BOAS',
                        'INCRIVEIS','INCRIVEL',
                        'OTIMO','OTIMA','OTIMOS','OTIMAS',
                        'ALEGRE','FELIZ','FELIZES','FELIZMENTE',
                        'AMO','AMOR',
                        'FANTASTICO','FANTASTICOS', 
                        'GOSTO','GOSTOU',
                        'MELHOR']
                    

VOCABULARIO_NEGATIVO_ADICIONAL = ['RUIM','RUINS',
                        'MAL','MALES',
                        'PESSIMO','PESSIMOS','PESSIMA','PESSIMAS', 
                        'TRISTE','INFELIZ','INFELIZES', 'INFELIZMENTE',
                        'ODEIO','ODIO',
                        'HORRIVEL','HORRIVEIS',
                        'DETESTO','DETESTOU',
                        'PIOR']                                    
                       

stemmer = nltk.stem.RSLPStemmer()
