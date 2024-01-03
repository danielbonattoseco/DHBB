# -*- coding: utf-8 -*-
"""
Este software foi gerado dentro do âmbito do projeto "Programação aplicada ao DHBB" pelo CPDOC/FGV.
Orientador: Profa. Dra. Jaqueline Porto Zulini (http://lattes.cnpq.br/4672784311890510)
Orientando/Desenvolvedor: Daniel Bonatto Seco (http://lattes.cnpq.br/8325397475123191)
Software sob MIT License. (https://opensource.org/license/mit/)
"""

### IMPORTAÇÃO DE BIBLIOTECAS
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import ImageTk, Image
from datetime import datetime
import locale
import ctypes
import json
import requests
import pickle
import webbrowser
import os

myappid = 'fgv.geradordeverbetes.0.1' #https://semver.org/
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

#%% CLASSES VERBETADO

"""
Cada módulo dentro da UI do software (com exceção da parte 1 - Identificação pessoal)
é definina por uma classe que possui seus respectivos atributos.
Cada classe possui uma função "construtor_paragrafo" que converte os atributos
em uma frase que será inserida no corpo do verbete.
As classes integram o objeto "Verbetado" que recebe todos os metadados.
"""
        
class AtuacaoImprensa():
    """Recebe os metadados do módulo 'Parte 7 - Atuação Legislativa' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 nome_jornal, 
                 funcao_exercida,
                 ano_inicio,
                 ano_fim):
        self.nome_jornal = str(nome_jornal)
        self.funcao_exercida = str(funcao_exercida)
        self.ano_inicio = str(ano_inicio)
        self.ano_fim = str(ano_fim)
        
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = 'Atuou no jornal ' \
        + self.nome_jornal \
        + (' como %s'%self.funcao_exercida.lower() if self.funcao_exercida else '') \
        + (' a partir de %s'%self.ano_inicio if self.ano_inicio else '') \
        + (' até %s'%self.ano_fim if self.ano_fim else '') \
        + '. '
        return paragrafo

#####

class Conjuge(): 
    """Recebe os metadados do módulo 'Parte 11 - Cônjuges' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 nome, 
                 tem_filhos,
                 qtd_filhos,
                 nome_filho):
        self.nome = str(nome)
        self.tem_filhos = tem_filhos
        self.qtd_filhos = str(qtd_filhos)
        self.nome_filhos = []
        
        for i in range(len(nome_filho)):
            if nome_filho[i] != '':
                self.nome_filhos.append(Conjuge.FilhoConjuge(nome_filho[i]))

    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = 'Casou-se com ' \
        + self.nome \
        + (', com quem teve %s filho%s'%(self.qtd_filhos,"s" if int(self.qtd_filhos) > 1 else '') \
        + ((": " + ", ".join([i.nome for i in self.nome_filhos[:-1]]) + " e " + self.nome_filhos[-1].nome) 
           if len(self.nome_filhos) > 1 and len(self.nome_filhos) == int(self.qtd_filhos)
           else (" incluindo " + ", ".join([i.nome for i in self.nome_filhos[:-1]]) + " e " + self.nome_filhos[-1].nome) 
           if len(self.nome_filhos) > 1
           else (" chamado %s"%self.nome_filhos[0].nome 
                 if len(self.nome_filhos) == 1 and int(self.qtd_filhos) == 1 
                 else " incluindo %s"%self.nome_filhos[0].nome if len(self.nome_filhos) == 1 else '')) if self.tem_filhos else '') \
        + '.\n'
        return paragrafo

    class FilhoConjuge():
        """Recebe os metadados do módulo 'Parte 11 - Cônjuges' 
        da UI referentes ao(s) filho(s) do verbetado e os converte 
        em uma subclasse da classe Conjuge."""
        def __init__(self,
                     nome):
            self.nome = nome

#####

class ObraAutor():
    """Recebe os metadados do módulo 'Parte 8 - Obras publicadas pelo verbetado' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 nome_obra,
                 ano_publicacao):
        self.nome_obra = str(nome_obra)
        self.ano_publicacao = str(ano_publicacao)
        
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = 'Publicou a obra "' \
        + self.nome_obra \
        + ('" em %s'%self.ano_publicacao if self.ano_publicacao else '') \
        + '. '
        return paragrafo

#####

class ObraSobre():
    """Recebe os metadados do módulo 'Parte 9 - Obras publicadas sobre o verbetado' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 nome_obra,
                 ano_publicacao):
        self.nome_obra = str(nome_obra)
        self.ano_publicacao = str(ano_publicacao)

    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = ('Em %s'%self.ano_publicacao if self.ano_publicacao else '') \
        + (' teve' if self.ano_publicacao else 'Teve') \
        + (' uma obra publicada em sua referência, intitulada "' \
        + self.nome_obra) \
        + '". '
        return paragrafo

#####

class Processo():
    """Recebe os metadados do módulo 'Parte 10 - Processos criminais concluidos e Condenações' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 processo,
                 n_processo,
                 motivo_processo,
                 condenado,
                 data_condenacao):
        self.processo = str(processo)
        self.n_processo = str(n_processo)
        self.motivo_processo = str(motivo_processo)
        self.condenado = condenado
        self.data_condenacao = str(data_condenacao)
        
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        if self.condenado:
            paragrafo = "Foi indiciad%s no processo"%('a' if dados_verbetado.genero == 'Feminino' else 'o') \
            + (' %s,'%self.processo if self.processo else '') \
            + (' número %s,'%self.n_processo if self.n_processo else '') \
            + (' movido por motivo de %s,'%self.motivo_processo.lower() if self.motivo_processo else '') \
            + ' do qual foi condenad%s'%('a' if dados_verbetado.genero == 'Feminino' else 'o') \
            + (' em %s'%self.data_condenacao if self.data_condenacao else '') \
            + '. '
            return paragrafo
        else:
            paragrafo = ''
            return paragrafo

#####

class BurocraciaEstatal():
    """Recebe os metadados do módulo 'Parte 6 - Trajetória na Burocracia Estatal' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 cargo_nomeado,
                 orgao,
                 data_nomeacao,
                 exonerado,
                 data_exoneracao,
                 motivo_exoneracao):
        self.cargo_nomeado = str(cargo_nomeado)
        self.orgao = str(orgao)
        self.data_nomeacao = str(data_nomeacao)
        self.exonerado = exonerado
        self.data_exoneracao = str(data_exoneracao)
        self.motivo_exoneracao = str(motivo_exoneracao)

    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = 'Foi nomead%s para o cargo de %s'%('a' if dados_verbetado.genero == 'Feminino' else 'o', self.cargo_nomeado) \
        + (' no %s'%self.orgao if self.orgao else '') \
        + (' em %s'%self.data_nomeacao if self.data_nomeacao else '') \
        + '. ' \
        + (('Foi exonerad%s do cargo'%('a' if dados_verbetado.genero == 'Feminino' else 'o') \
        + (' em %s'%self.data_exoneracao if self.data_exoneracao else '') \
        + (' por motivo de %s'%self.motivo_exoneracao if self.motivo_exoneracao else '') \
        + '. ') if self.exonerado else '')
        return paragrafo

#####

class Formacao():
    """Recebe os metadados do módulo 'Parte 3 - Formação Acadêmica' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 tipo,
                 curso,
                 instituicao,
                 uf,
                 municipio,
                 ano_inicio,
                 ano_conclusao):
        self.tipo = str(tipo)
        self.curso = str(curso)
        self.instituicao = str(instituicao)
        self.uf = str(uf)
        self.municipio = str(municipio)
        self.ano_inicio = str(ano_inicio)
        self.ano_conclusao = str(ano_conclusao)

    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = 'Cursou' \
        + (' o' if self.tipo in ['Ensino Fundamental','Ensino Médio'] else '') \
        + (' %s'%self.tipo.lower() if self.tipo else '') \
        + (' em %s'%self.curso.lower() if ((self.tipo in ['Graduação','Pós-Graduação','Especialização']) and self.curso) else '') \
        + (' na instituição %s'%self.instituicao if self.instituicao else '') \
        + (' em %s (%s)'%(self.municipio,list(siglas_estados.values())[list(siglas_estados.keys()).index(self.uf)] ) if (self.municipio and self.uf) else '') \
        + (' a partir de %s'%self.ano_inicio if self.ano_inicio else '') \
        + (' até %s'%self.ano_conclusao if self.ano_conclusao else '') \
        + '. '
        return paragrafo

#####

class Fonte():
    """Recebe os metadados do módulo 'Parte 12 - Fontes' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 autor,
                 titulo,
                 tipo,
                 URL,
                 data_acesso,
                 info_complementares):
        self.autor = str(autor)
        self.titulo = str(titulo)
        self.tipo = str(tipo)
        self.URL = str(URL)
        self.data_acesso = str(data_acesso)
        self.info_complementares = str(info_complementares)
        
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = "\n"
        if self.autor:
            autor_split = self.autor.split()
            if len(autor_split) > 1:
                autor_formatado = f"{autor_split[-1].upper()}, {' '.join(autor_split[:-1])}"
                paragrafo += (f'{autor_formatado}. ')
            else:
                paragrafo += (f'{self.autor.upper()}. ')
        paragrafo += (f'{self.titulo}. ' if self.titulo else '')
        paragrafo += (f'{self.info_complementares}. ' if self.info_complementares else '')
        if self.tipo == "Online":
            paragrafo += (f'Disponível em: {self.URL}. ' if self.URL else '')
            paragrafo += (f'Acesso em: {self.data_acesso}. ' if self.data_acesso else '')
        return paragrafo

#####

class ParentelaPolitica():
    """Recebe os metadados do módulo 'Parte 2 - Parentela Política' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 nome,
                 parentesco,
                 verbetado_dhbb,
                 cargo):
        self.nome = str(nome)
        self.parentesco = str(parentesco)
        self.verbetado_dhbb = str(verbetado_dhbb)
        self.cargos = []
        
        for i in range(len(cargo)):
            self.cargos.append(ParentelaPolitica.Cargo(cargo[i]))
            
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = self.parentesco.title() \
                    + " de " \
                    + self.nome
        
        if len(self.cargos) > 0 and self.cargos[0].cargo != '':
            paragrafo = paragrafo + ', que atuou como '
            for i, cargo in enumerate(self.cargos):
                if len(self.cargos) > 1 and i == len(self.cargos) - 1:
                    paragrafo = paragrafo + " e "
                paragrafo = paragrafo \
                + cargo.cargo.lower()
                if i == len(self.cargos) - 1:
                    paragrafo = paragrafo + ". "
                elif i != len(self.cargos) - 2:
                        paragrafo = paragrafo + ", "
        else:
            paragrafo = paragrafo + '. '
        return paragrafo
        
    class Cargo():
        """Recebe os metadados do módulo 'Parte 2 - Parentela Política' 
        da UI referentes ao(s) cargo(s) do parente do verbetado e os converte 
        em uma subclasse da classe Conjuge."""
        def __init__(self,
                     cargo):
            self.cargo = cargo

#####

class TrajetoriaPolitica():
    """Recebe os metadados do módulo 'Parte 4 - Trajetória Política' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 cargo,
                 ano,
                 partido,
                 votos,
                 eleito,
                 mandato,
                 renunciou_ao_cargo,
                 motivo_renuncia,
                 data_renuncia,
                 atuacoes_legislativas):
        self.cargo = str(cargo)
        self.ano = str(ano)
        self.partido = str(partido)
        self.votos = str(votos)
        self.eleito = eleito
        self.mandato = str(mandato)
        self.renunciou_ao_cargo = renunciou_ao_cargo
        self.motivo_renuncia = str(motivo_renuncia)
        self.data_renuncia = str(data_renuncia)
        self.atuacoes_legislativas = [atuacao
                                      for atuacao
                                      in atuacoes_legislativas
                                      if atuacao.trajetoria_relacionada ==
                                      self.cargo + " (" + self.mandato + ")"] # FILTRA APENAS AS ATUAÇÕES LEGISLATIVAS REFERENTES A CADA TRAJETÓRIA POLÍTICA RELACIONADA
        
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        if primeira_trajetoria_politica():
            paragrafo = '\nIniciou na vida política no ano de %s'%self.ano \
            + ' quando concorreu ao cargo de %s'%self.cargo \
            + (' pelo %s'%self.partido if self.partido else '') \
            + ', no qual' \
            + (' recebeu %s votos e'%self.votos if self.votos else '') \
            + (' %sconseguiu eleger-se.'%('' if self.eleito else 'não ')) \
            + ((' Renunciou ao cargo' \
            + (' em %s'%self.data_renuncia if self.data_renuncia else '') \
            + (' por motivo de %s'%self.motivo_renuncia.lower() if self.motivo_renuncia else '') \
            + '. ') if self.renunciou_ao_cargo else '')
            
            ###INSERIR ATUACOES LEGISLATIVAS
            if self.atuacoes_legislativas:
                if len(self.atuacoes_legislativas) > 1: #CASO HAJA MAIS DE UMA ATUAÇÃO LEGISLATIVA
                    
                    paragrafo += " Durante o exercício de seu mandato atuou nas seguintes funções legislativas: "
                    
                    for index, atuacao in enumerate(self.atuacoes_legislativas):
                        
                        paragrafo += "%i) "%(index + 1) \
                        + "%s"%(atuacao.nome.lower() if atuacao.nome else '') \
                        + (', %s'%atuacao.tipo.lower() if atuacao.tipo else '') \
                        + ((' n%s'%('a ' if atuacao.casa_legislativa == 'Câmara dos Deputados' else 'o ') \
                        + atuacao.casa_legislativa.lower()) if atuacao.casa_legislativa else '') \
                        + (', na função de %s'%atuacao.funcao.lower() if atuacao.funcao else '')
                        
                        if index == len(self.atuacoes_legislativas) - 1:
                            paragrafo += ".\n"
                        elif index == len(self.atuacoes_legislativas) - 2:
                            paragrafo += " e "
                        else:
                            paragrafo += ", "
                        
                else: #CASO HAJA APENAS UMA ATUAÇÃO LEGISLATIVA
                    
                    for atuacao in self.atuacoes_legislativas:
                        
                        paragrafo += " Durante o exercício de seu mandato atuou na %s"%(atuacao.nome.lower() if atuacao.nome else '') \
                        + (', %s'%atuacao.tipo.lower() if atuacao.tipo else '') \
                        + ((' n%s'%('a ' if atuacao.casa_legislativa == 'Câmara dos Deputados' else 'o ') \
                        + atuacao.casa_legislativa.lower()) if atuacao.casa_legislativa else '') \
                        + (', na função de %s'%atuacao.funcao.lower() if atuacao.funcao else '') \
                        + ".\n"
            else: #CASO NÃO HAJA ATUAÇÃO LEGISLATIVA
                paragrafo += "\n"

            return paragrafo
        
        else: #SEGUNDA TRAJETÓRIA POLÍTICA EM DIANTE
        
            paragrafo = 'Candidatou-se ao cargo de %s'%self.cargo \
            + (' nas eleições de %s'%self.ano if self.ano else '') \
            + (' pelo %s'%self.partido if self.partido else '') \
            + ', no qual' \
            + (' recebeu %s votos e'%self.votos if self.votos else '') \
            + (' %sconseguiu eleger-se.'%('' if self.eleito else 'não ')) \
            + ((' Renunciou ao cargo' \
            + (' em %s'%self.data_renuncia if self.data_renuncia else '') \
            + (' por motivo de %s'%self.motivo_renuncia.lower() if self.motivo_renuncia else '') \
            + '. ') if self.renunciou_ao_cargo else '')
                
            ###INSERIR ATUACOES LEGISLATIVAS
            if self.atuacoes_legislativas:
                if len(self.atuacoes_legislativas) > 1: #CASO HAJA MAIS DE UMA ATUAÇÃO LEGISLATIVA
                    
                    paragrafo += " Durante o exercício de seu mandato atuou nas seguintes funções legislativas: "
                    
                    for index, atuacao in enumerate(self.atuacoes_legislativas):
                        
                        paragrafo += "%i) "%(index + 1) \
                        + "%s"%(atuacao.nome.lower() if atuacao.nome else '') \
                        + (', %s'%atuacao.tipo.lower() if atuacao.tipo else '') \
                        + ((' n%s'%('a ' if atuacao.casa_legislativa == 'Câmara dos Deputados' else 'o ') \
                        + atuacao.casa_legislativa.lower()) if atuacao.casa_legislativa else '') \
                        + (', na função de %s'%atuacao.funcao.lower() if atuacao.funcao else '')
                        
                        if index == len(self.atuacoes_legislativas) - 1:
                            paragrafo += ".\n"
                        elif index == len(self.atuacoes_legislativas) - 2:
                            paragrafo += " e "
                        else:
                            paragrafo += ", "
                        
                else: #CASO HAJA APENAS UMA ATUAÇÃO LEGISLATIVA
                    
                    for atuacao in self.atuacoes_legislativas:
                        
                        paragrafo += " Durante o exercício de seu mandato atuou na %s"%(atuacao.nome.lower() if atuacao.nome else '') \
                        + (', %s'%atuacao.tipo.lower() if atuacao.tipo else '') \
                        + ((' n%s'%('a ' if atuacao.casa_legislativa == 'Câmara dos Deputados' else 'o ') \
                        + atuacao.casa_legislativa.lower()) if atuacao.casa_legislativa else '') \
                        + (', na função de %s'%atuacao.funcao.lower() if atuacao.funcao else '') \
                        + ".\n"

            else: #CASO NÃO HAJA ATUAÇÃO LEGISLATIVA
                paragrafo += "\n" 
            
            return paragrafo

