# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 01:23:16 2020

@author: bernardo.vieira
"""

from unidecode import unidecode

def padronizar_plural(palavra):
    
    lista_til = ['AO']
    lista_vogais = ['A','E','I','O','U']
    lista_R_S_Z = ['R','S','Z']
    
    if palavra[len(palavra)-1] in lista_R_S_Z:
        
        if palavra[len(palavra)-1] == 'R':
            return palavra + 'ES'
        
        if palavra[len(palavra)-1] == 'Z':
            return palavra + 'ES'
    
    if palavra[len(palavra)-2:len(palavra)] in lista_til:        
        return palavra[0:len(palavra)-2] + 'OES'
    
    
    if palavra[len(palavra)-1] in lista_vogais:       
        return palavra + 'S'
    
    if palavra[len(palavra)-1] in ['M']:
        return palavra[0:len(palavra)-1] + 'NS'
    
    if palavra[len(palavra)-1] in ['L']: 
        
        if palavra[len(palavra)-2:len(palavra)] == 'IL':
            return palavra[0:len(palavra)-2] + 'IS'
        
        return palavra[0:len(palavra)-1] + 'IS'
    
    return palavra


import pandas as pd

palavras_positivas =  pd.read_csv('C:/Users/berna/Desktop/TCC-POSPUC/Planilhas/corpus-positivo.csv')
lista_palavras_positivas = []

for indice, linha in palavras_positivas.iterrows():
    palavra_traduzida = unidecode(linha[2]).upper().strip()
    
    if palavra_traduzida != 'IGUAL' and palavra_traduzida != 'SIM':
        if ' ' not in palavra_traduzida and '-' not in palavra_traduzida:       
            palavra_traduzida_plural = padronizar_plural(palavra_traduzida)
            
            if palavra_traduzida not in lista_palavras_positivas:
                lista_palavras_positivas.append(palavra_traduzida)
                
            if palavra_traduzida_plural not in lista_palavras_positivas:
                lista_palavras_positivas.append(palavra_traduzida_plural)
        

palavras_negativas =  pd.read_csv('C:/Users/berna/Desktop/TCC-POSPUC/Planilhas/corpus-negativo.csv')
lista_palavras_negativas = []

for indice, linha in palavras_negativas.iterrows():
    palavra_traduzida = unidecode(linha[2]).upper().strip()
    
    if palavra_traduzida != 'IGUAL' and palavra_traduzida != 'SIM':
        if ' ' not in palavra_traduzida and '-' not in palavra_traduzida:       
            palavra_traduzida_plural = padronizar_plural(palavra_traduzida)
            
            if palavra_traduzida not in lista_palavras_negativas:
                lista_palavras_negativas.append(palavra_traduzida)
                
            if palavra_traduzida_plural not in lista_palavras_negativas:
                lista_palavras_negativas.append(palavra_traduzida_plural)

    
df_positivas = pd.DataFrame(lista_palavras_positivas, columns=['POSITIVOS'])
df_positivas.to_excel('termos_positivos.xlsx',header=True, index=False)
    
df_negativas = pd.DataFrame(lista_palavras_negativas, columns=['NEGATIVOS'])
df_negativas.to_excel('termos_negativos.xlsx',header=True, index=False)

df_positivo = pd.read_excel('termos_positivos.xlsx')
df_negativo = pd.read_excel('termos_negativos.xlsx')
