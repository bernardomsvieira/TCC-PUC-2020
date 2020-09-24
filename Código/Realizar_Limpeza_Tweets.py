# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:59:00 2020

@author: bernardo.vieira
"""
import Constantes_Pos_puc

from nltk.corpus import stopwords
from unidecode import unidecode


def tratar_vogais_repetidas(palavra): 
  
    while('AA' in palavra):
        palavra = palavra.replace('AA','A')
        
    while('EE' in palavra):
        palavra = palavra.replace('EE','E')
    
    while('II' in palavra):
        palavra = palavra.replace('II','I')
    
    while('OO' in palavra):
        palavra = palavra.replace('OO','O')
        
    while('UU' in palavra):
        palavra = palavra.replace('UU','U')
        
    return palavra
    
def obter_tweets_nao_duplicados():
    arquivo = open(Constantes_Pos_puc.NOME_ARQUIVO, "r",encoding='utf-8')
    texto = arquivo.read()
    texto = texto.split('Usuário: ')
    lista_texto_sem_duplicados = list(dict.fromkeys(texto[1:]))
    print('Total de ' + str(len(lista_texto_sem_duplicados)) + ' tweets não duplicados')
    arquivo.close()
    return lista_texto_sem_duplicados


def tratar_texto(lista_sem_duplicados):    
    stop = stopwords.words('portuguese')
    stop.append('pra'.upper())
    stop.append('pras'.upper())
    stop.append('https'.upper())
    stop.append('umas'.upper())
    stop.append('RT'.upper())
    
    for i in range(0,len(stop)): 
        stop[i] = stop[i].upper() 
    
    lista_sem_duplicados = tratar_tuites(lista_sem_duplicados,stop)
    print('Após tratamentos: ' + str(len(lista_sem_duplicados)) + ' tweets não duplicados')
    arquivo_resultado = open("tweets_tratados.txt", "w")
    arquivo_resultado.write(str(lista_sem_duplicados))
    arquivo_resultado.close()
    return lista_sem_duplicados


def tratar_usuario_hashtag(palavra):
    if palavra[0] == '@':
        return ''
    
    if palavra[0] == '#':
        return ''
    
    return palavra

def tratar_palavra_baixo_calao(palavra):
    for palavrao in Constantes_Pos_puc.PALAVRAS_BAIXO_CALAO:
        if palavrao == palavra.upper():
            return 'Palavrão'
    return palavra

def tratar_risadas(palavra):
    for risada in Constantes_Pos_puc.RISADAS:
        if risada in palavra.upper():
            return 'Risada'
    return palavra
        
def tratar_link(palavra):
    if palavra[0:5] == 'HTTPS':
        return ''
    
    if palavra[0:4] == 'HTTP':
        return ''
    
    return palavra

def tratar_palavra_incompleta(palavra):
    
    if palavra[-3:] == '...':
        return ''
    return palavra
    

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

def tratar_expressoes(texto):
    texto = texto.replace('BOM DIA','BOMDIA')
    texto = texto.replace('BOA NOITE','BOANOITE')
    texto = texto.replace('BOA TARDE','BOATARDE')
    texto = texto.replace('BOA SORTE','BOASORTE')
    texto = texto.replace('MENOS MAL','MENOSMAL')
    texto = texto.replace('MENOS MAU','MENOSMAU')
    texto = texto.replace('TUDO BEM','TUDOBEM')

    return texto


def limpar_texto(texto,stop):
    
    texto = unidecode(str(texto)).upper()   
    resultado = ''.join([i for i in str(texto) if not i.isdigit()])
    resultado = tratar_expressoes(resultado)
    
    #NAO REMOVIDO A #
    pontuacao = r'".,!$%&*()-_+=+{}[]]?;:<>,´"\/\''
        
    string = ''    
    palavras = resultado.split()
    
    contador_validas = 0
    for palavra in palavras:
        #item == 'ar' or len(item) > 2) and 
             
        #palavra_valida = padronizar_plural(palavra)
        palavra_valida = tratar_risadas(palavra)
        palavra_valida = tratar_palavra_baixo_calao(palavra_valida)
        palavra_valida = tratar_usuario_hashtag(palavra_valida)
        palavra_valida = tratar_link(palavra_valida)
        palavra_valida = tratar_palavra_incompleta(palavra_valida)
        palavra_valida = tratar_vogais_repetidas(palavra_valida)
        
        for caractere in pontuacao:
            palavra_valida = palavra_valida.replace(caractere,' ')
        
        if Constantes_Pos_puc.USAR_STEMMING and palavra_valida != '':
            palavra_valida = Constantes_Pos_puc.stemmer.stem(palavra_valida)
            
        if len(palavra) > 2 and palavra not in (stop):    
            contador_validas+=1
            string += " " + palavra_valida.strip()     
    
    if contador_validas < 5:
        return None
    
    return string.upper().strip() 

def tratar_tuites(lista_tweets,stop):
    
    lista_tweets_tratados = []
    
    for i in range(len(lista_tweets)):
        
        tweet = lista_tweets[i]
        tweet_tratado = limpar_texto(tweet,stop)
        
        if tweet_tratado != None:
            lista_tweets_tratados.append(tweet_tratado)
            
    return lista_tweets_tratados