#FUNÇÕES PARA REDIGIR DE FORMA DIFERENTE A PRIMEIRA TRAJETORIA POLITICA 
def primeira_trajetoria_politica():
    """Cria uma flag no primeiro objeto do tipo 'TrajetoriaPolitica'
    para que o mesmo seja redigido de forma diferente, em conformidade
    com o Manual de Redação de Verbetes."""
    if hasattr(primeira_trajetoria_politica, "flag"):
        pass
    else:
        primeira_trajetoria_politica.flag = True
        return True
    return False

def atualizar_primeira_trajetoria_politica():
    """Elimina a flag assim que a primeira trajetória política é redigida."""
    if hasattr(primeira_trajetoria_politica, "flag"):
        del primeira_trajetoria_politica.flag

#####

class AtuacaoLegislativa():
    """Recebe os metadados do módulo 'Parte 5 - Atuação Legislativa' 
    da UI e os converte em um parágrafo formatado do verbete."""
    def __init__(self,
                 nome,
                 trajetoria_relacionada,
                 tipo,
                 casa_legislativa,
                 funcao):
        self.tipo = str(tipo)
        self.casa_legislativa = str(casa_legislativa)
        self.nome = str(nome)
        self.funcao = str(funcao)
        self.trajetoria_relacionada = str(trajetoria_relacionada)
        
    def construtor_paragrafo(self):
        """Converte os metadados da classe em um parágrafo formatado do verbete"""
        paragrafo = ('Durante o exercício de seu mandato como %s '%self.trajetoria_relacionada.lower() if self.trajetoria_relacionada else '') \
        + ('%stuou na %s'%('a' if self.trajetoria_relacionada else 'A', self.nome.lower() if self.nome else '')) \
        + (', %s'%self.tipo.lower() if self.tipo else '') \
        + ((' n%s'%('a ' if self.casa_legislativa == 'Câmara dos Deputados' else 'o ') \
        + self.casa_legislativa.lower()) if self.casa_legislativa else '') \
        + (', na função de %s'%self.funcao.lower() if self.funcao else '') \
        + '. '
        return paragrafo

#####

class Verbetado():
    """
    Classe principal que reúne todos os metadados do verbetado, 
    incluindo as subclasses dos módulos presentes na UI.
    """ 
    def __init__(self, atua_impren, atua_legis, buroc_estat,
                 causa_fal, conjuges, data_fal, data_nasc, fontes,
                 formacoes, genero, mun_fal, mun_nasc, nome_civ,
                 nome_mae, nome_pai, nome_pol, nome_soc, obras_autor,
                 obras_sobre, parent_pol, processos, prof_mae, prof_pai,
                 trajet_pol, uf_fal, uf_nasc, tipo_verbete, nome_autor_verbete):

        self.atua_impren = []
        for i in range(len(atua_impren[0])):
            if atua_impren[0][i].get(): #Campo obrigatório
                self.atua_impren.append(AtuacaoImprensa(str(atua_impren[0][i].get()),
                                                        str(atua_impren[1][i].get()),
                                                        str(atua_impren[2][i].get()),
                                                        str(atua_impren[3][i].get())))
        self.atua_legis = []
        for i in range(len(atua_legis[0])):
            if atua_legis[0][i].get(): #Campo obrigatório
                self.atua_legis.append(AtuacaoLegislativa(str(atua_legis[0][i].get()),
                                                          str(atua_legis[1][i].get()),
                                                          str(atua_legis[2][i].get()),
                                                          str(atua_legis[3][i].get()),
                                                          str(atua_legis[4][i].get())))

        self.buroc_estat = []
        for i in range(len(buroc_estat[0])):
            if buroc_estat[0][i].get(): #Campo obrigatório
                self.buroc_estat.append(BurocraciaEstatal(str(buroc_estat[0][i].get()),
                                                          str(buroc_estat[1][i].get()),
                                                          str(buroc_estat[2][i].get()),
                                                          buroc_estat[3][i].get(),
                                                          str(buroc_estat[4][i].get()),
                                                          str(buroc_estat[5][i].get())))
                
        self.conjuges = []
        for i in range(len(conjuges[0])):
            if conjuges[0][i].get(): #Campo obrigatório
                self.conjuges.append(Conjuge(str(conjuges[0][i].get()),
                                             conjuges[1][i].get(),
                                             str(conjuges[2][i].get()),
                                             [str(item.get()) for item in conjuges[3][i]]))

        self.fontes = []
        for i in range(len(fontes[0])):
            if fontes[1][i].get(): #Campo obrigatório
                self.fontes.append(Fonte(str(fontes[0][i].get()),
                                         str(fontes[1][i].get()),
                                         str(fontes[2][i].get()),
                                         str(fontes[3][i].get()),
                                         str(fontes[4][i].get()),
                                         str(fontes[5][i].get())))

        self.formacoes = []
        for i in range(len(formacoes[0])):
            if formacoes[0][i].get(): #Campo obrigatório
                self.formacoes.append(Formacao(str(formacoes[0][i].get()),
                                               str(formacoes[1][i].get()),
                                               str(formacoes[2][i].get()),
                                               str(formacoes[3][i].get()),
                                               str(formacoes[4][i].get()),
                                               str(formacoes[5][i].get()),
                                               str(formacoes[6][i].get())))

        self.obras_autor = []
        for i in range(len(obras_autor[0])):
            if obras_autor[0][i].get(): #Campo obrigatório
                self.obras_autor.append(ObraAutor(str(obras_autor[0][i].get()),
                                                  str(obras_autor[1][i].get())))

        self.obras_sobre = []
        for i in range(len(obras_sobre[0])):
            if obras_sobre[0][i].get(): #Campo obrigatório
                self.obras_sobre.append(ObraSobre(str(obras_sobre[0][i].get()),
                                                  str(obras_sobre[1][i].get())))

        self.parent_pol = []
        for i in range(len(parent_pol[0])):
            if parent_pol[0][i].get(): #Campo obrigatório
                self.parent_pol.append(ParentelaPolitica(str(parent_pol[0][i].get()),
                                                         str(parent_pol[1][i].get()),
                                                         str(parent_pol[2][i].get()),
                                                         [str(item.get()) for item in parent_pol[3][i]]))

        self.processos = []
        for i in range(len(processos[0])):
            if processos[0][i].get(): #Campo obrigatório
                self.processos.append(Processo(str(processos[0][i].get()),
                                               str(processos[1][i].get()),
                                               str(processos[2][i].get()),
                                               processos[3][i].get(),
                                               str(processos[4][i].get())))

        self.trajet_pol = []
        for i in range(len(trajet_pol[0])):
            if trajet_pol[0][i].get(): #Campo obrigatório
                self.trajet_pol.append(TrajetoriaPolitica(str(trajet_pol[0][i].get()),
                                                          str(trajet_pol[1][i].get()),
                                                          str(trajet_pol[2][i].get()),
                                                          str(trajet_pol[3][i].get()),
                                                          trajet_pol[4][i].get(),
                                                          str(trajet_pol[5][i].get()),
                                                          trajet_pol[6][i].get(),
                                                          str(trajet_pol[7][i].get()),
                                                          str(trajet_pol[8][i].get()),
                                                          self.atua_legis))

        self.causa_fal = causa_fal.get()
        self.data_fal = data_fal.get()
        self.data_nasc = data_nasc.get()
        self.genero = genero.get() if genero.get() != 'Selecione' else ''
        self.mun_fal = mun_fal.get()
        self.mun_nasc = mun_nasc.get()
        self.nome_civ = nome_civ.get()
        self.nome_mae = nome_mae.get()
        self.nome_pai = nome_pai.get()
        self.nome_pol = nome_pol.get()
        self.nome_soc = nome_soc.get()
        self.prof_mae = prof_mae.get()
        self.prof_pai = prof_pai.get()
        self.causa_fal = causa_fal.get()
        self.data_fal = data_fal.get()
        self.data_nasc = data_nasc.get()
        self.uf_fal = uf_fal.get() if uf_fal.get() != 'Selecione' else ''
        self.uf_nasc = uf_nasc.get() if uf_nasc.get() != 'Selecione' else ''
        self.tipo_verbete = tipo_verbete.get()
        self.nome_autor_verbete = nome_autor_verbete.get()
      
    def toJSON(self):
        """Exporta um arquivo .json contendo os metadados do objeto Verbetado"""
        return json.dumps(self, 
                          default=lambda o: o.__dict__,
                          sort_keys=True, 
                          indent=4, 
                          ensure_ascii=False)
        
#%% CLASSES DO SISTEMA
class Date():
    """Recebe os valores do input_data gerados pela funçào criar_input_data,
    realiza as validações necessárias e converte os valores em uma string formatada."""
    def __init__(self, 
                 dia, 
                 mes, 
                 ano):
        
        self.dia = dia
        self.mes = mes
        self.ano = ano

    def get(self):
        """Fornece a string formatada de data a partir dos dados inputados na UI."""
        dia = int(self.dia.get()) if len(self.dia.get()) > 0 else None
        mes = int(self.mes.get()) if len(self.mes.get()) > 0 else None
        ano = int(self.ano.get()) if len(self.ano.get()) > 0 else None
        
        dia_valido = False
        mes_valido = False
        ano_valido = False
        
        data_formatada = ""
        
        if dia is not None:
            if not (1 <= dia <= 31):
                tk.messagebox.showerror("Erro","O dia deve estar entre 1 e 31")
            else:
                dia_valido = True
        if mes is not None:
            if not (1 <= mes <= 12):
                tk.messagebox.showerror("Erro","O mês deve estar entre 1 e 12")
            else:
                mes_valido = True
        if ano is not None and len(str(ano)) >= 4:
            if not (1900 <= ano <= datetime.now().year):
                tk.messagebox.showerror("Erro",f"O ano deve estar entre 1900 e {datetime.now().year}")
            else:
                ano_valido = True

        if dia_valido and mes_valido and ano_valido:
            data_formatada += f"{dia:02d}/"
        if mes_valido and ano_valido:
            data_formatada += f"{mes:02d}/"
        if ano_valido:
            data_formatada += f"{ano:04d}"
                
        self.data = data_formatada.strip("/")

        return self.data

def criar_input_data(parent_frame):
    """Os objetos de data na UI do software foram desenvolvidas de forma a permitir
    ao pesquisador inserir apenas as informaçòes que possuir (apenas ano, mês/ano ou dia/mês/ano).
    Esta funçào cria um frame com todos os objetos necessários para que possam ser
    posicionados na UI como um widget padrão."""
    frame_data = tk.Frame(parent_frame)
    dia = tk.StringVar()
    mes = tk.StringVar()
    ano = tk.StringVar()

    entry_dia = ttk.Combobox(frame_data,
                         textvariable=dia,
                         state="readonly",
                         width=2,
                         font=('Roboto', 11),
                         justify="center",
                         values = [""] + list(range(1, 32)))
    entry_dia.pack(side="left")
    CreateToolTip(entry_dia,
          text='Dia (deixar vazio caso não possuir a informação)') 
    
    tk.Label(frame_data,
             text='/',
             font=('Roboto', 12)).pack(side="left")
    
    entry_mes = ttk.Combobox(frame_data,
                         textvariable=mes,
                         state="readonly",
                         width=2,
                         font=('Roboto', 11),
                         justify="center",
                         values = [""] + list(range(1, 13)))
    entry_mes.pack(side="left")
    CreateToolTip(entry_mes,
          text='Mês (deixar vazio caso não possuir a informação)') 
    
    tk.Label(frame_data,
             text='/',
             font=('Roboto', 12)).pack(side="left")
    
    entry_ano = ttk.Combobox(frame_data,
                         textvariable=ano,
                         state="readonly",
                         width=4,
                         font=('Roboto', 11),
                         justify="center",
                         values = [''] + list(range(1900,datetime.now().year+1))[::-1])
    entry_ano.pack(side="left")
    CreateToolTip(entry_ano,
          text='Ano (deixar vazio caso não possuir a informação)') 
    
    data = Date(dia, 
                mes, 
                ano)
    
    entry_dia.bind("<Key>", validar_input_numeros)
    entry_mes.bind("<Key>", validar_input_numeros)
    entry_ano.bind("<Key>", validar_input_numeros)

    return frame_data,data

######

class ToolTip():
    """Exibe a caixa de informações sobre cada metadado na UI com mouseover."""
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        """Exibe a caixa de informações"""
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """Elimina a caixa de informações"""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
            
def CreateToolTip(widget, text):
    """Função para criar a caixa de informações a partir da classe ToolTip"""
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

######

