# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:34:19 2020

@author: Puu
"""

import pandas as pd
from collections import defaultdict
import random
          
# DADOS INSERIDOS PELO USUÁRIO
print ('Vamos gerar textos automáticos para posts em redes sociais.')
print ('Escolha uma opção dentre TWITTER, FABEBOOK ou INSTAGRAM.')
rede = str(input('Qual a rede escolhida? '))
rede = rede.upper()

# DADOS A SEREM TRABALHADOS
planilha_dados = pd.read_csv('planilha_dados.csv', encoding='utf-8')
posts_brutos = planilha_dados['ELEMENTOS TEXTUAIS'].values.tolist()  
posts_brutos_rede = planilha_dados[planilha_dados['REDE'] == rede]['ELEMENTOS TEXTUAIS'].values.tolist()

# PREPARAR TEXTO
def preparar_texto(lista):
    arquivo = ' '.join(lista)
    arquivo = arquivo.split()
    for palavra in arquivo:
        if 'http' in palavra:
            arquivo.remove(palavra)
    arquivo_texto = ' '.join(arquivo)
    arquivo_texto = arquivo_texto.replace('.', ' <s> </s> ')
    arquivo_texto = arquivo_texto.replace('!', ' <s> </s> ')
    arquivo_texto = arquivo_texto.replace('?', ' <s> </s> ')
    texto = arquivo_texto.split()
    retirar = ',:;"`()[]{}\|$%^&*人'
    texto_parcial = [x.strip(retirar).lower() for x in texto] 
    texto_tratado = [x for x in texto_parcial
            if x.isalpha() or '-' in x or '@' in x or '#' in x or '<s>' in x or '</s>' in x]
    
    return texto_tratado

texto_geral = preparar_texto(posts_brutos)
texto_rede = preparar_texto(posts_brutos_rede)

# CRIAR BIGRAMAS E TRIGRAMAS
def gerar_ngramas(lista_tratada):
    unigramas = lista_tratada
    bigramas = list(zip(unigramas, unigramas[1:]))
    trigramas = list(zip(unigramas, unigramas[1:], unigramas[2:]))
     
    return bigramas, trigramas

bi = gerar_ngramas(texto_geral)[0]
tri = gerar_ngramas(texto_geral)[1]

# DEFINIR MÉDIA DE PALAVRAS PARA SAÍDA
media = len(texto_rede)/len(posts_brutos_rede)

# DEFINIR MÁXIMO DE CARACTERES PARA SAÍDA
def max_caracteres(string):
    if (string == 'TWITTER'):
        caracteres = 140
    elif (string == 'FACEBOOK'):
        caracteres = 63206
    else:
        caracteres = 2200
    return caracteres

caracteres_max = max_caracteres(rede)

# GERAR TEXTO
def inicio_de_post(bigramas):
    inicio_post = list()
    for tupla in bigramas:
        if (tupla[0] == '</s>' and tupla[1] != '<s>'):
            inicio_post.append(tupla[1])
    return inicio_post

inicio_post = inicio_de_post(bi)

def final_de_post(bigramas):
    final_post = list()
    for tupla in bigramas:
        if (tupla[1] == '<s>' and tupla[0] != '</s>'):
            final_post.append(tupla[0])
    return final_post

final_post = final_de_post(bi)

def gerar_texto(inicio, final, media_de_palavras, caracteres, bigramas, trigramas):
    post = list()
    palavra_inicial = random.choice(inicio)
    post.append(palavra_inicial)
    
    if (len(' '.join(post)) < caracteres):
        while (len(post) < (media_de_palavras-1)):
            i = 0
            for tupla in bigramas:
                if (tupla[0] == post[i] and tupla[1] != '<s>' and tupla[1] != '</s>'):
                    possibilidades = list()
                    possibilidades.append(tupla[1])
                    for tupla_tri in trigramas:
                        proxima_palavra = random.choice(possibilidades)
                        if (post[i] == tupla_tri[0] and proxima_palavra == tupla_tri[1] 
                        and tupla_tri[2] != '<s>' and tupla_tri[2] != '</s>'):
                            post.append(proxima_palavra)
                            possibilidades2 = list()
                            possibilidades2.append(tupla_tri[2])                        
                            proxima_palavra2 = random.choice(possibilidades2)
                            post.append(proxima_palavra2)
                            i = i + 2
        for tupla in bigramas:
            palavra_final = random.choice(final)
            if (post[-1] == tupla[0] and palavra_final == tupla[1]):
                post.append(palavra_final)
    
    return ' '.join(post)

post_final = gerar_texto(inicio_post, final_post, media, caracteres_max, bi, tri)

# EXTRAS
def dicionarios(lista):
    x = len(lista)
    x = x-1
    dicionario_hashtags = defaultdict(int)
    dicionario_usuarios = defaultdict(int)
    dicionario_palavras = defaultdict(int)
    while (x >= 0):
        if (lista[x][0] == '#'):
            dicionario_hashtags[lista[x]] += 1
        elif (lista[x][0] == '@'):
            dicionario_usuarios[lista[x]] += 1
        else:
            dicionario_palavras[lista[x]] += 1
        x = x - 1    
        
    return dicionario_hashtags, dicionario_usuarios, dicionario_palavras

hashtagsdic = dicionarios(texto_rede)[0]
usuariosdic = dicionarios(texto_rede)[1]

def listas_de_dicionarios(dicionarios):
    lista = list()
    for k, v in dicionarios.items():
        lista.append(k)
    return lista

hashtags = listas_de_dicionarios(hashtagsdic)
usuarios = listas_de_dicionarios(usuariosdic)     

print ('Nossa sugestão para o post: ', post_final)
print ('Média de palavras utilizadas por postagem na rede selecionada: ', media)
print ('Total de postagens avaliadas para gerar o resultado: ', len(posts_brutos_rede))
print ('Já pensou em marcar algum destes usuários? ', usuarios)
print ('Algumas hashtags em alta: ', hashtags )