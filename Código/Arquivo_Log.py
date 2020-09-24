# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:38:38 2019

@author: bernardo.vieira
"""

import time

class ArquivoLog:
    
    caminho_log = ''
    
    nome_log = ''
    
    def obter_data(self):
        diaAtual = int(time.strftime("%d"))
        mesAtual = int(time.strftime("%m"))
        anoAtual = int(time.strftime("%Y"))
        
        data = str(diaAtual) + "_" + str(mesAtual) + "_" + str(anoAtual)
        
        return data
        
    def definir_nome_log(self,nome):
        self.nome_log = nome
    
    def definir_caminho_log(self,caminho):
        self.caminho_log = caminho
        
    def escrever_log(self,escrita):
        
        data = self.obter_data()
        nome_arquivo_log = str(self.caminho_log) + 'log_' + self.nome_log + '_' + data + '.txt'
        
        with open(nome_arquivo_log, "a+") as arquivo_log:
            arquivo_log.write(escrita + '\n')
        
        