def construtor_verbete(event):
    """Bindado a todos os eventos na UI (digitação, modificação de campos, cliques etc.).
    Chama funçòes nnecessárias para atualizaçòes na UI e em metadados relacionados,
    constrói o objeto Verbetado a partir dos metadados forecidos na UI
    e constrói o verbete chamando as funções necessárias em todos os objetos do objeto Verbetado."""
    
    global dados_verbetado
    
    # CALL FUNÇOES PARA ATUALIZAÇÃO DE CAMPOS/ITENS DA UI
    
    atualizar_cbox_trajetorias()
    atualizar_primeira_trajetoria_politica()
    campos_obrigatorios(event)
    foi_eleito()
        
    #CONSTRUÇÃO DO OBJETO Verbetado
    
    dados_verbetado = Verbetado(input_atua_impren, input_atua_legis, input_buroc_estat,
                                input_causa_fal, input_conjuges, input_data_fal,
                                input_data_nasc, input_fontes, input_formacoes, input_genero,
                                input_mun_fal, input_mun_nasc, input_nome_civ, input_nome_mae,
                                input_nome_pai, input_nome_pol, input_nome_soc, input_obras_autor,
                                input_obras_sobre, input_parent_pol, input_processos,
                                input_prof_mae, input_prof_pai, input_trajet_pol,
                                input_uf_fal, input_uf_nasc, tipo_verbete, input_nome_autor_verbete)

    # REGRA QUE IMPEDE A REDAÇÃO DE QUALQUER ITEM DO VERBETE SEM O NOME CIVIL DO MESMO
    
    if not dados_verbetado.nome_civ:
        string_verbete.set('Nome civil do verbetado obrigatório.')
        text_frame_previa.delete("1.0", "end")
        text_frame_previa.insert(tk.END,string_verbete.get(),'warning')
        return None

    # REDAÇÃO CABEÇALHO DE METADADOS
    
    nome_cabecalho = (dados_verbetado.nome_pol 
                      if dados_verbetado.nome_pol
                      else dados_verbetado.nome_soc 
                      if dados_verbetado.nome_soc
                      else dados_verbetado.nome_civ)
    
    cabecalho = f"---\ntitle: {nome_cabecalho.split()[-1].upper()}" \
                f"""{", " + ' '.join(word for word in nome_cabecalho.split()[:-1]) 
                if len(' '.join(word 
                                for word 
                                in nome_cabecalho.split()[:-1])) > 0 
                else ''}""" \
                f"\nnatureza: Biográfico" \
                f"""\nsexo: {dados_verbetado.genero[0].lower() 
                if dados_verbetado.genero 
                in ['Feminino','Masculino'] 
                else ''}""" \
                f"\n---\n\n"

    # REDAÇÃO PARAGRAFO DE INTRODUCAO
                
    paragrafo_introducao = f"«{dados_verbetado.nome_civ.title()}»" \
        + (' nasceu' 
               if dados_verbetado.data_nasc
               or dados_verbetado.mun_nasc
               else '') \
        + ((f' em {dados_verbetado.mun_nasc}' 
          + ' (' 
          + list(siglas_estados.values())[list(siglas_estados.keys()).index(dados_verbetado.uf_nasc)] 
          + ')') 
             if dados_verbetado.uf_nasc
             and dados_verbetado.mun_nasc
             else '') \
        + (" em" + \
        (' %s de'%(data_nasc.dia.get()) if data_nasc.dia.get() else '') \
        + (' %s de'%(datetime.strptime(data_nasc.mes.get(), "%m").strftime("%B")) if data_nasc.mes.get() else '') \
        + (' %s'%(data_nasc.ano.get()) if data_nasc.ano.get() else '') 
            if dados_verbetado.data_nasc
            else '') \
        + ((f", filh{'a' if dados_verbetado.genero == 'Feminino' else 'o'} de " +
            (f"{dados_verbetado.nome_mae}" if dados_verbetado.nome_mae else '')  +
            (', ' +
            dados_verbetado.prof_mae 
            if dados_verbetado.prof_mae
            and dados_verbetado.nome_mae
            else '') +
           (' e ' if dados_verbetado.nome_mae
           and dados_verbetado.nome_pai
           else '') + 
           (f"{dados_verbetado.nome_pai if len(dados_verbetado.nome_pai) > 0 else ''}"))
           if dados_verbetado.nome_mae
           or dados_verbetado.nome_pai
           else '') + \
            (', ' +
            dados_verbetado.prof_pai 
            if dados_verbetado.prof_pai 
            and dados_verbetado.nome_pai
            else '') \
        + '. '
        
    paragrafo_introducao += ''.join([parentela_politica.construtor_paragrafo() for parentela_politica in dados_verbetado.parent_pol])

    # REDAÇÃO PARAGRAFOS INTERMEDIARIOS ORGANIZADOS EM ORDEM CRONOLÓGICA
    
    paragrafo_intermediario = ''
    
    lista_ordem_cronologica = []
    for i in dados_verbetado.atua_impren:
        lista_ordem_cronologica.append((i, i.ano_inicio))
    for i in dados_verbetado.buroc_estat:
        lista_ordem_cronologica.append((i, i.data_nomeacao[-4:]))
    for i in dados_verbetado.formacoes:
        lista_ordem_cronologica.append((i, i.ano_inicio))
    for i in dados_verbetado.processos:
        lista_ordem_cronologica.append((i, i.data_condenacao[-4:]))
    for i in dados_verbetado.trajet_pol:
        lista_ordem_cronologica.append((i, i.ano))
           
    lista_ordem_cronologica.sort(key = lambda t: (t[1] == '', t[1]))
    
    lista_ordem_cronologica_obras = []
    for i in dados_verbetado.obras_autor:
        lista_ordem_cronologica_obras.append((i, i.ano_publicacao[-4:]))
    for i in dados_verbetado.obras_sobre:
        lista_ordem_cronologica_obras.append((i, i.ano_publicacao[-4:]))

    lista_ordem_cronologica_obras.sort(key = lambda t: (t[1] == '', t[1]))
    
    for i in lista_ordem_cronologica:
        paragrafo_intermediario += i[0].construtor_paragrafo()
    for i in lista_ordem_cronologica_obras:
        paragrafo_intermediario += i[0].construtor_paragrafo()

    #REDAÇÃO PARÁGRAFO DE CÔNJUGES/FILHOS
    
    for i in dados_verbetado.conjuges:
        paragrafo_intermediario += i.construtor_paragrafo()

    # REDAÇÃO PARAGRAFO DE FALECIMENTO    
    
    if dados_verbetado.data_fal or dados_verbetado.mun_fal:            
        paragrafo_falecimento = "Faleceu em" \
        + (' %s de'%(data_fal.dia.get()) if data_fal.dia.get() else '') \
        + (' %s de'%(datetime.strptime(data_fal.mes.get(), "%m").strftime("%B")) if data_fal.mes.get() else '') \
        + (' %s'%(data_fal.ano.get()) if data_fal.ano.get() else '') \
        + ((f' em {dados_verbetado.mun_fal}' 
          + ' (' 
          + list(siglas_estados.values())[list(siglas_estados.keys()).index(dados_verbetado.uf_fal)] 
          + ')') 
         if dados_verbetado.uf_fal
         and dados_verbetado.mun_fal
         else '') \
        + '. '
    else:
        paragrafo_falecimento = ''
        
    # REDAÇÃO METADADOS FINAIS
    
    paragrafo_metadados = ''
    
    if dados_verbetado.nome_autor_verbete:
        paragrafo_metadados += f"\n\n*{dados_verbetado.nome_autor_verbete} (colaboração)"
    
    if dados_verbetado.fontes:
        paragrafo_metadados += "\n\nFONTES:"
        for fonte in dados_verbetado.fontes:
            paragrafo_metadados += fonte.construtor_paragrafo()
    
    # CONVERTER TODOS OS PARÁGRAFOS GERADOS EM UMA ÚNICA STRING
    
    string_verbete.set(cabecalho + 
                       paragrafo_introducao +
                       paragrafo_intermediario +
                       paragrafo_falecimento + 
                       paragrafo_metadados)
    
    #INSERIR A STRINNG NA PRÉVIA DA UI
    
    text_frame_previa.delete("1.0", "end")
    text_frame_previa.insert(tk.END,string_verbete.get())
    
    return string_verbete.get()


#%% CRIAÇÃO DE FRAMES PARA OS METADADOS NA UI
#%%  Parte 2 - Parentela Política

label_parent_pol = [[],[],[],[]]
input_parent_pol = [[],[],[],[]]
entry_parent_pol = [[],[],[],[]]
frames_parent_pol = []

def criar_widgets_parent_pol():
    """Cria os widgets da 'Parte 2 - Parentela Política'"""
    frames_parent_pol.append(tk.LabelFrame(frame_parte2,
                                       text='Parente Político {}'.format(len(frames_parent_pol)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte2.winfo_screenwidth()))
    frames_parent_pol[-1].grid(row=len(frames_parent_pol)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)
    
    #NOME
    label_parent_pol[0].append(tk.Label(frames_parent_pol[-1],
                       text='Nome:',
                       font=('Roboto', 12)))
    label_parent_pol[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e',
                                padx=(10, 0))

    input_parent_pol[0].append(tk.StringVar(root))

    entry_parent_pol[0].append(tk.Entry(frames_parent_pol[-1],
                                    textvariable = input_parent_pol[0][-1],
                                    font = ('Roboto', 12)))
    entry_parent_pol[0][-1].mandatory = True
    entry_parent_pol[0][-1].config(bg="#ffffea")
    entry_parent_pol[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_parent_pol[0][-1],
                  text='Nome do parente do político verbetado.')

    #PARENTESCO
    label_parent_pol[1].append(tk.Label(frames_parent_pol[-1],
                       text='Parentesco:',
                       font=('Roboto', 12)))
    label_parent_pol[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e',
                                padx=(68, 0))

    input_parent_pol[1].append(tk.StringVar(root))

    entry_parent_pol[1].append(AutocompleteCombobox(frames_parent_pol[-1],
                                                    font=('Roboto', 12),
                                                    textvariable = input_parent_pol[1][-1]))

    entry_parent_pol[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_parent_pol[1][-1],
                  text='Tipo de parentesco com o político verbetado.')
    
    #VERBETADO NO DHBB?
    label_parent_pol[2].append(tk.Label(frames_parent_pol[-1],
                       text='Verbetado no DHBB?',
                       font=('Roboto', 12)))
    label_parent_pol[2][-1].grid(row=0,
                                column=4,
                                sticky = 'e',
                                padx=(0, 0))

    input_parent_pol[2].append(tk.IntVar(root))

    entry_parent_pol[2].append(tk.Checkbutton(frames_parent_pol[-1],
                                           variable=input_parent_pol[2][-1],
                                           onvalue=1,
                                           offvalue=0))
    entry_parent_pol[2][-1].extra = 'check_verbetado%i'%len(input_parent_pol[2])
    entry_parent_pol[2][-1].grid(row=0,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_parent_pol[2][-1],
                  text='Ative caso o parente do político verbetado mencionado possua um verbete ativo no DHBB.')

    label_parent_pol[3].append([])
    input_parent_pol[3].append([])
    entry_parent_pol[3].append([])

    #CARGO
    label_parent_pol[3][-1].append(tk.Label(frames_parent_pol[-1],
                       text='Cargo:',
                       font=('Roboto', 12)))
    label_parent_pol[3][-1][-1].grid(row=1,
                                column=0,
                                sticky = 'e')

    input_parent_pol[3][-1].append(tk.StringVar(root))

    entry_parent_pol[3][-1].append(tk.Entry(frames_parent_pol[-1],
                                    textvariable = input_parent_pol[3][-1][-1],
                                    font = ('Roboto', 12)))
    entry_parent_pol[3][-1][-1].grid(row=1,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_parent_pol[3][-1][-1],
                  text='Cargo do parente do político verbetado.')

    #ATUALIZA A ONTOLOGIA DE PARENTESCO A PARTIR DO GÊNERO DO VERBETADO
    
    func_genero() 
    
    # ADICIONAR CARGO AO PARENTE POLITICO
    
    botao_adicionar_atuacao_parente = tk.Button(frames_parent_pol[-1], 
                                                text="Adicionar Cargo",
                                                bg='#d8ffc5',
                                                width = 15,
                                                font=('Roboto', 8, 'bold'),
                                                command=lambda frame=frames_parent_pol[-1]: adicionar_atuacao_parente(frame))
    
    botao_adicionar_atuacao_parente.grid(row=0, 
                                         column=6,
                                         padx=(20,0))

def adicionar_atuacao_parente(frame):
    """Adiciona mais um possível cargo a um parente político dentro do mesmo frame."""
    row = frame.grid_size()[1] + 1
    
    x = int(frame.cget("text").split()[2]) - 1
    
    #CARGO
    label_parent_pol[3][x].append(tk.Label(frame,
                       text=f'Cargo {len(entry_parent_pol[3][x])+1}:',
                       font=('Roboto', 12)))
    label_parent_pol[3][x][-1].grid(row=row,
                                column=0,
                                sticky = 'e')

    input_parent_pol[3][x].append(tk.StringVar(root))

    entry_parent_pol[3][x].append(tk.Entry(frame,
                                    textvariable = input_parent_pol[3][x][-1],
                                    font = ('Roboto', 12)))
    entry_parent_pol[3][x][-1].grid(row=row,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_parent_pol[3][x][-1],
                  text='Cargo do parente do político verbetado.')

def deletar_widgets_parent_pol():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_parent_pol) > 0:
        for x in range(0,len(entry_parent_pol)):
            if hasattr(entry_parent_pol[x][-1], '__iter__'):
                for entry_cargo in entry_parent_pol[x][-1]:
                    entry_cargo.destroy()
                for label_cargo in label_parent_pol[x][-1]:
                    label_cargo.destroy()
            else:
                entry_parent_pol[x][-1].destroy()
                label_parent_pol[x][-1].destroy()
                
            entry_parent_pol[x].pop(-1)
            input_parent_pol[x].pop(-1)
            label_parent_pol[x].pop(-1)
        frames_parent_pol[-1].destroy()
        frames_parent_pol.pop(-1)

#%%  Parte 3 - Formação Acadêmica

label_formacoes = [[],[],[],[],[],[],[]]
input_formacoes = [[],[],[],[],[],[],[]]
entry_formacoes = [[],[],[],[],[],[],[]]
frames_formacoes = []

def criar_widgets_formacao():
    """Cria os widgets da 'Parte 3 - Formação Acadêmica'"""
    # .TIPO DE FORMACAO
    tipos_formacao = ['','Ensino Fundamental','Ensino Médio','Graduação','Pós-Graduação','Especialização']

    frames_formacoes.append(tk.LabelFrame(frame_parte3,
                                       text='Formação {}'.format(len(frames_formacoes)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte3.winfo_width()))
    frames_formacoes[-1].grid(row=len(frames_formacoes)+1,
                              column=0,
                              columnspan=1000)

    label_formacoes[0].append(tk.Label(frames_formacoes[-1],
                       text='Tipo:',
                       font=('Roboto', 12)))
    label_formacoes[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_formacoes[0].append(tk.StringVar(root))

    entry_formacoes[0].append(ttk.Combobox(frames_formacoes[-1],
                                           state='readonly',
                                           height='6',
                                           font=('Roboto', 11),
                                           background="#ffffea",
                                           textvariable=input_formacoes[0][-1],
                                           values=tipos_formacao))
    entry_formacoes[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_formacoes[0][-1],
                  text='Tipo de Formação')

    #CURSO
    label_formacoes[1].append(tk.Label(frames_formacoes[-1],
                       text='Curso:',
                       font=('Roboto', 12)))
    label_formacoes[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_formacoes[1].append(tk.StringVar(root))

    entry_formacoes[1].append(tk.Entry(frames_formacoes[-1],
                                    textvariable = input_formacoes[1][-1],
                                    font = ('Roboto', 12)))
    entry_formacoes[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_formacoes[1][-1],
                  text="Nome do curso realizado pelo verbetado.\nExemplo: Administração de Empresas, Ciência Política, etc.")


    #INSTITUICAO
    label_formacoes[2].append(tk.Label(frames_formacoes[-1],
                       text='Instituição:',
                       font=('Roboto', 12)))
    label_formacoes[2][-1].grid(row=0,
                                column=4,
                                sticky = 'e')

    input_formacoes[2].append(tk.StringVar(root))

    entry_formacoes[2].append(tk.Entry(frames_formacoes[-1],
                                    textvariable = input_formacoes[2][-1],
                                    font = ('Roboto', 12)))
    entry_formacoes[2][-1].grid(row=0,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_formacoes[2][-1],
                  text='Nome da instituição de ensino onde o verbetado concluiu a formação.')

    #ESTADO
    label_formacoes[3].append(tk.Label(frames_formacoes[-1],
                        text='UF:',
                        font=('Roboto', 12)))
    label_formacoes[3][-1].grid(row=1,
                                column=0,
                                sticky = 'e',
                                padx=2,
                                pady=2)

    input_formacoes[3].append(tk.StringVar())
    input_formacoes[3][-1].set("Selecione")
    input_formacoes[3][-1].trace("w", get_municipios)

    entry_formacoes[3].append(tk.OptionMenu(frames_formacoes[-1],
                              input_formacoes[3][-1],
                              *estados_br_lista))
    entry_formacoes[3][-1].config(font=('Roboto', 10))
    entry_formacoes[3][-1].grid(row=1,
                                column=1,
                                sticky = 'w',
                                padx=2,
                                pady=2)
    CreateToolTip(entry_formacoes[3][-1],
                  text='Estado da instituição de ensino onde o verbetado concluiu a formação.')

    #MUNICIPIO
    label_formacoes[4].append(tk.Label(frames_formacoes[-1],
                       text='Município:',
                       font=('Roboto', 12)))
    label_formacoes[4][-1].grid(row=1,
                                column=2,
                                sticky = 'e')

    input_formacoes[4].append(tk.StringVar(root))

    entry_formacoes[4].append(AutocompleteCombobox(frames_formacoes[-1],
                                          font=('Roboto', 12),
                                          textvariable = input_formacoes[4][-1],
                                          completevalues=['']))

    entry_formacoes[4][-1].grid(row=1,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_formacoes[4][-1],
                  text='Município da instituição de ensino onde o verbetado concluiu a formação.')

    #ANO INICIO
    label_formacoes[5].append(tk.Label(frames_formacoes[-1],
                       text='Ano Inicio:',
                       font=('Roboto', 12)))
    label_formacoes[5][-1].grid(row=2,
                                column=0,
                                sticky = 'e')

    input_formacoes[5].append(tk.StringVar(root))

    entry_formacoes[5].append(ttk.Combobox(frames_formacoes[-1],
                                           state='readonly',
                                           width='6',
                                           font=('Roboto', 11),
                                           textvariable=input_formacoes[5][-1],
                                           values = [''] + list(range(1900,datetime.now().year+1))[::-1]))

    entry_formacoes[5][-1].grid(row=2,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_formacoes[5][-1],
                  text='Ano de inicio da formação.')

    #ANO CONCLUSAO
    label_formacoes[6].append(tk.Label(frames_formacoes[-1],
                       text='Ano Conclusão:',
                       font=('Roboto', 12)))
    label_formacoes[6][-1].grid(row=2,
                                column=2,
                                sticky = 'e')

    input_formacoes[6].append(tk.StringVar(root))

    entry_formacoes[6].append(ttk.Combobox(frames_formacoes[-1],
                                           state='readonly',
                                           width='6',
                                           font=('Roboto', 11),
                                           textvariable=input_formacoes[6][-1],
                                           values = [''] + list(range(1900,datetime.now().year+1))[::-1]))

    entry_formacoes[6][-1].grid(row=2,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_formacoes[6][-1],
                  text='Ano de conclusão da formação.')

def deletar_widgets_formacao():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_formacoes) > 0:
        for x in range(0,len(entry_formacoes)):
            entry_formacoes[x][-1].destroy()
            label_formacoes[x][-1].destroy()

            entry_formacoes[x].pop(-1)
            input_formacoes[x].pop(-1)
            label_formacoes[x].pop(-1)
        frames_formacoes[-1].destroy()
        frames_formacoes.pop(-1)

#%%  Parte 4 - Trajetória Política

label_trajet_pol = [[],[],[],[],[],[],[],[],[]]
input_trajet_pol = [[],[],[],[],[],[],[],[],[]]
entry_trajet_pol = [[],[],[],[],[],[],[],[],[]]
frames_trajet_pol = []

def criar_widgets_trajet_pol():
    """Cria os widgets da 'Parte 4 - Trajetória Política'"""
    frames_trajet_pol.append(tk.LabelFrame(frame_parte4,
                                       text='Trajetória {}'.format(len(frames_trajet_pol)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=root.winfo_width()))

    frames_trajet_pol[-1].grid(row=len(frames_trajet_pol)+1,
                               column=0,
                                columnspan=1000,
                                rowspan=1,
                              sticky='we')

    #CARGO
    label_trajet_pol[0].append(tk.Label(frames_trajet_pol[-1],
                       text='Cargo:',
                       font=('Roboto', 12)))
    label_trajet_pol[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_trajet_pol[0].append(tk.StringVar(root))

    entry_trajet_pol[0].append(tk.Entry(frames_trajet_pol[-1],
                                    textvariable = input_trajet_pol[0][-1],
                                    font = ('Roboto', 12)))
    entry_trajet_pol[0][-1].mandatory = True
    entry_trajet_pol[0][-1].config(bg="#ffffea")
    entry_trajet_pol[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_trajet_pol[0][-1],
                  text='Cargo ao qual o político verbetado se candidatou.')

    #ANO
    label_trajet_pol[1].append(tk.Label(frames_trajet_pol[-1],
                       text='Ano do Pleito:',
                       font=('Roboto', 12)))
    label_trajet_pol[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_trajet_pol[1].append(tk.StringVar(root))

    entry_trajet_pol[1].append(ttk.Combobox(frames_trajet_pol[-1],
                                           state='readonly',
                                           width='6',
                                           font=('Roboto', 11),
                                           textvariable=input_trajet_pol[1][-1],
                                           values = [''] + list(range(1900,datetime.now().year+1))[::-1]))

    entry_trajet_pol[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_trajet_pol[1][-1],
                  text='Ano em que o político verbetado se candidatou ao cargo.')
    
    #PARTIDO
    
    #CARREGA A LISTA DE PARTIDOS A PARTIR DE ARQUIVO DISPONÍVEL NO PROJETO
    with open('./dicts/partidos.txt', 'r', encoding='UTF-8') as f:
        lista_partidos = [line.strip() for line in f]

    label_trajet_pol[2].append(tk.Label(frames_trajet_pol[-1],
                       text='Partido:',
                       font=('Roboto', 12)))
    label_trajet_pol[2][-1].grid(row=0,
                                column=4,
                                sticky = 'e')

    input_trajet_pol[2].append(tk.StringVar(root))


    entry_trajet_pol[2].append(ttk.Combobox(frames_trajet_pol[-1],
                                           width='35',
                                           font=('Roboto', 11),
                                           textvariable=input_trajet_pol[2][-1],
                                           values=lista_partidos))

    entry_trajet_pol[2][-1].grid(row=0,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_trajet_pol[2][-1],
                  text='Partido pelo qual o político verbetado se candidatou.')

    #VOTOS
    label_trajet_pol[3].append(tk.Label(frames_trajet_pol[-1],
                       text='Votos:',
                       font=('Roboto', 12)))
    label_trajet_pol[3][-1].grid(row=1,
                                column=0,
                                sticky = 'e')

    input_trajet_pol[3].append(tk.StringVar(root))

    entry_trajet_pol[3].append(tk.Entry(frames_trajet_pol[-1],
                                    textvariable = input_trajet_pol[3][-1],
                                    font = ('Roboto', 12)))
    entry_trajet_pol[3][-1].grid(row=1,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_trajet_pol[3][-1],
                  text='Quantidade de votos que o verbetado recebeu na candidatura.')

    #ELEITO?
    label_trajet_pol[4].append(tk.Label(frames_trajet_pol[-1],
                              text='''Foi eleito?''',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT))
    label_trajet_pol[4][-1].grid(row=1,
                               column=2,
                               sticky = 'e',
                               padx=2,
                               pady=2)

    input_trajet_pol[4].append(tk.BooleanVar())

    entry_trajet_pol[4].append(tk.Checkbutton(frames_trajet_pol[-1],
                                          variable=input_trajet_pol[4][-1],
                                          onvalue=True,
                                          offvalue=False,
                                          command=foi_eleito))
    entry_trajet_pol[4][-1].grid(row=1,
                               column=3,
                               sticky = 'w',
                               padx=2,
                               pady=2)

    #LEGISLATURA

    #CARREGA A LISTA DE LEGISLATURAS A PARTIR DE ARQUIVO DISPONÍVEL NO PROJETO
    with open('./dicts/legislaturas.txt', 'r', encoding='UTF-8') as f:
        lista_legislaturas = [line.strip() for line in f]

    label_trajet_pol[5].append(tk.Label(frames_trajet_pol[-1],
                       text='Mandato:',
                       font=('Roboto', 12)))
    label_trajet_pol[5][-1].grid(row=1,
                                column=4,
                                sticky = 'e')

    input_trajet_pol[5].append(tk.StringVar(root))

    entry_trajet_pol[5].append(ttk.Combobox(frames_trajet_pol[-1],
                                           width='20',
                                           font=('Roboto', 11),
                                           textvariable=input_trajet_pol[5][-1],
                                           values=lista_legislaturas))

    entry_trajet_pol[5][-1].grid(row=1,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_trajet_pol[5][-1],
                  text='Legislatura ou período em para o qual o político verbetado foi empossado.')


    #RENUNCIA?
    label_trajet_pol[6].append(tk.Label(frames_trajet_pol[-1],
                              text='''Renunciou ao cargo?''',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT))
    label_trajet_pol[6][-1].grid(row=2,
                               column=0,
                               sticky = 'e',
                               padx=2,
                               pady=2)

    input_trajet_pol[6].append(tk.BooleanVar())

    entry_trajet_pol[6].append(tk.Checkbutton(frames_trajet_pol[-1],
                                          variable=input_trajet_pol[6][-1],
                                          onvalue=True,
                                          offvalue=False,
                                          command=renuncia_cargo))
    entry_trajet_pol[6][-1].grid(row=2,
                               column=1,
                               sticky = 'w',
                               padx=2,
                               pady=2)
    CreateToolTip(entry_trajet_pol[6][-1],
              text='Marque esta opçào caso o candidato tenha renunciado ao cargo durante o exercício do mandato.')

    #MOTIVO RENÚNCIA
    label_trajet_pol[7].append(tk.Label(frames_trajet_pol[-1],
                              text='Motivo da renúncia:',
                              font=('Roboto', 12)))
    label_trajet_pol[7][-1].grid(row=2,
                             column=2,
                             sticky = 'e',
                             padx=2,
                             pady=2)

    input_trajet_pol[7].append(tk.StringVar(root))

    entry_trajet_pol[7].append(tk.Entry(frames_trajet_pol[-1],
                                        textvariable = input_trajet_pol[7][-1],
                                        font = ('Roboto', 12)))
    entry_trajet_pol[7][-1].grid(row=2,
                          column=3,
                          sticky = 'w',
                          padx=2,
                          pady=2)
    CreateToolTip(entry_trajet_pol[7][-1],
                  text='Motivo noticiado/alegado pelo verbetado para a renúncia ao cargo.')

    # DATA RENÚNCIA
    label_trajet_pol[8].append(tk.Label(frames_trajet_pol[-1],
                              text='Data da renúncia:',
                              font=('Roboto', 12)))
    label_trajet_pol[8][-1].grid(row=2,
                              column=4,
                              sticky = 'e',
                              padx=2,
                              pady=2)

    frame_data,data = criar_input_data(frames_trajet_pol[-1])
    entry_trajet_pol[8].append(frame_data)
    entry_trajet_pol[8][-1].grid(row=2,
                            column=5,
                            sticky = 'w')
    CreateToolTip(entry_trajet_pol[8][-1],
                  text='Data da renúncia do verbetado ao cargo.') 
    input_trajet_pol[8].append(data)

    renuncia_cargo()
    foi_eleito()
    
def deletar_widgets_trajet_pol():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_trajet_pol) > 0:
        for x in range(0,len(entry_trajet_pol)):
            entry_trajet_pol[x][-1].destroy()
            label_trajet_pol[x][-1].destroy()

            entry_trajet_pol[x].pop(-1)
            input_trajet_pol[x].pop(-1)
            label_trajet_pol[x].pop(-1)
        frames_trajet_pol[-1].destroy()
        frames_trajet_pol.pop(-1)

#%%  Parte 5 - Atuação Legislativa

label_atua_legis = [[],[],[],[],[]]
input_atua_legis = [[],[],[],[],[]]
entry_atua_legis = [[],[],[],[],[]]
frames_atua_legis = []

def criar_widgets_atua_legis():
    """Cria os widgets da 'Parte 5 - Atuação Legislativa'"""
    frames_atua_legis.append(tk.LabelFrame(frame_parte5,
                                       text='Atuação Legislativa {}'.format(len(frames_atua_legis)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte5.winfo_screenwidth()))
    frames_atua_legis[-1].grid(row=len(frames_atua_legis)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    #NOME
    label_atua_legis[0].append(tk.Label(frames_atua_legis[-1],
                       text='Nome:',
                       font=('Roboto', 12)))
    label_atua_legis[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_atua_legis[0].append(tk.StringVar(root))

    entry_atua_legis[0].append(tk.Entry(frames_atua_legis[-1],
                                    textvariable = input_atua_legis[0][-1],
                                    width='25',
                                    font = ('Roboto', 12)))
    entry_atua_legis[0][-1].mandatory = True
    entry_atua_legis[0][-1].config(bg="#ffffea")

    entry_atua_legis[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_atua_legis[0][-1],
                  text='Nome da comissão em que o verbetado atuou.')


    #ATUAÇÃO LEGISLATIVA RELACIONADA
    label_atua_legis[1].append(tk.Label(frames_atua_legis[-1],
                       text='Trajet. Política Relacionada:',
                       font=('Roboto', 12)))
    label_atua_legis[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_atua_legis[1].append(tk.StringVar(root))

    entry_atua_legis[1].append(ttk.Combobox(frames_atua_legis[-1],
                                           state='readonly',
                                           width='23',
                                           font=('Roboto', 11),
                                           textvariable=input_atua_legis[1][-1],
                                           values=''))

    entry_atua_legis[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_atua_legis[1][-1],
                  text='Etapa da trajetória política do verbetado na qual exerceu a atuação legislativa.')


    # .TIPO DE COMISSAO
    label_atua_legis[2].append(tk.Label(frames_atua_legis[-1],
                       text='Tipo:',
                       font=('Roboto', 12)))
    label_atua_legis[2][-1].grid(row=1,
                                column=0,
                                sticky = 'e')

    input_atua_legis[2].append(tk.StringVar(root))

    entry_atua_legis[2].append(ttk.Combobox(frames_atua_legis[-1],
                                    textvariable = input_atua_legis[2][-1],
                                    font = ('Roboto', 12),
                                    values = ['Comissão Permanente',
                                              'Comissão Especial',
                                              'Comissão Externa',
                                              'Comissão Parlamentar de Inquérito (CPI)'
                                              ],
                                    width='23',
                                    state='readonly'))

    entry_atua_legis[2][-1].grid(row=1,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_atua_legis[2][-1],
                  text='Tipo de comissão em que o verbetado atuou.')

    #CASA LEGISLATIVA
    label_atua_legis[3].append(tk.Label(frames_atua_legis[-1],
                       text='Casa Legislativa:',
                       font=('Roboto', 12)))
    label_atua_legis[3][-1].grid(row=1,
                                column=2,
                                sticky = 'e')

    input_atua_legis[3].append(tk.StringVar(root))

    entry_atua_legis[3].append(ttk.Combobox(frames_atua_legis[-1],
                                    textvariable = input_atua_legis[3][-1],
                                    font = ('Roboto', 12),
                                    values = ['Câmara dos Deputados',
                                              'Senado Federal'
                                              ],
                                    width='23',
                                    state='readonly'))

    entry_atua_legis[3][-1].grid(row=1,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_atua_legis[3][-1],
                  text='Casa legislativa onde a comissão foi instaurada.')


    #FUNÇÃO
    label_atua_legis[4].append(tk.Label(frames_atua_legis[-1],
                       text='Função:',
                       font=('Roboto', 12)))
    label_atua_legis[4][-1].grid(row=1,
                                column=4,
                                sticky = 'e')

    input_atua_legis[4].append(tk.StringVar(root))

    entry_atua_legis[4].append(ttk.Combobox(frames_atua_legis[-1],
                                    textvariable = input_atua_legis[4][-1],
                                    font = ('Roboto', 12),
                                    values = ['Presidente',
                                              'Membro Titular'],
                                    width='23',
                                    state='readonly'))

    entry_atua_legis[4][-1].grid(row=1,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_atua_legis[4][-1],
                  text='Função exercida pelo verbetado na comissão.')
    
def deletar_widgets_atua_legis():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_atua_legis) > 0:
        for x in range(0,len(entry_atua_legis)):
            entry_atua_legis[x][-1].destroy()
            label_atua_legis[x][-1].destroy()

            entry_atua_legis[x].pop(-1)
            input_atua_legis[x].pop(-1)
            label_atua_legis[x].pop(-1)
        frames_atua_legis[-1].destroy()
        frames_atua_legis.pop(-1)
    
#%%  Parte 6 - Trajetória na Burocracia Estatal

label_buroc_estat = [[],[],[],[],[],[]]
input_buroc_estat = [[],[],[],[],[],[]]
entry_buroc_estat = [[],[],[],[],[],[]]
frames_buroc_estat = []

def criar_widgets_buroc_estat():
    """Cria os widgets da 'Parte 6 - Trajetória na Burocracia Estatal'"""
    frames_buroc_estat.append(tk.LabelFrame(frame_parte6,
                                       text='Atuação em Burocracia Estatal {}'.format(len(frames_buroc_estat)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte6.winfo_screenwidth()))
    frames_buroc_estat[-1].grid(row=len(frames_buroc_estat)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    # CARGO NOMEADO
    label_buroc_estat[0].append(tk.Label(frames_buroc_estat[-1],
                       text='Cargo Nomeado:',
                       font=('Roboto', 12)))
    label_buroc_estat[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_buroc_estat[0].append(tk.StringVar(root))

    entry_buroc_estat[0].append(tk.Entry(frames_buroc_estat[-1],
                                    textvariable = input_buroc_estat[0][-1],
                                    width='25',
                                    font = ('Roboto', 12)))
    entry_buroc_estat[0][-1].mandatory = True
    entry_buroc_estat[0][-1].config(bg="#ffffea")
    entry_buroc_estat[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_buroc_estat[0][-1],
                  text='Cargo para o qual o verbetado foi nomeado.')
    
    # ÓRGÃO
    label_buroc_estat[1].append(tk.Label(frames_buroc_estat[-1],
                       text='Órgão:',
                       font=('Roboto', 12)))
    label_buroc_estat[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_buroc_estat[1].append(tk.StringVar(root))

    entry_buroc_estat[1].append(tk.Entry(frames_buroc_estat[-1],
                                    textvariable = input_buroc_estat[1][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_buroc_estat[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_buroc_estat[1][-1],
                  text='Órgão ao qual o verbetado foi vinculado no exercício de seu cargo.')


    # DATA DE NOMEAÇÃO
    label_buroc_estat[2].append(tk.Label(frames_buroc_estat[-1],
                       text='Data de Nomeação:',
                       font=('Roboto', 12)))
    label_buroc_estat[2][-1].grid(row=0,
                                column=4,
                                sticky = 'e')

    frame_data,data = criar_input_data(frames_buroc_estat[-1])
    entry_buroc_estat[2].append(frame_data)
    entry_buroc_estat[2][-1].grid(row=0,
                            column=5,
                            sticky = 'w')
    CreateToolTip(entry_buroc_estat[2][-1],
                  text='Data de nomeação do verbetado para o cargo.') 
    input_buroc_estat[2].append(data)


    #EXONERADO?
    label_buroc_estat[3].append(tk.Label(frames_buroc_estat[-1],
                              text='Exonerado?',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT))
    label_buroc_estat[3][-1].grid(row=1,
                               column=0,
                               sticky = 'e',
                               padx=2,
                               pady=2)

    input_buroc_estat[3].append(tk.BooleanVar())

    entry_buroc_estat[3].append(tk.Checkbutton(frames_buroc_estat[-1],
                                          variable=input_buroc_estat[3][-1],
                                          onvalue=True,
                                          offvalue=False,
                                          command=exonerado_buroc))
    entry_buroc_estat[3][-1].grid(row=1,
                               column=1,
                               sticky = 'w',
                               padx=2,
                               pady=2)

    # DATA DE EXONERAÇÃO
    label_buroc_estat[4].append(tk.Label(frames_buroc_estat[-1],
                       text='Data de Exoneração:',
                       font=('Roboto', 12)))
    label_buroc_estat[4][-1].grid(row=1,
                                column=2,
                                sticky = 'e')

    frame_data,data = criar_input_data(frames_buroc_estat[-1])
    entry_buroc_estat[4].append(frame_data)
    entry_buroc_estat[4][-1].grid(row=1,
                            column=3,
                            sticky = 'w')
    CreateToolTip(entry_buroc_estat[4][-1],
                  text='Data de exoneração do verbetado do cargo.') 
    input_buroc_estat[4].append(data)

    # MOTIVO DA EXONERAÇÃO
    label_buroc_estat[5].append(tk.Label(frames_buroc_estat[-1],
                       text='Motivo da Exoneração:',
                       font=('Roboto', 12)))
    label_buroc_estat[5][-1].grid(row=1,
                                column=4,
                                sticky = 'e')

    input_buroc_estat[5].append(tk.StringVar(root))

    entry_buroc_estat[5].append(tk.Entry(frames_buroc_estat[-1],
                                    textvariable = input_buroc_estat[5][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_buroc_estat[5][-1].grid(row=1,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_buroc_estat[5][-1],
                  text='Motivo conhecido da exoneração do verbetado do cargo.')
    
    exonerado_buroc()

def deletar_widgets_buroc_estat():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_buroc_estat) > 0:
        for x in range(0,len(entry_buroc_estat)):
            entry_buroc_estat[x][-1].destroy()
            label_buroc_estat[x][-1].destroy()

            entry_buroc_estat[x].pop(-1)
            input_buroc_estat[x].pop(-1)
            label_buroc_estat[x].pop(-1)
        frames_buroc_estat[-1].destroy()
        frames_buroc_estat.pop(-1)

#%%  Parte 7 - Atuação na Imprensa

label_atua_impren = [[],[],[],[]]
input_atua_impren = [[],[],[],[]]
entry_atua_impren = [[],[],[],[]]
frames_atua_impren = []

def criar_widgets_atua_impren():
    """Cria os widgets da 'Parte 7 - Atuação na Imprensa'"""
    frames_atua_impren.append(tk.LabelFrame(frame_parte7,
                                       text='Atuação na Imprensa {}'.format(len(frames_atua_impren)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte7.winfo_screenwidth()))
    frames_atua_impren[-1].grid(row=len(frames_atua_impren)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    # JORNAL
    label_atua_impren[0].append(tk.Label(frames_atua_impren[-1],
                       text='Nome do Jornal:',
                       font=('Roboto', 12)))
    label_atua_impren[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_atua_impren[0].append(tk.StringVar(root))

    entry_atua_impren[0].append(tk.Entry(frames_atua_impren[-1],
                                    textvariable = input_atua_impren[0][-1],
                                    width='25',
                                    font = ('Roboto', 12),
                                    highlightthickness=1
                                    ))
    entry_atua_impren[0][-1].mandatory = True
    entry_atua_impren[0][-1].config(bg="#ffffea")

    entry_atua_impren[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_atua_impren[0][-1],
                  text='Nome do jornal/periódico ou afins em que o verbetado atuava.')

    # FUNÇÃO
    label_atua_impren[1].append(tk.Label(frames_atua_impren[-1],
                       text='Função Exercida:',
                       font=('Roboto', 12)))
    label_atua_impren[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_atua_impren[1].append(tk.StringVar(root))

    entry_atua_impren[1].append(tk.Entry(frames_atua_impren[-1],
                                    textvariable = input_atua_impren[1][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_atua_impren[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_atua_impren[1][-1],
                  text='Função exercida pelo verbetado no jornal/periódico ou afins relacionado.')

    #DATA INICIO
    label_atua_impren[2].append(tk.Label(frames_atua_impren[-1],
                       text='Ano Inicio:',
                       font=('Roboto', 12)))
    label_atua_impren[2][-1].grid(row=1,
                                column=0,
                                sticky = 'e')

    input_atua_impren[2].append(tk.StringVar(root))

    entry_atua_impren[2].append(ttk.Combobox(frames_atua_impren[-1],
                                           state='readonly',
                                           width='6',
                                           font=('Roboto', 11),
                                           textvariable=input_atua_impren[2][-1],
                                           values = [''] + list(range(1900,datetime.now().year+1))[::-1]))

    entry_atua_impren[2][-1].grid(row=1,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_atua_impren[2][-1],
                  text='Ano em que o político verbetado iniciou as atividades na função.')

    #DATA FIM
    label_atua_impren[3].append(tk.Label(frames_atua_impren[-1],
                       text='Ano Fim:',
                       font=('Roboto', 12)))
    label_atua_impren[3][-1].grid(row=1,
                                column=2,
                                sticky = 'e')

    input_atua_impren[3].append(tk.StringVar(root))

    entry_atua_impren[3].append(ttk.Combobox(frames_atua_impren[-1],
                                           state='readonly',
                                           width='6',
                                           font=('Roboto', 11),
                                           textvariable=input_atua_impren[3][-1],
                                           values = [''] + list(range(1900,datetime.now().year+1))[::-1]))

    entry_atua_impren[3][-1].grid(row=1,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_atua_impren[3][-1],
                  text='Ano em que o político verbetado encerrou as atividades na função.')

def deletar_widgets_atua_impren():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_atua_impren) > 0:
        for x in range(0,len(entry_atua_impren)):
            entry_atua_impren[x][-1].destroy()
            label_atua_impren[x][-1].destroy()

            entry_atua_impren[x].pop(-1)
            input_atua_impren[x].pop(-1)
            label_atua_impren[x].pop(-1)
        frames_atua_impren[-1].destroy()
        frames_atua_impren.pop(-1)

#%%  Parte 8 - Obras publicadas pelo verbetado

label_obras_autor = [[],[]]
input_obras_autor = [[],[]]
entry_obras_autor = [[],[]]
frames_obras_autor = []

def criar_widgets_obras_autor():
    """Cria os widgets da 'Parte 8 - Obras publicadas pelo verbetado'"""
    frames_obras_autor.append(tk.LabelFrame(frame_parte8,
                                       text='Obra Escrita pelo Verbetado {}'.format(len(frames_obras_autor)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte7.winfo_screenwidth()))
    frames_obras_autor[-1].grid(row=len(frames_obras_autor)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    # NOME DA OBRA
    label_obras_autor[0].append(tk.Label(frames_obras_autor[-1],
                       text='Nome da Obra:',
                       font=('Roboto', 12)))
    label_obras_autor[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_obras_autor[0].append(tk.StringVar(root))

    entry_obras_autor[0].append(tk.Entry(frames_obras_autor[-1],
                                    textvariable = input_obras_autor[0][-1],
                                    width='25',
                                    font = ('Roboto', 12)))
    entry_obras_autor[0][-1].mandatory = True
    entry_obras_autor[0][-1].config(bg="#ffffea")

    entry_obras_autor[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_obras_autor[0][-1],
                  text='Nome da obra escrita pelo verbetado.')

    # DATA DE PUBLICAÇÃO
    label_obras_autor[1].append(tk.Label(frames_obras_autor[-1],
                       text='Data de Publicação:',
                       font=('Roboto', 12)))
    label_obras_autor[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    frame_data,data = criar_input_data(frames_obras_autor[-1])
    entry_obras_autor[1].append(frame_data)
    entry_obras_autor[1][-1].grid(row=0,
                            column=3,
                            sticky = 'w')
    CreateToolTip(entry_obras_autor[1][-1],
                  text='Ano de publicação da obra relacionada.') 
    input_obras_autor[1].append(data)

def deletar_widgets_obras_autor():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_obras_autor) > 0:
        for x in range(0,len(entry_obras_autor)):
            entry_obras_autor[x][-1].destroy()
            label_obras_autor[x][-1].destroy()

            entry_obras_autor[x].pop(-1)
            input_obras_autor[x].pop(-1)
            label_obras_autor[x].pop(-1)
        frames_obras_autor[-1].destroy()
        frames_obras_autor.pop(-1)

#%%  Parte 9 - Obras sobre o verbetado

label_obras_sobre = [[],[]]
input_obras_sobre = [[],[]]
entry_obras_sobre = [[],[]]
frames_obras_sobre = []

def criar_widgets_obras_sobre():
    """Cria os widgets da 'Parte 9 - Obras sobre o verbetado'"""
    frames_obras_sobre.append(tk.LabelFrame(frame_parte9,
                                       text='Obra Sobre o Verbetado {}'.format(len(frames_obras_sobre)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte9.winfo_screenwidth()))
    frames_obras_sobre[-1].grid(row=len(frames_obras_sobre)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)
    
    # NOME DA OBRA
    label_obras_sobre[0].append(tk.Label(frames_obras_sobre[-1],
                        text='Nome da Obra:',
                        font=('Roboto', 12)))
    label_obras_sobre[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_obras_sobre[0].append(tk.StringVar(root))

    entry_obras_sobre[0].append(tk.Entry(frames_obras_sobre[-1],
                                    textvariable = input_obras_sobre[0][-1],
                                    width='25',
                                    font = ('Roboto', 12)))
    entry_obras_sobre[0][-1].mandatory = True
    entry_obras_sobre[0][-1].config(bg="#ffffea")
    entry_obras_sobre[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_obras_sobre[0][-1],
                  text='Nome da obra sobre o verbetado.')


    # DATA DE PUBLICAÇÃO
    label_obras_sobre[1].append(tk.Label(frames_obras_sobre[-1],
                        text='Data de Publicação:',
                        font=('Roboto', 12)))
    label_obras_sobre[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')
    
    frame_data,data = criar_input_data(frames_obras_sobre[-1])
    entry_obras_sobre[1].append(frame_data)
    entry_obras_sobre[1][-1].grid(row=0,
                            column=3,
                            sticky = 'w')
    CreateToolTip(entry_obras_sobre[1][-1],
                  text='Ano de publicação da obra relacionada.') 
    input_obras_sobre[1].append(data)

def deletar_widgets_obras_sobre():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_obras_sobre) > 0:
        for x in range(0,len(entry_obras_sobre)):
            entry_obras_sobre[x][-1].destroy()
            label_obras_sobre[x][-1].destroy()

            entry_obras_sobre[x].pop(-1)
            input_obras_sobre[x].pop(-1)
            label_obras_sobre[x].pop(-1)
        frames_obras_sobre[-1].destroy()
        frames_obras_sobre.pop(-1)

#%%  Parte 10 - Processos Criminais Concluídos e Condenações

label_processos = [[],[],[],[],[]]
input_processos = [[],[],[],[],[]]
entry_processos = [[],[],[],[],[]]
frames_processos = []

def criar_widgets_processos():
    """Cria os widgets da 'Parte 10 - Processos Criminais Concluídos e Condenações'"""
    frames_processos.append(tk.LabelFrame(frame_parte10,
                                       text='Processo Criminal {}'.format(len(frames_processos)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte10.winfo_screenwidth()))
    frames_processos[-1].grid(row=len(frames_processos)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    # PROCESSO
    label_processos[0].append(tk.Label(frames_processos[-1],
                       text='Processo:',
                       font=('Roboto', 12)))
    label_processos[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_processos[0].append(tk.StringVar(root))

    entry_processos[0].append(tk.Entry(frames_processos[-1],
                                    textvariable = input_processos[0][-1],
                                    width='25',
                                    font = ('Roboto', 12)))
    entry_processos[0][-1].mandatory = True
    entry_processos[0][-1].config(bg="#ffffea")
    entry_processos[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_processos[0][-1],
                  text='Processo movido contra o verbetado.')

    # NUMERO DO PROCESSO
    label_processos[1].append(tk.Label(frames_processos[-1],
                       text='Nº do Processo:',
                       font=('Roboto', 12)))
    label_processos[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_processos[1].append(tk.StringVar(root))

    entry_processos[1].append(tk.Entry(frames_processos[-1],
                                    textvariable = input_processos[1][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_processos[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_processos[1][-1],
                  text='Número do processo movido contra o verbetado.')

    # MOTIVO DO PROCESSO
    label_processos[2].append(tk.Label(frames_processos[-1],
                       text='Motivo do Processo:',
                       font=('Roboto', 12)))
    label_processos[2][-1].grid(row=0,
                                column=4,
                                sticky = 'e')

    input_processos[2].append(tk.StringVar(root))

    entry_processos[2].append(tk.Entry(frames_processos[-1],
                                    textvariable = input_processos[2][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_processos[2][-1].grid(row=0,
                                column=5,
                                sticky = 'w')
    CreateToolTip(entry_processos[2][-1],
                  text='Motivo do processo movido contra o verbetado.')
    
    #CONDENADO?
    label_processos[3].append(tk.Label(frames_processos[-1],
                              text='Condenado?',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT))
    label_processos[3][-1].grid(row=1,
                               column=0,
                               sticky = 'e',
                               padx=2,
                               pady=2)

    input_processos[3].append(tk.BooleanVar())

    entry_processos[3].append(tk.Checkbutton(frames_processos[-1],
                                          variable=input_processos[3][-1],
                                          onvalue=True,
                                          offvalue=False,
                                          command=condenado_processo))
    entry_processos[3][-1].grid(row=1,
                               column=1,
                               sticky = 'w',
                               padx=2,
                               pady=2)
    

    # DATA DA CONDENAÇÃO
    label_processos[4].append(tk.Label(frames_processos[-1],
                       text='Data de Condenação:',
                       font=('Roboto', 12)))
    label_processos[4][-1].grid(row=1,
                                column=2,
                                sticky = 'e')

    frame_data,data = criar_input_data(frames_processos[-1])
    entry_processos[4].append(frame_data)
    entry_processos[4][-1].grid(row=1,
                            column=3,
                            sticky = 'w')
    CreateToolTip(entry_processos[4][-1],
                  text='Data da condenação judicial do verbetado.') 
    input_processos[4].append(data)
    
    condenado_processo()

def deletar_widgets_processos():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_processos) > 0:
        for x in range(0,len(entry_processos)):
            entry_processos[x][-1].destroy()
            label_processos[x][-1].destroy()

            entry_processos[x].pop(-1)
            input_processos[x].pop(-1)
            label_processos[x].pop(-1)
        frames_processos[-1].destroy()
        frames_processos.pop(-1)

#%%  Parte 11 - Cônjuges

label_conjuges = [[],[],[],[]]
input_conjuges = [[],[],[],[]]
entry_conjuges = [[],[],[],[]]
frames_conjuges = []

def criar_widgets_conjuges():
    """Cria os widgets da 'Parte 11 - Cônjuges'"""
    frames_conjuges.append(tk.LabelFrame(frame_parte11,
                                       text='Cônjuge {}'.format(len(frames_conjuges)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte11.winfo_screenwidth()))
    frames_conjuges[-1].grid(row=len(frames_conjuges)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    # NOME
    label_conjuges[0].append(tk.Label(frames_conjuges[-1],
                      text='Nome:',
                      font=('Roboto', 12)))
    label_conjuges[0][-1].grid(row=0,
                               column=0,
                               sticky = 'e')

    input_conjuges[0].append(tk.StringVar(root))

    entry_conjuges[0].append(tk.Entry(frames_conjuges[-1],
                                      textvariable = input_conjuges[0][-1],
                                      width='25',
                                      font = ('Roboto', 12)))
    entry_conjuges[0][-1].mandatory = True
    entry_conjuges[0][-1].config(bg="#ffffea")
    entry_conjuges[0][-1].grid(row=0,
                               column=1,
                               sticky = 'w')
    CreateToolTip(entry_conjuges[0][-1],
                  text='Nome completo do cônjuge do verbetado.')

    # TEVE FILHOS?
    label_conjuges[1].append(tk.Label(frames_conjuges[-1],
                              text='''Filhos?''',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT))
    label_conjuges[1][-1].grid(row=0,
                               column=2,
                               sticky = 'e',
                               padx=2,
                               pady=2)

    input_conjuges[1].append(tk.BooleanVar())

    entry_conjuges[1].append(tk.Checkbutton(frames_conjuges[-1],
                                          variable=input_conjuges[1][-1],
                                          onvalue=True,
                                          offvalue=False,
                                          command=lambda frame=frames_conjuges[-1]: conjuge_teve_filhos(frame))) 
    entry_conjuges[1][-1].grid(row=0,
                               column=3,
                               sticky = 'w',
                               padx=2,
                               pady=2)

    # QUANTOS FILHOS?
    label_conjuges[2].append(tk.Label(frames_conjuges[-1],
                              text='''Qtd Filhos:''',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT))
    label_conjuges[2][-1].grid(row=0,
                               column=4,
                               sticky = 'e',
                               padx=2,
                               pady=2)

    input_conjuges[2].append(tk.StringVar(value=1))
    
    entry_conjuges[2].append(ttk.Spinbox(frames_conjuges[-1],
                                         from_=1,
                                         to=20,
                                         textvariable=input_conjuges[2][-1],
                                         state = 'readonly',
                                         width=4,
                                         justify='center',
                                         font=Font(family='Roboto', size=11),
                                         command=lambda frame=frames_conjuges[-1]: conjuge_teve_filhos(frame)))
    entry_conjuges[2][-1].grid(row=0,
                               column=5,
                               sticky = 'w',
                               padx=2,
                               pady=2)

    label_conjuges[3].append([])
    input_conjuges[3].append([])
    entry_conjuges[3].append([])
    
def conjuge_teve_filhos(frame):
    """Caso marcado que o verbetado teve filho(s) com o cônjuge, habilita o campo
    'Qtd Filhos' e constrói a quantidade de campos 'Nome do Filho x' correspondente
    à quantidade de filhos inserida no campo Qtd Filhos."""
    x = int(frame.cget("text").split()[1]) - 1
    tem_filhos = input_conjuges[1][x].get()
    
    if tem_filhos:
        entry_conjuges[2][x].config(state='readonly')
        numero_filhos = input_conjuges[2][x].get()
        
        if int(numero_filhos) > len(input_conjuges[3][x]):
            row = frame.grid_size()[1] + 1
            # NOME DO FILHO
            label_conjuges[3][x].append(tk.Label(frame,
                              text=f'Nome do(a) filho(a) {len(entry_conjuges[3][x])+1}:',
                              font=('Roboto', 12)))
            label_conjuges[3][x][-1].grid(row=row,
                                       column=0,
                                       sticky = 'e')
        
            input_conjuges[3][x].append(tk.StringVar(root))
        
            entry_conjuges[3][x].append(tk.Entry(frame,
                                              textvariable = input_conjuges[3][x][-1],
                                              width='25',
                                              font = ('Roboto', 12)))
            entry_conjuges[3][x][-1].grid(row=row,
                                       column=1,
                                       sticky = 'w')
            CreateToolTip(entry_conjuges[3][x][-1],
                          text='Nome do(a) filho(a) do verbetado com o cônjuge.')

        elif int(numero_filhos) < len(input_conjuges[3][x]):
            label_conjuges[3][x][-1].destroy()
            entry_conjuges[3][x][-1].destroy()
            entry_conjuges[3][x].pop(-1)
            input_conjuges[3][x].pop(-1)
            label_conjuges[3][x].pop(-1)
    else:
        entry_conjuges[2][x].set(1)
        for i in list(range(len(input_conjuges[3][x])))[::-1]:
            label_conjuges[3][x][i].destroy()
            entry_conjuges[3][x][i].destroy()
            entry_conjuges[3][x].pop(i)
            input_conjuges[3][x].pop(i)
            label_conjuges[3][x].pop(i)
        entry_conjuges[2][x].config(state='disabled')
    
def deletar_widgets_conjuges():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_conjuges) > 0:
        for x in range(0,len(entry_conjuges)):
            
            if hasattr(entry_conjuges[x][-1], '__iter__'):
                for entry_filho in entry_conjuges[x][-1]:
                    entry_filho.destroy()
                for label_filho in label_conjuges[x][-1]:
                    label_filho.destroy()
            else:
                entry_conjuges[x][-1].destroy()
                label_conjuges[x][-1].destroy()

            entry_conjuges[x].pop(-1)
            input_conjuges[x].pop(-1)
            label_conjuges[x].pop(-1)
        frames_conjuges[-1].destroy()
        frames_conjuges.pop(-1)

#%%  Parte 12 - Fontes

label_fontes = [[],[],[],[],[],[]]
input_fontes = [[],[],[],[],[],[]]
entry_fontes = [[],[],[],[],[],[]]
frames_fontes = []

def criar_widgets_fontes():
    """Cria os widgets da 'Parte 12 - Fontes'"""
    frames_fontes.append(tk.LabelFrame(frame_parte12,
                                       text='Fonte {}'.format(len(frames_fontes)+1),
                                       font=('Roboto', 8, 'bold'),
                                       labelanchor='n',
                                       fg='#444444',
                                       width=frame_parte1.winfo_screenwidth()))
    frames_fontes[-1].grid(row=len(frames_fontes)+1,
                              column=0,
                              columnspan=1000,
                              rowspan=1)

    # AUTOR/ORGANIZAÇÃO
    label_fontes[0].append(tk.Label(frames_fontes[-1],
                       text='Autor/Organização:',
                       font=('Roboto', 12)))
    label_fontes[0][-1].grid(row=0,
                                column=0,
                                sticky = 'e')

    input_fontes[0].append(tk.StringVar(root))

    entry_fontes[0].append(tk.Entry(frames_fontes[-1],
                                    textvariable = input_fontes[0][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_fontes[0][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_fontes[0][-1],
                  text='Autor ou organizador da fonte consultada (Ex: Nome de Autor(es) de artigo consultado, Portal da Câmara dos Deputados, Portal G1 de Notícias, etc.)')

    # TITULO
    label_fontes[1].append(tk.Label(frames_fontes[-1],
                       text='Título:',
                       font=('Roboto', 12)))
    label_fontes[1][-1].grid(row=0,
                                column=2,
                                sticky = 'e')

    input_fontes[1].append(tk.StringVar(root))

    entry_fontes[1].append(tk.Entry(frames_fontes[-1],
                                    textvariable = input_fontes[1][-1],
                                    width='25',
                                    font = ('Roboto', 12)))
    entry_fontes[1][-1].grid(row=0,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_fontes[1][-1],
                  text='Título da página ou matéria da fonte consultada (Ex: Título de obra, bibliografia, artigo etc.)')

    # ORIGEM
    label_fontes[2].append(tk.Label(frames_fontes[-1],
                       text='Origem:',
                       font=('Roboto', 12)))
    label_fontes[2][-1].grid(row=1,
                                column=0,
                                sticky = 'e')

    input_fontes[2].append(tk.StringVar(root))
    
    frame_origem = tk.Frame(frames_fontes[-1])
    frame_origem.grid(row=1,
                      column=1,
                      sticky = 'w')

    entry_fontes[2].append(ttk.Radiobutton(frame_origem,
                                    variable = input_fontes[2][-1],
                                    text="Online",
                                    value="Online",
                                    command=tipo_fonte))
    entry_fontes[2][-1].grid(row=0,
                                column=0,
                                sticky = 'w')
    CreateToolTip(entry_fontes[2][-1],
                  text='Fonte Online (Ex: Site, Portal online de notícias etc.)')
    
    entry_fontes[2].append(ttk.Radiobutton(frame_origem,
                                    variable = input_fontes[2][-1],
                                    text="Offline",
                                    value="Offline",
                                    command=tipo_fonte))
    entry_fontes[2][-1].grid(row=0,
                                column=1,
                                sticky = 'w')
    CreateToolTip(entry_fontes[2][-1],
                  text='Fonte Offline (Ex: Livro, Arquivo etc.)')
    
    input_fontes[2][-1].set("Offline")
    
    # URL
    label_fontes[3].append(tk.Label(frames_fontes[-1],
                       text='URL:',
                       font=('Roboto', 12)))
    label_fontes[3][-1].grid(row=1,
                                column=2,
                                sticky = 'e')

    input_fontes[3].append(tk.StringVar(root))

    entry_fontes[3].append(tk.Entry(frames_fontes[-1],
                                    textvariable = input_fontes[3][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_fontes[3][-1].grid(row=1,
                                column=3,
                                sticky = 'w')
    CreateToolTip(entry_fontes[3][-1],
                  text='URL da página ou matéria da fonte consultada.')
    
    # DATA DE ACESSO
    label_fontes[4].append(tk.Label(frames_fontes[-1],
                       text='Data de Acesso:',
                       font=('Roboto', 12)))
    label_fontes[4][-1].grid(row=1,
                                column=4,
                                sticky = 'e')

    frame_data,data = criar_input_data(frames_fontes[-1])
    entry_fontes[4].append(frame_data)
    entry_fontes[4][-1].grid(row=1,
                            column=5,
                            sticky = 'w')
    CreateToolTip(entry_fontes[4][-1],
                  text='Data de acesso da fonte consultada.') 
    input_fontes[4].append(data)
    
    # INFORMACOES COMPLEMENTARES
    
    label_fontes[5].append(tk.Label(frames_fontes[-1],
                       text='Informações Complementares:',
                       font=('Roboto', 12)))
    label_fontes[5][-1].grid(row=0,
                                column=4,
                                sticky = 'e')

    input_fontes[5].append(tk.StringVar(root))

    entry_fontes[5].append(tk.Entry(frames_fontes[-1],
                                    textvariable = input_fontes[5][-1],
                                    width='25',
                                    font = ('Roboto', 12)))

    entry_fontes[5][-1].grid(row=0,
                                column=5,
                                sticky = 'w',
                                columnspan = 20)
    CreateToolTip(entry_fontes[5][-1],
                  text='Demais informações pertinentes à fonte consultada.')

    tipo_fonte()

def deletar_widgets_fontes():
    """Deleta o último frame do módulo e seus campos associados."""
    if len(frames_fontes) > 0:
        for x in range(0,len(entry_fontes)):
            entry_fontes[x][-1].destroy()
            # entry_fontes[x][-1].destroy()
            label_fontes[x][-1].destroy()

            entry_fontes[x].pop(-1)
            # entry_fontes[x].pop(-1)
            input_fontes[x].pop(-1)
            label_fontes[x].pop(-1)
        frames_fontes[-1].destroy()
        frames_fontes.pop(-1)

#%% FUNÇOES DO SISTEMA

def func_genero(*args):
    """Atualiza a ontologia de parentesco político a partir do gênero do verbetado"""
    onto_parentela_masc = ['afilhado', 'avô', 'bisavô', 'bisneto', 'companheiro', 'cunhado', 'enteado', 'esposo', 'ex-esposo', 'filho', 'genro', 'herdeiro', 'irmão', 'meio-irmão', 'neto', 'noivo', 'padrasto', 'padrinho', 'pai', 'primo', 'sobrinho', 'sobrinho-neto', 'sogro', 'tataravô', 'tio', 'tio-avô', 'viúvo']
    onto_parentela_fem = ['afilhada', 'avó', 'bisavó', 'bisneta', 'companheira', 'cunhada', 'enteada', 'esposa', 'ex-esposa', 'filha', 'nora', 'herdeira', 'irmã', 'meia-irmã', 'neta', 'noiva', 'madrasta', 'madrinha', 'mãe', 'prima', 'sobrinha', 'sobrinha-neta', 'sogra', 'tataravó', 'tia', 'tia-avó', 'viúva']

    for i in range(0,len(entry_parent_pol[1])):
        entry_parent_pol[1][i].configure(completevalues=onto_parentela_fem if input_genero.get() == 'Feminino' else onto_parentela_masc)
    entry_parent_pol[1][-1].set('')
            
def get_municipios(*args):
    """Utiliza a API do IBGE para retornar a lista de municípios no campo correspondente
    do módulo a partir do estado selecionado na UI."""
    if args[0] == 'input_uf_nasc':
        sigla_estado = siglas_estados[input_uf_nasc.get()]
    elif args[0] == 'input_uf_fal':
        sigla_estado = siglas_estados[input_uf_fal.get()]
    else:
        sigla_estado = (siglas_estados[input_formacoes[3][-1].get()]
                        if input_formacoes[3][-1].get() in siglas_estados.keys()
                        else "")
    if sigla_estado == '':
        return

    municipios = requests.get(
        'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'.format(
        sigla_estado
            )
        )
    municipios_lista = [item['nome'] for item in municipios.json()]
    municipios_lista.sort()

    if args[0] == 'input_uf_nasc':
        entry_mun_nasc.configure(completevalues=municipios_lista)
        entry_mun_nasc.set('')
    elif args[0] == 'input_uf_fal':
        entry_mun_fal.configure(completevalues=municipios_lista)
        entry_mun_fal.set('')
    else:
        entry_formacoes[4][-1].configure(completevalues=municipios_lista)
        entry_formacoes[4][-1].set('')

def causa_fal_con():
    """Habilita/desabilita o campo 'causa da morte' quando 
    habilitado o campo 'causa da morte conhecida?'."""
    if input_causa_fal_con.get() == 1:
        entry_causa_fal.config(state='normal')
        CreateToolTip(entry_causa_fal,
              text="Causa da morte conhecida. Exemplo: Causa natural, suicídio...\n"\
              "(Esta informação não integra o corpo do verbete, sendo armazenada apenas como um metadado)")
    else:
        entry_causa_fal.config(state='disabled')
        input_causa_fal.set('')
        CreateToolTip(entry_causa_fal,
              text='Ative a opção "Causa da morte conhecida" para habilitar este campo.')

def renuncia_cargo():
    """Habilita/desabilita os campos 'data da renúncia' e 'motivo da renúncia'
    caso o campo 'renunciou ao cargo?' seja habilitado/desabilitado."""
    for i in range(len(input_trajet_pol[6])):
        grid_widgets = entry_trajet_pol[8][i].winfo_children()
        if input_trajet_pol[6][i].get():
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='normal')
                    # widget.set('')
            CreateToolTip(entry_trajet_pol[8][i],
                  text='Data da renúncia do verbetado ao cargo.')

            entry_trajet_pol[7][i].config(state='normal')
            CreateToolTip(entry_trajet_pol[7][i],
                  text='Motivo noticiado/alegado pelo verbetado para a renúncia ao cargo.')
        else:
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
                    widget.set('')
            CreateToolTip(entry_trajet_pol[8][i],
                  text='Ative a opção "Renunciou ao cargo?" para habilitar este campo.')

            entry_trajet_pol[7][i].config(state='disabled')
            input_trajet_pol[7][i].set('')
            CreateToolTip(entry_trajet_pol[7][i],
                  text='Ative a opção "Renunciou ao cargo?" para habilitar este campo.')

def foi_eleito(*args):
    """Habilita/desabilita os campos de 'legislatura' (preenchido automaticamente
    após a seleção do ano do pleito, através de uma lista de legislaturas disponibilizado
    junto ao projeto) e 'renunciou ao cargo?'."""
    legislaturas = json.load(open("./dicts/legislaturas_anos.txt"))
    
    for i in range(len(input_trajet_pol[4])):
        if input_trajet_pol[4][i].get():
            for j in range(5,7):
                entry_trajet_pol[j][i].config(state='normal')
            CreateToolTip(entry_trajet_pol[5][i],
                  text='Legislatura ou período em para o qual o político verbetado foi empossado.')
            CreateToolTip(entry_trajet_pol[6][i],
                  text='Marque esta opçào caso o candidato tenha renunciado ao cargo durante o exercício do mandato.')            
            
            if input_trajet_pol[1][i].get():
                chave_menor_igual = min((int(chave) 
                                         for chave 
                                         in legislaturas 
                                         if int(chave) >= int(input_trajet_pol[1][i].get())), 
                                        default=None)
                input_trajet_pol[5][i].set(legislaturas.get(str(chave_menor_igual),
                                                            None))

        else:
            entry_trajet_pol[6][i].deselect()
            for j in range(5,8):
                entry_trajet_pol[j][i].config(state='disabled')
                CreateToolTip(entry_trajet_pol[j][i],
                      text='Ative a opção "Foi eleito?" para habilitar este campo.')
            input_trajet_pol[5][i].set('')
    
    renuncia_cargo()

def exonerado_buroc():
    """Habilita/desabilita os campos de 'data de exoneração' e 'motivo da
    exoneraçào' ao habilitar/desabilitar o campo 'exonerado?'."""
    for i in range(len(input_buroc_estat[3])):
        grid_widgets = entry_buroc_estat[4][i].winfo_children()
        if input_buroc_estat[3][i].get():
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='normal')
                    widget.set('')
            CreateToolTip(entry_buroc_estat[4][i],
                  text='Data de exoneração do verbetado do cargo.')
            entry_buroc_estat[5][i].config(state='normal')
            CreateToolTip(entry_buroc_estat[5][i],
                  text='Motivo conhecido da exoneração do verbetado do cargo.')
        else:
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
                    widget.set('')
            CreateToolTip(entry_buroc_estat[4][i],
                  text='Ative a opção "Exonerado?" para habilitar este campo.')
            entry_buroc_estat[5][i].config(state='disabled')
            input_buroc_estat[5][i].set('')
            CreateToolTip(entry_buroc_estat[5][i],
                  text='Ative a opção "Exonerado?" para habilitar este campo.')

def condenado_processo():
    """Habilita/desabilita os campos 'data da condenação' ao habilitar/desabilitar
    o campo 'condenado?'."""
    for i in range(len(input_processos[3])):
        grid_widgets = entry_processos[4][i].winfo_children()
        if input_processos[3][i].get():
            CreateToolTip(entry_processos[4][i],
                          text='Data da condenação judicial do verbetado.') 
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='normal')
                    widget.set('')
        else:
            CreateToolTip(entry_processos[4][i],
                          text='Ative a opção "Condenado?" para habilitar este campo.') 
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
                    widget.set('')

def tipo_fonte():
    """Habilita/desabilita os campos 'URL' e 'data de acesso' ao selecionar
    natureza da fonte online ou offline"""
    for i in range(len(input_fontes[2])):
        grid_widgets = entry_fontes[4][i].winfo_children()
        if input_fontes[2][i].get() == "Online":
            CreateToolTip(entry_fontes[4][i],
                          text='Data de acesso da fonte consultada.') 
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='normal')
                    widget.set('')
            entry_fontes[3][i].config(state='normal')
            CreateToolTip(entry_fontes[3][i],
                          text='URL da página ou matéria da fonte consultada.') 
        else:
            CreateToolTip(entry_fontes[4][i],
                          text='Opção válida apenas para fontes online. Selecione origem "Online" para ativar o campo.') 
            for widget in grid_widgets:
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
                    widget.set('')
            entry_fontes[3][i].delete(0, "end")
            entry_fontes[3][i].config(state='disabled')
            CreateToolTip(entry_fontes[3][i],
                          text='Opção válida apenas para fontes online. Selecione origem "Online" para ativar o campo.') 

def atualizar_cbox_trajetorias():
    """Prenche o campo 'trajetória política relacionada' do módulo 'parte 5 - 
    atuação leggislativa' com os caros preenchidos no módulo 'parte 4 - trajetória política'."""
    for cbox in entry_atua_legis[1]:
        cbox['values'] = [x.cargo + (
                          ' (' + 
                          x.mandato +
                          ')' if x.mandato != '' else '')
                          for x 
                          in dados_verbetado.trajet_pol 
                          if len(x.cargo) > 0 
                          and x.eleito] 

def campos_obrigatorios(event):
    """Personaliza os campos obrigatórios na UI se possuem ou não um valor atribuído."""
    if type(event.widget).__name__ == "Entry":
        if hasattr(event.widget, 'mandatory') and event.widget.mandatory == True:
            if event.widget.get():
                event.widget.config(bg="#ffffff")
            else:
                event.widget.config(bg="#ffffea")
    elif type(event.widget).__name__ == "Combobox":
        if hasattr(event.widget, 'mandatory') and event.widget.mandatory == True:
            if event.widget.get():
                event.widget.config(background="#ffffff")
            else:
                event.widget.config(background="#ffffea")

def validar_input_numeros(event):
    """Valida apenas números nos widgets de tipo Entry"""
    for char in event.char:
        if not (char.isdigit() or char in ('\b', '\x7f')):
            return "break"
        
def SalvarArquivo():
    """Cria subpastas no diretório padrão do software para o verbetado (se não houver) 
    e salva um arquivo .pickle com o objeto Verbetado produzido."""
    if len(dados_verbetado.nome_civ) > 0:

        nome_arquivo = '%s'%'_'.join(word
                                     for word
                                     in dados_verbetado.nome_civ.split())

        if not os.path.isdir("./Verbetes"):
            os.mkdir("./Verbetes")        
        
        if not os.path.isdir("./Verbetes/%s"%nome_arquivo):
            os.mkdir("./Verbetes/%s"%nome_arquivo)

        with open('./Verbetes/%s/%s.pickle'%(nome_arquivo,nome_arquivo), 'wb') as handle:
            pickle.dump(dados_verbetado, handle, protocol=pickle.HIGHEST_PROTOCOL)
        tk.messagebox.showinfo(title='Salvar Arquivo', 
                            message='Arquivo salvo com sucesso em %s\Verbetes\%s\%s.pickle.'%(os.path.abspath(os.curdir),
                                                                                       nome_arquivo,
                                                                                       nome_arquivo))
    else:
        tk.messagebox.showerror(title='Salvar Arquivo', 
                             message='O nome civil do verbetado é obrigatório.')


def ExportarVerbete():
    """Cria subpastas no diretório padrão do software para o verbetado (se não houver) 
    e salva um arquivo .txt com o verbete produzido."""
    global string_verbete
    
    nome_arquivo = '%s'%'_'.join(word
                                 for word
                                 in dados_verbetado.nome_civ.split())
    
    if not os.path.isdir("./Verbetes"):
        os.mkdir("./Verbetes")        
    
    if not os.path.isdir("./Verbetes/%s"%nome_arquivo):
        os.mkdir("./Verbetes/%s"%nome_arquivo)

    with open('./Verbetes/%s/%s.txt'%(nome_arquivo,nome_arquivo), 'w+') as handle:
        handle.write(string_verbete.get())
    tk.messagebox.showinfo(title='Exportar Verbete', 
                        message='Verbete exportado com sucesso em %s\Verbetes\%s\%s.txt.'%(os.path.abspath(os.curdir),
                                                                                           nome_arquivo,
                                                                                           nome_arquivo))

def ExportarJSON():
    """Cria subpastas no diretório padrão do software para o verbetado (se não houver) 
    e salva um arquivo .json com o objeto Verbetado produzido."""
    global dados_verbetado
    
    nome_arquivo = '%s'%'_'.join(word
                             for word
                             in dados_verbetado.nome_civ.split())
    
    if not os.path.isdir("./Verbetes"):
        os.mkdir("./Verbetes")        
    
    if not os.path.isdir("./Verbetes/%s"%nome_arquivo):
        os.mkdir("./Verbetes/%s"%nome_arquivo)

    with open('./Verbetes/%s/%s.json'%(nome_arquivo,nome_arquivo), 'w+', encoding='utf-8') as handle:
        handle.write(dados_verbetado.toJSON())
    tk.messagebox.showinfo(title='Exportar Verbete', 
                        message='Arquivo salvo com sucesso em %s\Verbetes\%s\%s.json.'%(os.path.abspath(os.curdir),
                                                                                   nome_arquivo,
                                                                                   nome_arquivo))
    
def _on_mousewheel(event):
    """Permite a rolagem da página através do scrool do mouse."""
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
def AboutButton():
    """Abre o GitHub do projeto."""
    webbrowser.open("https://github.com/danielbonattoseco/DHBB")
    
#%% CONSTRUÇÃO UI

if __name__ == "__main__":

    # DEFINIR TELA PRINCIPAL
    root = tk.Tk()
    root.title('Gerador de Verbetes DHBB 0.1')
    root.iconbitmap('images/fgv-logo.ico')

    # MENUS
    menu = tk.Menu(root)
    root.config(menu=menu)
    
    # MENUS - ARQUIVO
    filemenu = tk.Menu(menu,tearoff=0)
    menu.add_cascade(label='Arquivo', menu=filemenu)
    filemenu.add_command(label='Salvar Arquivo', command=SalvarArquivo)
    
    exportmenu = tk.Menu(filemenu,tearoff=0)
    filemenu.add_cascade(label='Exportar', menu=exportmenu)
    exportmenu.add_command(label='Exportar Verbete (.txt)', command=ExportarVerbete)
    exportmenu.add_command(label='Exportar Metadados (.JSON)', command=ExportarJSON)
    
    # MENUS - SOBRE
    menu.add_command(label='Sobre', command=AboutButton)

    #DIMENSÃO E POSICIONAMENTO DA JANELA
    windowWidth = 1160
    windowHeight = 600

    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

    root.geometry("{}x{}+{}+{}".format(windowWidth,
                                       windowHeight,
                                       positionRight,
                                       positionDown))
    root.resizable(False, True)

    #IMAGEM CPDOC
    logo_cpdoc = Image.open("images/cpdoc-logo.png")
    logo_cpdoc = logo_cpdoc.resize((200, 50))
    logo_cpdoc = ImageTk.PhotoImage(logo_cpdoc)
    frame_logo_cpdoc = tk.Frame(root,
                         width=root.winfo_screenwidth(),
                         height=50,
                         bg='white',
                         relief='flat',
                         highlightbackground="silver",
                         highlightthickness=1)
    frame_logo_cpdoc.pack_propagate(False)
    frame_logo_cpdoc.pack()

    label = tk.Label(frame_logo_cpdoc,
                  image = logo_cpdoc,
                  bg='#E2FCFF',
                  width=root.winfo_screenwidth(),
                  height=50)
    label.pack()

    #FRAME DE DADOS (CENTRAL - CAMPOS DE INPUT)
    frame_dados = tk.Frame(root,
                     width=root.winfo_screenwidth(),
                     height=400,
                     relief='flat')

    canvas = tk.Canvas(frame_dados)
    
    scrollbar = ttk.Scrollbar(frame_dados,
                              orient="vertical",
                              command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    frame_dados_scroll = ttk.Frame(canvas)
    frame_dados_scroll.bind_all("<MouseWheel>", _on_mousewheel)
    frame_dados_scroll.bind("<MouseWheel>", _on_mousewheel)

    frame_dados_scroll.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0),
                         window=frame_dados_scroll,
                         anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

    frame_dados.pack_propagate(False)
    frame_dados.pack()

    # FRAME DE PRÉVIA DO TEXTO (INFERIOR)
    
    frame_previa = tk.Frame(root,
                          width=root.winfo_screenwidth(),
                          height=root.winfo_screenheight(),
                          bg='white',
                          relief='flat',
                          highlightbackground="silver",
                          highlightthickness=1)

    frame_previa.pack_propagate(False)
    frame_previa.pack()

    titulo_previa_texto = tk.Label(frame_previa,
                        text='PREVIEW DO VERBETE',
                        bg='white',
                        font=('Roboto', 8, 'bold'))
    titulo_previa_texto.pack()

    text_frame_previa = tk.Text(frame_previa,
                        wrap='word')

    text_frame_previa.pack(side=tk.LEFT,
                           fill=tk.X,
                           expand=True)

    text_frame_previa.tag_config('warning', foreground="red")

    sb_previa = tk.Scrollbar(frame_previa)
    sb_previa.pack(side=tk.RIGHT,
                   fill=tk.Y)

    text_frame_previa.config(yscrollcommand=sb_previa.set)
    sb_previa.config(command=text_frame_previa.yview)

    #STRING DE PREVIEW DO VERBETE, ATUALIZADA À MEDIDA QUE O USUARIO INSERE DADOS
    string_verbete = tk.StringVar(root)
    string_verbete.set('Neste campo será apresentada uma prévia do verbete. Preencha os campos acima para iniciar a redação.')
    text_frame_previa.insert(tk.INSERT,
                             string_verbete.get())

#%% INICIO CAMPOS PREENCHIMENTO

    #DICIONÁRIO DO VERBETE
    
    frame_tipo = tk.LabelFrame(frame_dados_scroll,
                              text='Dados do Verbete',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_tipo.pack(fill=tk.X)
    
    label_tipo_verbete = tk.Label(frame_tipo,
                              text='Dicionário do verbete:',
                              font=('Roboto', 12))
    label_tipo_verbete.grid(row=0,
                            column=0,
                            sticky = 'e', 
                            padx=2, 
                            pady=2)

    tipo_verbete = tk.StringVar(root, value="DHBB")
    
    radio_biografico = ttk.Radiobutton(frame_tipo,
                                    variable = tipo_verbete,
                                    text="DHBB",
                                    value="DHBB")
    radio_biografico.grid(row=0,
                          column=1,
                          sticky = 'e', 
                          padx=2, 
                          pady=2)
    
    radio_tematico = ttk.Radiobutton(frame_tipo,
                                    variable = tipo_verbete,
                                    text="DHBPR",
                                    value="DHBPR")
    radio_tematico.grid(row=0,
                        column=2,
                        sticky = 'e',
                        padx=2,
                        pady=2)
    
    #NOME AUTOR VERBETE
    label_nome_autor_verbete = tk.Label(frame_tipo,
                              text='Autor do verbete:',
                              font=('Roboto', 12))
    label_nome_autor_verbete.grid(row=0,
                                  column=3,
                                  sticky = 'e', 
                                  padx=(75,0), 
                                  pady=2)

    input_nome_autor_verbete = tk.StringVar(root)
    entry_nome_autor_verbete = tk.Entry(frame_tipo,
                                        textvariable = input_nome_autor_verbete,
                                        font = ('Roboto', 12))
    entry_nome_autor_verbete.mandatory = True
    entry_nome_autor_verbete.config(bg="#ffffea")
    entry_nome_autor_verbete.grid(row=0,
                                  column=4,
                                  sticky = 'w', 
                                  padx=2, 
                                  pady=2)
    CreateToolTip(entry_nome_autor_verbete,
                  text='Nome completo do autor do verbete.')
    

    ############################ PARTE 1 #####################################

    frame_parte1 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 1 - Identificação Pessoal',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte1.pack(fill=tk.X)

    #NOME CIVIL
    label_nome_civ = tk.Label(frame_parte1,
                              text='Nome civil:',
                              font=('Roboto', 12))
    label_nome_civ.grid(row=0,column=0,sticky = 'e', padx=2, pady=2)

    input_nome_civ = tk.StringVar(root)
    entry_nome_civ = tk.Entry(frame_parte1,
                              name="entry_nome_civ",
                              textvariable = input_nome_civ,
                              font = ('Roboto', 12))
    entry_nome_civ.focus_force()
    entry_nome_civ.mandatory = True
    entry_nome_civ.config(bg="#ffffea")
    entry_nome_civ.grid(row=0,column=1,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_nome_civ,
                  text='Nome completo no registro civil oficial do verbetado.')

    #NOME SOCIAL
    label_nome_soc = tk.Label(frame_parte1,
                              text='Nome social:',
                              font=('Roboto', 12))
    label_nome_soc.grid(row=0,column=2,sticky = 'e', padx=2, pady=2)

    input_nome_soc = tk.StringVar(root)
    entry_nome_soc = tk.Entry(frame_parte1,
                              textvariable = input_nome_soc,
                              font = ('Roboto', 12))
    entry_nome_soc.grid(row=0,column=3,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_nome_soc,
                  text='Nome que o político verbetado adotou para adequar a sua identidade referenciando o nome que o representa.')

    #NOME POLITICO
    label_nome_pol = tk.Label(frame_parte1,
                              text='Nome político:',
                              font=('Roboto', 12))
    label_nome_pol.grid(row=0,column=4,sticky = 'e', padx=2, pady=2)

    input_nome_pol = tk.StringVar(root)
    entry_nome_pol = tk.Entry(frame_parte1,
                              textvariable = input_nome_pol,
                              font = ('Roboto', 12))
    entry_nome_pol.grid(row=0,column=5,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_nome_pol,
                  text='Nome político/fantasia pelo qual o verbetado é conhecido na política.')

    #GENERO
    label_genero = tk.Label(frame_parte1,
                        text='Gênero:',
                        font=('Roboto', 12))
    label_genero.grid(row=1,column=0,sticky = 'e', padx=2, pady=2)
    input_genero = tk.StringVar()
    input_genero.set("Selecione")
    input_genero.trace("w", func_genero)

    entry_genero = ttk.Combobox(frame_parte1,
                              textvariable=input_genero,
                              values=["Masculino","Feminino"],
                              state='readonly',
                              width='12',
                              font=('Roboto', 12))
    entry_genero.grid(row=1,column=1,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_genero,
                  text='Gênero do político verbetado.')

    #DATA DE NASCIMENTO
    label_data_nasc = tk.Label(frame_parte1,
                                  text='Data de nascimento:',
                                  font=('Roboto', 12))
    label_data_nasc.grid(row=2,column=0,sticky = 'e', padx=2, pady=2)
    
    entry_data_nasc,data_nasc = criar_input_data(frame_parte1)
    entry_data_nasc.grid(row=2,
                        column=1,
                        sticky = 'w')
    input_data_nasc = data_nasc
    CreateToolTip(entry_data_nasc,
                  text='Data de nascimento do verbetado.')

    #DATA DE FALECIMENTO
    label_data_fal = tk.Label(frame_parte1,
                                  text='Data de falecimento:',
                                  font=('Roboto', 12))
    label_data_fal.grid(row=3,column=0,sticky = 'e', padx=2, pady=2)
    
    entry_data_fal,data_fal = criar_input_data(frame_parte1)
    entry_data_fal.grid(row=3,
                        column=1,
                        sticky = 'w')
    input_data_fal = data_fal
    CreateToolTip(entry_data_fal,
                  text='Data de falecimento do verbetado.')

    #UF DE NASCIMENTO
    try:
        estados_br = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados').json()
        estados_br_lista = [estado['nome']
                            for estado
                            in estados_br]
        estados_br_lista.sort()
        siglas_estados = {item['nome']:item['sigla'] for item in estados_br}
    except Exception:
        with open('dicts/estados_br.json') as f:
            estados_br = json.load(f)
        estados_br_lista = list(estados_br.values())
        estados_br_lista.sort()
        siglas_estados = {v: k for k, v in estados_br.items()}

    label_uf_nasc = tk.Label(frame_parte1,
                        text='UF Nascimento:',
                        font=('Roboto', 12))
    label_uf_nasc.grid(row=2,column=2,sticky = 'e', padx=2, pady=2)

    input_uf_nasc = tk.StringVar(name="input_uf_nasc")
    input_uf_nasc.set("Selecione")
    input_uf_nasc.trace("w", get_municipios)

    entry_uf_nasc = tk.OptionMenu(frame_parte1,
                              input_uf_nasc,
                              *estados_br_lista)
    entry_uf_nasc.config(font=('Roboto', 10))
    entry_uf_nasc.grid(row=2,column=3,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_uf_nasc,
                  text='Estado de nascimento do político verbetado.')

    #MUNICIPIO DE NASCIMENTO
    label_mun_nasc = tk.Label(frame_parte1,
                              text='Mun. Nascimento:',
                              font=('Roboto', 12))
    label_mun_nasc.grid(row=2,column=4,sticky = 'e', padx=2, pady=2)

    input_mun_nasc = tk.StringVar(root)

    entry_mun_nasc = AutocompleteCombobox(frame_parte1,
                                          font=('Roboto', 12),
                                          textvariable = input_mun_nasc,
                                          completevalues=[''])
    entry_mun_nasc.grid(row=2,column=5,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_mun_nasc,
                  text='Município de nascimento do político verbetado.')

    #UF DE FALECIMENTO
    label_uf_fal = tk.Label(frame_parte1,
                        text='UF Falecimento:',
                        font=('Roboto', 12))
    label_uf_fal.grid(row=3,column=2,sticky = 'e', padx=2, pady=2)
    input_uf_fal = tk.StringVar(name='input_uf_fal')
    input_uf_fal.set("Selecione")
    input_uf_fal.trace("w", get_municipios)

    entry_uf_fal = tk.OptionMenu(frame_parte1,
                              input_uf_fal,
                              *estados_br_lista)
    entry_uf_fal.config(font=('Roboto', 10))
    entry_uf_fal.grid(row=3,column=3,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_uf_fal,
                  text='Estado de falecimento do político verbetado.')

    #MUNICIPIO DE FALECIMENTO
    label_mun_fal = tk.Label(frame_parte1,
                              text='Mun. Falecimento:',
                              font=('Roboto', 12))
    label_mun_fal.grid(row=3,column=4,sticky = 'e', padx=2, pady=2)

    input_mun_fal = tk.StringVar(root)

    entry_mun_fal = AutocompleteCombobox(frame_parte1,
                                         textvariable = input_mun_fal,
                                         font=('Roboto', 12),
                                         completevalues=[''])

    entry_mun_fal.grid(row=3,column=5,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_mun_fal,
                  text='Município de falecimento do político verbetado.')

    #CAUSA DO FALECIMENTO CONHECIDA?
    label_causa_fal_con = tk.Label(frame_parte1,
                              text='''Causa da morte\nconhecida?''',
                              font=('Roboto', 12),
                              anchor="e",
                              justify=tk.RIGHT)
    label_causa_fal_con.grid(row=4,
                             column=0,
                             sticky = 'e',
                             padx=2,
                             pady=2)

    input_causa_fal_con = tk.IntVar()

    entry_causa_fal_con = tk.Checkbutton(frame_parte1,
                                      variable=input_causa_fal_con,
                                      onvalue=1,
                                      offvalue=0,
                                      command=causa_fal_con)
    entry_causa_fal_con.grid(row=4,
                             column=1,
                             sticky = 'w',
                             padx=2,
                             pady=2)

    #CAUSA DO FALECIMENTO
    label_causa_fal = tk.Label(frame_parte1,
                              text='Causa da morte:',
                              font=('Roboto', 12))
    label_causa_fal.grid(row=4,column=2,sticky = 'e', padx=2, pady=2)

    input_causa_fal = tk.StringVar(root)

    entry_causa_fal = tk.Entry(frame_parte1,
                              textvariable = input_causa_fal,
                              font = ('Roboto', 12))
    entry_causa_fal.grid(row=4,column=3,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_causa_fal,
                  text='Causa da morte conhecida. Exemplo: Causa natural, suicídio...\n(Esta informação não integra o corpo do verbete, sendo armazenada apenas como um metadado)')

    causa_fal_con()

    #NOME DO PAI
    label_nome_pai = tk.Label(frame_parte1,
                              text='Nome do pai:',
                              font=('Roboto', 12))
    label_nome_pai.grid(row=5,column=0,sticky = 'e', padx=2, pady=2)

    input_nome_pai = tk.StringVar(root)
    entry_nome_pai = tk.Entry(frame_parte1,
                              textvariable = input_nome_pai,
                              font = ('Roboto', 12))
    entry_nome_pai.grid(row=5,column=1,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_nome_pai,
                  text='Nome do pai do político verbetado.')

    #PROFISSÃO DO PAI
    label_prof_pai = tk.Label(frame_parte1,
                              text='Profissão do pai:',
                              font=('Roboto', 12))
    label_prof_pai.grid(row=5,column=2,sticky = 'e', padx=2, pady=2)

    input_prof_pai = tk.StringVar(root)
    entry_prof_pai = tk.Entry(frame_parte1,
                              textvariable = input_prof_pai,
                              font = ('Roboto', 12))
    entry_prof_pai.grid(row=5,column=3,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_prof_pai,
                  text='Profissão do pai do político verbetado.')

    #NOME DA MÃE
    label_nome_mae = tk.Label(frame_parte1,
                              text='Nome da mãe:',
                              font=('Roboto', 12))
    label_nome_mae.grid(row=6,column=0,sticky = 'e', padx=2, pady=2)

    input_nome_mae = tk.StringVar(root)
    entry_nome_mae = tk.Entry(frame_parte1,
                              textvariable = input_nome_mae,
                              font = ('Roboto', 12))
    entry_nome_mae.grid(row=6,column=1,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_nome_mae,
                  text='Nome da mãe do político verbetado.')

    #PROFISSÃO DA MÃE
    label_prof_mae = tk.Label(frame_parte1,
                              text='Profissão da mãe:',
                              font=('Roboto', 12))
    label_prof_mae.grid(row=6,column=2,sticky = 'e', padx=2, pady=2)

    input_prof_mae = tk.StringVar(root)
    entry_prof_mae = tk.Entry(frame_parte1,
                              textvariable = input_prof_mae,
                              font = ('Roboto', 12))
    entry_prof_mae.grid(row=6,column=3,sticky = 'w', padx=2, pady=2)
    CreateToolTip(entry_prof_mae,
                  text='Profissão da mãe do político verbetado.')


    ############################ PARTE 2 #####################################

    #PARENTESCO
    frame_parte2 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 2 - Parentela Política',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte2.pack(fill=tk.X)

    botao_adicionar_parent_pol = tk.Button(frame_parte2,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_parent_pol)
    # botao_adicionar_formacao.pack(side=RIGHT)
    botao_adicionar_parent_pol.grid(row=0,
                                  column=0,
                                  sticky = 'w')

    botao_remover_parent_pol = tk.Button(frame_parte2,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_parent_pol)
    # botao_remover_formacao.pack(side=RIGHT)
    botao_remover_parent_pol.grid(row=0,
                                column=1,
                                sticky = 'w')

    criar_widgets_parent_pol()


    ############################ PARTE 3 #####################################

    frame_parte3 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 3 - Formação Acadêmica',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=frame_parte1.winfo_width())
    frame_parte3.pack(fill=tk.X)

    botao_adicionar_formacao = tk.Button(frame_parte3,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_formacao)
    # botao_adicionar_formacao.pack(side=RIGHT)
    botao_adicionar_formacao.grid(row=0,
                                  column=0,
                                  sticky = 'w')

    botao_remover_formacao = tk.Button(frame_parte3,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_formacao)
    # botao_remover_formacao.pack(side=RIGHT)
    botao_remover_formacao.grid(row=0,
                                column=1,
                                sticky = 'w')

    criar_widgets_formacao()

    # ############################ PARTE 4 #####################################

    frame_parte4 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 4 - Trajetória Política',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte4.pack(fill=tk.X)

    botao_adicionar_trajet_pol = tk.Button(frame_parte4,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_trajet_pol)
    botao_adicionar_trajet_pol.grid(row=0,column=0,sticky = 'w')

    botao_remover_trajet_pol = tk.Button(frame_parte4,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_trajet_pol)
    botao_remover_trajet_pol.grid(row=0,column=1,sticky = 'w')

    criar_widgets_trajet_pol()

    # ############################ PARTE 5 #####################################

    frame_parte5 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 5 - Atuação Legislativa',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte5.pack(fill=tk.X)

    botao_adicionar_atua_legis = tk.Button(frame_parte5,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_atua_legis)
    botao_adicionar_atua_legis.grid(row=0,column=0,sticky = 'w')

    botao_remover_atua_legis = tk.Button(frame_parte5,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_atua_legis)
    botao_remover_atua_legis.grid(row=0,column=1,sticky = 'w')

    criar_widgets_atua_legis()

    # ############################ PARTE 6 #####################################

    frame_parte6 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 6 - Trajetória na Burocracia Estatal',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte6.pack(fill=tk.X)

    botao_adicionar_buroc_estat = tk.Button(frame_parte6,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_buroc_estat)
    botao_adicionar_buroc_estat.grid(row=0,column=0,sticky = 'w')

    botao_remover_buroc_estat = tk.Button(frame_parte6,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_buroc_estat)
    botao_remover_buroc_estat.grid(row=0,column=1,sticky = 'w')

    criar_widgets_buroc_estat()

    # ############################ PARTE 7 #####################################

    frame_parte7 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 7 - Atuação na Imprensa',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte7.pack(fill=tk.X)

    botao_adicionar_atua_impren = tk.Button(frame_parte7,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_atua_impren)
    botao_adicionar_atua_impren.grid(row=0,column=0,sticky = 'w')

    botao_remover_atua_impren = tk.Button(frame_parte7,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_atua_impren)
    botao_remover_atua_impren.grid(row=0,column=1,sticky = 'w')

    criar_widgets_atua_impren()

    # ############################ PARTE 8 #####################################

    frame_parte8 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 8 - Obras publicadas pelo verbetado',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte8.pack(fill=tk.X)

    botao_adicionar_obras_autor = tk.Button(frame_parte8,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_obras_autor)
    botao_adicionar_obras_autor.grid(row=0,column=0,sticky = 'w')

    botao_remover_obras_autor = tk.Button(frame_parte8,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_obras_autor)
    botao_remover_obras_autor.grid(row=0,column=1,sticky = 'w')

    criar_widgets_obras_autor()

    # ############################ PARTE 9 #####################################

    frame_parte9 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 9 - Obras publicadas sobre o verbetado',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte9.pack(fill=tk.X)

    botao_adicionar_obras_sobre = tk.Button(frame_parte9,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_obras_sobre)
    botao_adicionar_obras_sobre.grid(row=0,column=0,sticky = 'w')

    botao_remover_obras_sobre = tk.Button(frame_parte9,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_obras_sobre)
    botao_remover_obras_sobre.grid(row=0,column=1,sticky = 'w')

    criar_widgets_obras_sobre()

    # ############################ PARTE 10 #####################################

    frame_parte10 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 10 - Processos Criminais Concluídos e Condenações',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte10.pack(fill=tk.X)

    botao_adicionar_processos = tk.Button(frame_parte10,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_processos)
    botao_adicionar_processos.grid(row=0,column=0,sticky = 'w')

    botao_remover_processos = tk.Button(frame_parte10,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_processos)
    botao_remover_processos.grid(row=0,column=1,sticky = 'w')

    criar_widgets_processos()

    # ############################ PARTE 11 #####################################

    frame_parte11 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 11 - Cônjuges',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte11.pack(fill=tk.X)

    botao_adicionar_conjuge = tk.Button(frame_parte11,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_conjuges)
    botao_adicionar_conjuge.grid(row=0,column=0,sticky = 'w')

    botao_remover_conjuge = tk.Button(frame_parte11,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_conjuges)
    botao_remover_conjuge.grid(row=0,column=1,sticky = 'w')

    criar_widgets_conjuges()

    # ############################ PARTE 12 #####################################

    frame_parte12 = tk.LabelFrame(frame_dados_scroll,
                              text='Parte 12 - Fontes',
                              labelanchor='nw',
                              font=('Roboto', 8, 'bold'),
                              width=root.winfo_screenwidth())
    frame_parte12.pack(fill=tk.X)

    botao_adicionar_fontes = tk.Button(frame_parte12,
                                      text='Adicionar',
                                      bg='#d8ffc5',
                                      font=('Roboto', 8, 'bold'),
                                      command=criar_widgets_fontes)
    botao_adicionar_fontes.grid(row=0,column=0,sticky = 'w')

    botao_remover_fontes = tk.Button(frame_parte12,
                                      text='Remover',
                                      bg='#FFCFCF',
                                      font=('Roboto', 8, 'bold'),
                                      command=deletar_widgets_fontes)
    botao_remover_fontes.grid(row=0,column=1,sticky = 'w')

    criar_widgets_fontes()

##############################################################################

    dados_verbetado = Verbetado(input_atua_impren, input_atua_legis, input_buroc_estat,
                                input_causa_fal, input_conjuges, input_data_fal,
                                input_data_nasc, input_fontes, input_formacoes, input_genero,
                                input_mun_fal, input_mun_nasc, input_nome_civ, input_nome_mae,
                                input_nome_pai, input_nome_pol, input_nome_soc, input_obras_autor,
                                input_obras_sobre, input_parent_pol, input_processos,
                                input_prof_mae, input_prof_pai, input_trajet_pol,
                                input_uf_fal, input_uf_nasc, tipo_verbete, input_nome_autor_verbete)

#%% BIND INTERAÇÒES COM A UI PARA CONSTRUÇÃO DO VERBETE
    root.bind("<Key>", construtor_verbete)
    root.bind("<Button-1>", construtor_verbete)
    root.bind("<ButtonRelease-1>", construtor_verbete)
    root.bind("<Return>", construtor_verbete)
    root.bind('<<ComboboxSelected>>', construtor_verbete)
    root.bind("<Enter>", construtor_verbete)
    root.bind('<Leave>', construtor_verbete)
    
#%% EXECUTAR A APLICAÇÀO
    root.mainloop()