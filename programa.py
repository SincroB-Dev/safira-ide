#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Toplevel
from tkinter import CURRENT
from tkinter import INSERT
from tkinter import Button
from tkinter import RAISED
from tkinter import Canvas
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import NSEW
from tkinter import Text
from tkinter import FLAT
from tkinter import Menu
from tkinter import END
from tkinter import N
from tkinter import S
from tkinter import E
from tkinter import W
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import Tk
import tkinter as tk
from interpretador import Run
from threading import Thread
from time import time, sleep
from os.path import abspath
from Arquivo import Arquivo
from Colorir import Colorir
from json import load
from os import listdir
from os import getcwd
import webbrowser
import funcoes

__author__ = 'Gabriel Gregório da Silva'
__email__ = 'gabriel.gregorio.1@outlook.com'
__project__ = 'Combratec'
__github__ = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__status__ = 'Desenvolvimento'
__date__ = '01/08/2019'
__last_update__ = '19/04/2020'
__version__ = '0.1'

global dic_info_arquivo
global bool_tela_em_fullscreen
global lst_titulos_frames
global tx_terminal
global tx_codfc
global linhas_laterais
global dic_design
global cor_do_comando
global posCorrente
global posAbsuluta
global instancia
global linha_para_break_point
global lst_abas
global fr_abas
global aba_focada
global controle_arquivos
global dic_abas
global bool_debug_temas

bool_debug_temas = False

# Ativa opções de debug
def debug():
    global bool_debug_temas
    messagebox.showinfo("Aviso","Debug iniciado para todos os casos")

    if bool_debug_temas:
        bool_debug_temas = False
    else:
        bool_debug_temas = True
    

def funcoes_arquivos_configurar(event, comando, link=None):
    global controle_arquivos
    global dic_abas
    global aba_focada
    global tx_codfc

    if controle_arquivos == None:
        return 0

    controle_arquivos.atualiza_infos(dic_abas, aba_focada, tx_codfc)

    if comando == "abrirArquivo":
        controle_arquivos.abrirArquivo(link)

    elif comando == "salvar_arquivo_dialog":
        controle_arquivos.salvar_arquivo_dialog(event)

    elif comando == "salvar_arquivo":
        controle_arquivos.salvar_arquivo(event)

    elif comando == "salvar_arquivo_como_dialog":
        controle_arquivos.salvar_arquivo_como_dialog(event)

    aba_focada = controle_arquivos.aba_focada
    dic_abas = controle_arquivos.dic_abas

    colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc)

def inicializa_orquestrador(event = None, libera_break_point_executa = False):
    print("\n Orquestrador iniciado")

    bt_playP.configure(image=ic_PStop)
    bt_playP.update()

    global dic_abas
    global tx_codfc
    global instancia
    global aba_focada
    global tx_terminal

    # Se for executar até o breakpoint
    if libera_break_point_executa:

        bool_ignorar_todos_breakpoints = False
        try:
            instancia.bool_break_point_liberado = True
            instancia.bool_ignorar_todos_breakpoints = False
        except:
            print("Iniciando programa até breakpoint")
        else:
            print("Liberando programa.")
            return 0
    else:
        bool_ignorar_todos_breakpoints = True

    inicio = time()

    try:
        print(instancia.numero_threads)

    except:
        pass

    else:

        try:
            instancia.aconteceu_erro = True

        except Exception as e:
            print("Impossivel para interpretador: " + str(e))

        return 0

    # Se for executar até o breakpoint
    if libera_break_point_executa:
        inicializador_terminal_debug()
    else:
        inicializador_terminal_producao()
        

    tx_terminal.delete('1.0', END)

    linhas = tx_codfc.get('1.0', END)[0:-1]
    nova_linha = ''

    lista = linhas.split('\n')
    for linha in range(len(lista)):
        nova_linha += '[{}]{}\n'.format( str(linha + 1), lista[linha] )

    linhas = nova_linha

    instancia = Run(
        tx_terminal,
        tx_codfc,
        False,
        dic_abas[aba_focada]["lst_breakpoints"],
        bool_ignorar_todos_breakpoints)

    t = Thread(target=lambda codigoPrograma = linhas: instancia.orquestrador_interpretador(codigoPrograma))
    t.start()

    while instancia.numero_threads != 0 or not instancia.boo_orquestrador_iniciado:
        print(instancia.numero_threads, instancia.boo_orquestrador_iniciado)
        tela.update()
    print(instancia.numero_threads, instancia.boo_orquestrador_iniciado)

    print("FIMMMMMMMMMMm")
    del instancia

    try:
        tx_terminal.insert(END, '\nScript finalizado em {:.3} segundos'.format(time() - inicio))
        tx_terminal.see("end")

    except Exception as erro:
        print('Impossível exibir mensagem de finalização, erro: '+ str(erro))
    
    bt_playP.configure(image=ic_playP)

def pressionar_enter_terminal(event = None):
    global instancia
    print("ENTERRRRRRRRRRRRRR")
    try:
        instancia.pressionou_enter(event)
    except Exception as erro:
        print("Impossivel detectar enter:", erro)

def capturar_tecla_terminal(event):
    print("TECLA QUALUQEE")
    global instancia
 
    try:
        instancia.capturar_tecla( event.keysym )
    except:
        pass

global top_janela_terminal
def destruir_instancia_terminal():
    global lista_itens_destruir

    for widget in lista_itens_destruir:
        try:
            widget.destroy()
        except Exception as e:
            print("Impossivel destruir instância: ", e)

def retornar_variaveis_correspondentes():
    global instancia

    try:
        dic_variaveis = instancia.dic_variaveis
    except Exception as e:
        print("Instancia finalizada ", e)
    else:
        arvores_grid.delete(*arvores_grid.get_children()) # IDS como argumentos

        palavra = campo_busca.get()
        for k, v in dic_variaveis.items():
            if palavra in k:
                arvores_grid.insert('', END, values=(k, v[1], v[0]))


global lista_itens_destruir
lista_itens_destruir = []

def inicializador_terminal_debug():
    global tx_terminal
    global top_janela_terminal
    global arvores_grid
    global campo_busca

    global lista_itens_destruir


    destruir_instancia_terminal()

    frame_terminal_e_grid = Frame(fr_princ)
    frame_terminal_e_grid.grid(row=1, column=4, sticky=NSEW)

    frame_terminal_e_grid.grid_columnconfigure(1, weight=1)
    frame_terminal_e_grid.rowconfigure(1, weight=1)

    # Terminal
    tx_terminal = Text(frame_terminal_e_grid)

    try:
        tx_terminal.configure(dic_design["tx_terminal"])
    except Exception as erro:
        print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

    tx_terminal.bind('<Return>', lambda event:pressionar_enter_terminal(event))
    tx_terminal.bind("<KeyRelease>", lambda event: capturar_tecla_terminal(event))
    tx_terminal.focus_force()
    tx_terminal.grid(row=1, column=1, sticky=NSEW)

    # Debug
    coluna_identificadores = ('Variavel', 'Tipo','Valor')
    fram_grid_variaveis = Frame(frame_terminal_e_grid)
    fram_grid_variaveis.grid(row=2, column=1, sticky = NSEW)

    fram_grid_variaveis.grid_columnconfigure(1, weight=1)
    fram_grid_variaveis.rowconfigure(2, weight=1)

    campo_busca = Entry(fram_grid_variaveis)
    campo_busca.bind("<KeyRelease>",  lambda event: retornar_variaveis_correspondentes())

    arvores_grid = ttk.Treeview(fram_grid_variaveis, columns=coluna_identificadores, show="headings")
    vsroolb = Scrollbar(fram_grid_variaveis, orient="vertical", command=arvores_grid.yview)
    hsroolb = Scrollbar(fram_grid_variaveis, orient="horizontal", command=arvores_grid.xview)
    arvores_grid.configure(yscrollcommand=vsroolb.set, xscrollcommand=hsroolb.set)
    for coluna in coluna_identificadores:
        arvores_grid.heading(coluna, text=coluna.title() )
        arvores_grid.column(coluna, width=tkFont.Font().measure(coluna.title()) + 20)

    campo_busca.grid(row=1, column=1, sticky=NSEW)
    arvores_grid.grid(row=2,column=1,  sticky=NSEW)
    vsroolb.grid(row=2,column=2, sticky='ns')
    hsroolb.grid(row=3,column=1,  sticky='ew')

    retornar_variaveis_correspondentes()


    lista_itens_destruir = [hsroolb, arvores_grid, campo_busca, fram_grid_variaveis, frame_terminal_e_grid]

def inicializador_terminal_producao():
    global tx_terminal
    global top_janela_terminal
    destruir_instancia_terminal()

    top_janela_terminal = Toplevel(tela)
    top_janela_terminal.grid_columnconfigure(1, weight=1)
    top_janela_terminal.rowconfigure(1, weight=1)

    top_janela_terminal.withdraw() # Ocultar tkinter

    t_width  = tela.winfo_screenwidth()
    t_heigth = tela.winfo_screenheight()

    top_janela_terminal.geometry("720x450+{}+{}".format( int(t_width / 2 - 720 / 2), int(t_heigth / 2 - 450 / 2) ))
    top_janela_terminal.deiconify()

    tela.update()

    tx_terminal = Text(top_janela_terminal)

    try:
        tx_terminal.configure(dic_design["tx_terminal"])
    except Exception as erro:
        print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

    tx_terminal.bind('<Return>', lambda event:pressionar_enter_terminal(event))
    tx_terminal.bind("<KeyRelease>", lambda event: capturar_tecla_terminal(event))
    tx_terminal.focus_force()
    tx_terminal.grid(row=1, column=1, sticky=NSEW)

def arquivoConfiguracao(chave, novo = None):

    if novo is None:
        with open('configuracoes/configuracoes.json') as json_file:
            configArquivoJson = load(json_file)
            retorno = configArquivoJson[chave]

        return retorno

    elif novo is not None:
        with open('configuracoes/configuracoes.json') as json_file:
            configArquivoJson = load(json_file)

            configArquivoJson[chave] = novo
            configArquivoJson = str(configArquivoJson).replace('\'','\"')

        file = open('configuracoes/configuracoes.json','w')
        file.write(str(configArquivoJson))
        file.close()

def atualizaInterface(chave, novo):
    global tela
    global tx_codfc
    global dic_design
    global cor_do_comando
    global bool_debug_temas

    while True:

        try:
            arquivoConfiguracao(chave, novo)
        except Exception as e:
            return [None,'Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas']

        dic_comandos, dic_design, cor_do_comando = funcoes.atualiza_configuracoes_temas()

        try:
            colorir_codigo.alterar_cor_comando(cor_do_comando)
            colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc).update()
            atualiza_design_interface()
        except Exception as erro:
            print('ERRO: ', erro)
        else:
            print('Temas atualizados')

        tela.update()
        tx_codfc.update()

        if not bool_debug_temas:
            break

def atualiza_interface_config(objeto, menu):
    global dic_design

    try:
        objeto.configure(dic_design[menu])
    except Exception as erro:
        print("Interface" + erro)
    return 0

def atualiza_design_interface():

    atualiza_interface_config(mn_intfc_casct_sintx, "cor_menu")
    atualiza_interface_config(mn_intfc_casct_temas, "cor_menu")
    atualiza_interface_config(mn_ferrm, "cor_menu")
    atualiza_interface_config(mn_intfc, "cor_menu")
    atualiza_interface_config(mn_loclz, "cor_menu")
    atualiza_interface_config(mn_exect, "cor_menu")
    atualiza_interface_config(mn_arqui, "cor_menu")
    atualiza_interface_config(mn_edita, "cor_menu")
    atualiza_interface_config(mn_exemp, "cor_menu")
    atualiza_interface_config(mn_barra, "cor_menu")
    atualiza_interface_config(mn_ajuda, "cor_menu")
    atualiza_interface_config(mn_sobre, "cor_menu")
    atualiza_interface_config(mn_devel, "cor_menu")
    atualiza_interface_config(mn_devel, "cor_menu")
    atualiza_interface_config(bt_salva, "dicBtnMenus")
    atualiza_interface_config(bt_playP, "dicBtnMenus")
    atualiza_interface_config(bt_breaP, "dicBtnMenus")
    atualiza_interface_config(bt_desfz, "dicBtnMenus")
    atualiza_interface_config(bt_redsf, "dicBtnMenus")
    atualiza_interface_config(bt_ajuda, "dicBtnMenus")
    atualiza_interface_config(bt_pesqu, "dicBtnMenus")
    atualiza_interface_config(bt_brk_p, "dicBtnMenus")
    atualiza_interface_config(fr_princ, "fr_princ")
    atualiza_interface_config(tela, "tela")
    atualiza_interface_config(linhas_laterais, "lb_linhas")
    atualiza_interface_config(tx_codfc, "tx_codificacao")
    atualiza_interface_config(sb_codfc, "scrollbar_text")
    atualiza_interface_config(fr_opc_rapidas, "fr_opcoes_rapidas")

    atualiza_interface_config(fr_abas, "dic_cor_abas_frame")
    atualiza_interface_config(fr_espaco, "dic_cor_abas_frame")

class ContadorLinhas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        global dic_abas
        global aba_focada
        self.textwidget = None

    def atribuir(self, text_widget):
        self.textwidget = text_widget

    def desenhar_linhas(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :

            dline= self.textwidget.dlineinfo(i)
            if dline is None: break

            y = dline[1]
            linenum = str(i).split(".")[0]

            cor_padrao = "#777777"
            if int(linenum) in dic_abas[aba_focada]["lst_breakpoints"]:
                linenum = linenum + " * "
                cor_padrao = "red"
            else:
                linenum = " " + str(linenum)

            self.create_text(2,y,anchor="nw", text=linenum, font=("Lucida Sans", 13),  fill=cor_padrao)
            i = self.textwidget.index("%s+1line" % i)

class EditorDeCodigo(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)
    
            if (args[0] in ("insert", "replace", "delete") or args[0:3] == ("mark", "set", "insert") or args[0:2] == ("xview", "moveto") or args[0:2] == ("xview", "scroll") or args[0:2] == ("yview", "moveto") or args[0:2] == ("yview", "scroll")):
                self.event_generate("<<Change>>", when="tail")

            return result        
        except Exception as erro:
            print("Erro em _proxy: ", erro)
            return ""

def atualizacao_linhas(event):
    linhas_laterais.desenhar_linhas()

def modoFullScreen(event=None):
    global bool_tela_em_fullscreen

    if bool_tela_em_fullscreen: bool_tela_em_fullscreen = False
    else: bool_tela_em_fullscreen = True

    tela.attributes("-fullscreen", bool_tela_em_fullscreen)

def ativar_logs(event=None):
    global instancia

    try:
        if instancia.bool_logs: instancia.bool_logs = False
        else: instancia.bool_logs = True

    except:
        print("Interpretador não iniciado")

def obterPosicaoDoCursor(event=None):
    global tx_codfc
    global linha_para_break_point

    try:
        numPosicao = str(tx_codfc.index(INSERT))
        posCorrente = int(float(tx_codfc.index(CURRENT)))
    except Exception as erro:
        print("Erro em obterPosicaoDoCursor: {}".format(erro))
    else:
        print('linha que o cursor está : ', numPosicao)
        print('posicao do cursor: ', posCorrente)
        linha_para_break_point = posCorrente


def adiciona_remove_breakpoint(event = None):
    global dic_abas

    if int(linha_para_break_point) in dic_abas[aba_focada]["lst_breakpoints"]:
        dic_abas[aba_focada]["lst_breakpoints"].remove(int(linha_para_break_point))
    else:
        dic_abas[aba_focada]["lst_breakpoints"].append(int(linha_para_break_point))
    atualizacao_linhas(event = None)

def atualiza_texto_tela(num_aba):
    print("atualiza_texto_tela")
    global tx_codfc
    global dic_abas

    tx_codfc.delete(1.0, END)
    tx_codfc.insert(END, str(dic_abas[num_aba]["arquivoAtual"]["texto"]))
    colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc)

    nome_arquivo = dic_abas[num_aba]["arquivoSalvo"]["link"].split("/")
    dic_abas[num_aba]["listaAbas"][1].configure(text=nome_arquivo[-1])

def fecha_aba(bt_fechar):
    print("fecha_aba")
    global dic_abas
    global aba_focada

    bool_era_focado = False
    dic_cor_abas = dic_design["dic_cor_abas"]
    for chave, valor in dic_abas.items():
        if dic_abas[chave]["listaAbas"][2] == bt_fechar:
            dic_abas[chave]["listaAbas"][2].grid_forget()
            dic_abas[chave]["listaAbas"][1].grid_forget()
            dic_abas[chave]["listaAbas"][0].grid_forget()

            if dic_abas[chave]["foco"] == True:
                bool_era_focado = True
            del dic_abas[chave]

            break

    if len(dic_abas) == 0:
        print("SEM NENHUMA ABA")
        nova_aba()

    elif bool_era_focado:
        print("ANTIGO ERA FOCADO")

        for chave, dados_aba in dic_abas.items():

            dic_cor_abas["background"] = dic_design["dic_cor_abas_focada"]["background"]
            bg_padrao = dic_design["dic_cor_abas_focada"]["background"]
            aba_focada = chave
            dic_abas[chave]["foco"] =True

            configurar_cor_aba(dic_cor_abas, bg_padrao)

            atualiza_texto_tela(chave)
            break

def configurar_cor_aba(dic_cor_abas, bg_padrao):
    global dic_abas
    global aba_focada

    dic_abas[aba_focada]["listaAbas"][0].configure(background=bg_padrao, height=20)
    dic_abas[aba_focada]["listaAbas"][1].configure(dic_cor_abas, activebackground=bg_padrao)
    dic_abas[aba_focada]["listaAbas"][2].configure(dic_cor_abas, activebackground=bg_padrao)

def atualiza_aba_foco(lb_aba):
    print("atualiza_aba_foco")
    global dic_abas
    global tx_codfc
    global aba_focada

    # Remove o foco da aba anterior
    dic_cor_abas = dic_design["dic_cor_abas"]
    
    dic_cor_abas["background"] = dic_design["dic_cor_abas_nao_focada"]["background"]
    bg_padrao = dic_design["dic_cor_abas_nao_focada"]["background"]
    configurar_cor_aba(dic_cor_abas, bg_padrao)

    dic_abas[aba_focada]["foco"] = False

    for chave, dados_aba in dic_abas.items():

        if dados_aba["listaAbas"][1] == lb_aba:
            dic_cor_abas["background"] = dic_design["dic_cor_abas_focada"]["background"]
            bg_padrao = dic_design["dic_cor_abas_focada"]["background"]
            aba_focada = chave
            dic_abas[chave]["foco"] = True

            configurar_cor_aba(dic_cor_abas, bg_padrao)

            atualiza_texto_tela(chave)
            break

def nova_aba(event=None):
    print("nova_aba")
    global dic_abas
    global aba_focada
    global dic_design
    global fr_abas

    if len(dic_abas) != 0:
        dic_cor_abas = dic_design["dic_cor_abas"] 
        bg_padrao = dic_design["dic_cor_abas_nao_focada"]["background"]
        dic_cor_abas["background"] = bg_padrao

        configurar_cor_aba(dic_cor_abas, bg_padrao)

        dic_abas[aba_focada]["listaAbas"][0].update()
        dic_abas[aba_focada]["listaAbas"][1].update()
        dic_abas[aba_focada]["listaAbas"][2].update()

        print(aba_focada,"FOCADA")

        posicao_adicionar = max(dic_abas.keys()) + 1 # Maior aba + 1
    else:
        posicao_adicionar = 0

    dic_abas[ posicao_adicionar ] = {"nome":"",
                                     "foco":True,
                                     "lst_breakpoints":[],
                                     "arquivoSalvo":{'link': "",'texto': ""},
                                     "arquivoAtual":{'texto': ""},
                                     "listaAbas":[]}

    dic_cor_abas = dic_design["dic_cor_abas"] 
    dic_cor_abas["background"] = dic_design["dic_cor_abas_focada"]["background"]
    bg_padrao = dic_design["dic_cor_abas_focada"]["background"]

    fr_uma_aba = Frame(fr_abas, height=20, background=dic_design["dic_cor_abas_frame"]["background"])
    lb_aba = Button(fr_uma_aba, dic_cor_abas, text="    ", border=0, highlightthickness=0, padx=8, activebackground=bg_padrao,font = ("Lucida Sans", 13))
    bt_fechar = Button(fr_uma_aba, dic_cor_abas, text="x", relief=FLAT, border=0, activebackground=bg_padrao, highlightthickness=0, font = ("Lucida Sans", 13))

    lb_aba['command'] = lambda lb_aba=lb_aba: atualiza_aba_foco(lb_aba)
    bt_fechar['command'] = lambda bt_fechar=bt_fechar: fecha_aba(bt_fechar)

    fr_uma_aba.rowconfigure(1, weight=1)
         
    fr_uma_aba.grid(row=1, column=posicao_adicionar + 2, sticky=N)
    lb_aba.grid(row=1, column=1, sticky=NSEW)
    bt_fechar.grid(row=1, column=2)

    dic_abas[posicao_adicionar]["listaAbas"].append(fr_uma_aba)
    dic_abas[posicao_adicionar]["listaAbas"].append(lb_aba)
    dic_abas[posicao_adicionar]["listaAbas"].append(bt_fechar)

    aba_focada = posicao_adicionar
    atualiza_texto_tela(aba_focada)

def renderizar_abas_inicio():
    print("renderizar_abas_inicio")
    """
        Usado apenas no inicio do programa *****1 VEZ*****
    """
    global fr_abas
    global aba_focada
    global dic_abas
    global dic_design

    cor_aba_focada = dic_design["dic_cor_abas_focada"]["background"]
    cor_aba_nao_focada = dic_design["dic_cor_abas_nao_focada"]["background"]

    for num_aba, dados_aba in dic_abas.items():
        dic_cor_abas = dic_design["dic_cor_abas"] 

        if dados_aba["foco"]:
            aba_focada = num_aba
            bg_padrao = cor_aba_focada
        else:
            bg_padrao = cor_aba_nao_focada

        dic_cor_abas["background"] = bg_padrao

        fr_uma_aba = Frame(fr_abas, height=20, background=dic_design["dic_cor_abas_frame"]["background"])
        fr_uma_aba.rowconfigure(1, weight=1)

        nome_arquivo = str(dados_aba["arquivoSalvo"]["link"]).split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if dados_aba["arquivoSalvo"]["texto"] != dados_aba["arquivoAtual"]["texto"]:
            txt_btn = "*"
        else:
            txt_btn = "x"

        if nome_arquivo == "":
            nome_arquivo = "     "

        lb_aba = Button(fr_uma_aba, dic_cor_abas, text=nome_arquivo, border=0, highlightthickness=0, padx=8, activebackground=bg_padrao,font = ("Lucida Sans", 13))
        bt_fechar = Button(fr_uma_aba, dic_cor_abas, text=txt_btn, relief=FLAT, border=0, activebackground=bg_padrao, highlightthickness=0, font = ("Lucida Sans", 13))
 
        fr_uma_aba.update()
        lb_aba.update()
        bt_fechar.update()

        fr_uma_aba.grid(row=1, column=num_aba + 2, sticky=N)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        lb_aba['command'] = lambda lb_aba=lb_aba: atualiza_aba_foco(lb_aba)
        bt_fechar['command'] = lambda bt_fechar=bt_fechar: fecha_aba(bt_fechar)

        dic_abas[num_aba]["listaAbas"].append(fr_uma_aba)
        dic_abas[num_aba]["listaAbas"].append(lb_aba)
        dic_abas[num_aba]["listaAbas"].append(bt_fechar)

def ativar_coordernar_coloracao(event = None):

    global tx_codfc
    global dic_abas
    global aba_focada

    print("Alterado!")
    if dic_abas != {}:
        dic_abas[aba_focada]["arquivoAtual"]['texto'] = tx_codfc.get(1.0, END)
    colorir_codigo.coordena_coloracao(event, tx_codfc=tx_codfc)

def centraliza_tela():
    tela.update()
    tela.withdraw() # Ocultar tkinter
    j_width  = tela.winfo_reqwidth()
    j_height = tela.winfo_reqheight()

    t_width    = tela.winfo_screenwidth()
    t_heigth   = tela.winfo_screenheight()

    tela.geometry("+{}+{}".format( int(t_width / 2) - int(j_width / 2), int(t_heigth / 2 ) - int (j_height / 2) ))
    tela.deiconify()
    tela.update()

dic_comandos, dic_design, cor_do_comando = funcoes.atualiza_configuracoes_temas()

tela = Tk()

tela.rowconfigure(1, weight=1)
tela.grid_columnconfigure(1, weight=1)
tela.withdraw()          # Ocultar Janela
tela.overrideredirect(1) # Remve barra de titulos

frame_tela = Frame(tela)
frame_splash = Frame(tela)

frame_splash.configure(dic_design["cor_intro"])
frame_splash.rowconfigure(1, weight=1)
frame_splash.grid_columnconfigure(0, weight=1)

fr_splash = Frame(frame_splash, dic_design["cor_intro"])

l1_splash = Label(frame_splash, dic_design["cor_intro"], text=" COMBRATEC ", fg="#404040", font=( "Lucida Sans", 90), bd=80)
l2_splash = Label(frame_splash, dic_design["cor_intro"], text="Carregando Safira ILE", fg="#404040", font=("Lucida Sans", 12))

frame_splash.grid(row=1, column=1, sticky=NSEW)
fr_splash.grid(row=0, column=1, sticky=NSEW)
l1_splash.grid(row=1, column=1, sticky=NSEW)
l2_splash.grid(row=2, column=1, sticky=NSEW)
frame_splash.update()

centraliza_tela()

# Carregamento de Dados
colorir_codigo = Colorir(cor_do_comando, dic_comandos)
bool_tela_em_fullscreen = False
linha_para_break_point = 0
lst_titulos_frames = []
controle_arquivos = None
posAbsuluta = 0
posCorrente = 0
aba_focada = 0
lst_abas = []
path = abspath(getcwd())

dic_abas = {
    0:{
        "nome":"",
        "foco":True,
        "lst_breakpoints":[],
        "arquivoSalvo":{'link': "",'texto': ""},
        "arquivoAtual":{'texto': ""},
        "listaAbas":[]
    }
}

sleep(3)

fr_splash.grid_forget()
l1_splash.grid_forget()
l2_splash.grid_forget()
frame_splash.grid_forget()
tela.update()

tela.overrideredirect(0)
tela.update()
tela.withdraw() # Ocultar tkinter
frame_tela.grid(row=1, column=1, sticky=NSEW)
frame_tela.update()

# Configurações de telas
tela.bind('<F11>', lambda event: modoFullScreen(event))
tela.bind('<F5>', lambda event: inicializa_orquestrador(event))
tela.bind('<Control-s>', lambda event:funcoes_arquivos_configurar(None, "salvar_arquivo"))
tela.bind('<Control-o>', lambda event: funcoes_arquivos_configurar(None, "salvar_arquivo_dialog"))
tela.bind('<Control-S>', lambda event: funcoes_arquivos_configurar(None, "salvar_arquivo_como_dialog"))
tela.bind('<F7>', lambda event: inicializa_orquestrador(libera_break_point_executa = True))
tela.bind('<F10>', lambda event: adiciona_remove_breakpoint())
tela.bind('<Control-n>', nova_aba)
tela.title('Combratec -  Safira ILE')

# tela.attributes('-fullscreen', True)

frame_tela.rowconfigure(2, weight=1)
frame_tela.grid_columnconfigure(1, weight=1)

try:
    imgicon = PhotoImage(file='icone.png')
    tela.call('wm', 'iconphoto', tela._w, imgicon)
except Exception as erro:
    print('Erro ao carregar icone do app:', erro)

mn_barra = Menu(tela, tearoff=False, font = ("Lucida Sans", 13))
tela.config(menu=mn_barra)

mn_ferrm = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_intfc = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_exect = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_loclz = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_exemp = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_arqui = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_edita = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_ajuda = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_sobre = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))
mn_devel = Menu(mn_barra, tearoff=False, font = ("Lucida Sans", 13))

mn_barra.add_cascade(label='  Arquivo'    , menu=mn_arqui, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Executar'   , menu=mn_exect, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Localizar'  , menu=mn_loclz, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Exemplos'  , menu=mn_exemp, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Interface'  , menu=mn_intfc, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Ajuda'      , menu=mn_ajuda, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  sobre'      , menu=mn_sobre, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Dev'        , menu=mn_devel, font = ("Lucida Sans", 13))
mn_barra.add_cascade(label='  Ferramentas', menu=mn_ferrm, font = ("Lucida Sans", 13))

mn_arqui.add_command(label='  Abrir arquivo (Ctrl+O)', command= lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo_dialog"))
mn_arqui.add_command(label='  Nova Aba (Ctrl-N)', command = nova_aba)
mn_arqui.add_command(label='  Abrir pasta')
mn_arqui.add_separator()
mn_arqui.add_command(label='  Recentes')
mn_arqui.add_separator()
mn_arqui.add_command(label='  Salvar (Ctrl-S)', command= lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo"))
mn_arqui.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo_como_dialog"))
mn_arqui.add_separator()
mn_arqui.add_command(label='  imprimir (Ctrl-P)')
mn_arqui.add_command(label='  Exportar (Ctrl-E)')
mn_arqui.add_command(label='  Enviar por e-mail ')

mn_exect.add_command(label='  Executar Tudo (F5)', command=lambda event=None: inicializa_orquestrador(libera_break_point_executa=False))
mn_exect.add_command(label='  Executar linha (F6)')
mn_exect.add_command(label='  Executar até breakpoint (F7)', command=lambda event=None: inicializa_orquestrador(libera_break_point_executa = True))
mn_exect.add_command(label='  Parar execução (F9)')
mn_exect.add_command(label='  Inserir breakpoint (F10)', command = adiciona_remove_breakpoint)
mn_loclz.add_command(label='  Localizar (CTRL + F)')
mn_loclz.add_command(label='  Substituir (CTRL + R)')

mn_arq_exemplo_casc = Menu(mn_exemp, tearoff = False)
for file in listdir('scripts/'):
    if len(file) > 5:
        if file[-3:] == 'fyn':
            funcao = lambda link = file:  funcoes_arquivos_configurar(None, "abrirArquivo" , 'scripts/' + str(link))
            mn_exemp.add_command(label="  " + file + "  ", command = funcao)

mn_intfc_casct_temas = Menu(mn_intfc, tearoff=False)
mn_intfc.add_cascade(label='  Temas', menu=mn_intfc_casct_temas)
for file in listdir('temas/'):
    if len(file) > 11:
        if file[-10:] == 'theme.json':
            funcao = lambda link = file: atualizaInterface('tema', str(link))
            mn_intfc_casct_temas.add_command(label=file, command=funcao)

mn_intfc_casct_sintx = Menu(mn_intfc, tearoff=False)
mn_intfc.add_cascade(label='  sintaxe', menu=mn_intfc_casct_sintx)
for file in listdir('temas/'):
    if len(file) > 13:
        if file[-12:] == 'sintaxe.json':
            funcao = lambda link = file: atualizaInterface('sintaxe', str(link))
            mn_intfc_casct_sintx.add_command(label=file, command=funcao)

mn_ajuda.add_command(label='  Ajuda (F1)', command=lambda event:webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comandos Disponíveis', command=lambda event:webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comunidade', command=lambda event:webbrowser.open("https://feynmancode.blogspot.com/p/comunidade.html"))
mn_sobre.add_command(label='  Projeto', command=lambda event:webbrowser.open("http://feynmancode.blogspot.com/"))
mn_devel.add_command(label='  Logs', command= lambda event=None: ativar_logs())
mn_devel.add_command(label='  Debug', command= lambda event=None: debug())

ic_salva = PhotoImage(file='imagens/ic_salvar.png')
ic_playP = PhotoImage(file='imagens/ic_play.png')
ic_PStop = PhotoImage(file='imagens/ic_parar.png')
ic_breaP = PhotoImage(file='imagens/ic_play_breakpoint.png')
ic_brk_p = PhotoImage(file='imagens/breakPoint.png')
ic_desfz = PhotoImage(file='imagens/left.png')
ic_redsf = PhotoImage(file='imagens/right.png')
ic_ajuda = PhotoImage(file='imagens/ic_duvida.png')
ic_pesqu = PhotoImage(file='imagens/ic_pesquisa.png')

ic_salva = ic_salva.subsample(4, 4)
ic_playP = ic_playP.subsample(4, 4)
ic_PStop = ic_PStop.subsample(4, 4)
ic_breaP = ic_breaP.subsample(4, 4)
ic_brk_p = ic_brk_p.subsample(4, 4)
ic_desfz = ic_desfz.subsample(4, 4)
ic_redsf = ic_redsf.subsample(4, 4)
ic_ajuda = ic_ajuda.subsample(4, 4)
ic_pesqu = ic_pesqu.subsample(4, 4)

fr_opc_rapidas = Frame(frame_tela)

bt_salva = Button(fr_opc_rapidas, image=ic_salva, relief=RAISED, command= lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo"))
bt_playP = Button(fr_opc_rapidas, image=ic_playP, relief=RAISED, command = inicializa_orquestrador)
bt_breaP = Button(fr_opc_rapidas, image=ic_breaP, relief=RAISED, command = lambda event=None: inicializa_orquestrador(libera_break_point_executa = True))
bt_brk_p = Button(fr_opc_rapidas, image=ic_brk_p, relief=RAISED, command = adiciona_remove_breakpoint)
bt_desfz = Button(fr_opc_rapidas, image=ic_desfz, relief=RAISED)
bt_redsf = Button(fr_opc_rapidas, image=ic_redsf, relief=RAISED)
bt_ajuda = Button(fr_opc_rapidas, image=ic_ajuda, relief=RAISED)
bt_pesqu = Button(fr_opc_rapidas, image=ic_pesqu, relief=RAISED)

fr_princ = Frame(frame_tela, bg='red')
fr_princ.grid_columnconfigure(2, weight=1)
fr_princ.rowconfigure(1, weight=1)

fr_abas = Frame(fr_princ, height=20)
fr_abas.rowconfigure(1, weight=1)
fr_espaco = Label(fr_abas, width=4)

renderizar_abas_inicio()

fr_espaco.grid(row=1, column=0, sticky=NSEW)

tx_codfc = EditorDeCodigo(fr_princ)
tx_codfc.bind("<<Change>>", atualizacao_linhas)
tx_codfc.bind("<Configure>", atualizacao_linhas)
tx_codfc.bind('<Button>', obterPosicaoDoCursor)
tx_codfc.bind('<KeyRelease>', lambda event = None: ativar_coordernar_coloracao(event))
tx_codfc.focus_force()
 
sb_codfc = Scrollbar(fr_princ, orient="vertical", command=tx_codfc.yview, relief=FLAT)
tx_codfc.configure(yscrollcommand=sb_codfc.set)
linhas_laterais = ContadorLinhas(fr_princ)
linhas_laterais.atribuir(tx_codfc)

fr_opc_rapidas.grid(row=1, column=1, sticky=NSEW, columnspan=2)
bt_salva.grid(row=1, column=1)
bt_playP.grid(row=1, column=4)
bt_breaP.grid(row=1, column=5)
bt_brk_p.grid(row=1, column=6)
bt_desfz.grid(row=1, column=7)
bt_redsf.grid(row=1, column=8)
bt_ajuda.grid(row=1, column=10)
bt_pesqu.grid(row=1, column=11)
fr_princ.grid(row=2, column=1, sticky=NSEW)
fr_abas.grid(row=0, column=1, columnspan=4, sticky=NSEW)
linhas_laterais.grid(row=1, column=1, sticky=NSEW)
tx_codfc.grid(row=1, column=2, sticky=NSEW)
sb_codfc.grid(row=1, column=3, sticky=NSEW)

atualiza_design_interface()

controle_arquivos = Arquivo(dic_abas, aba_focada, tx_codfc)

tela.update()

tela.withdraw() # Ocultar tkinter
t_width    = tela.winfo_screenwidth()
t_heigth   = tela.winfo_screenheight()
tela.geometry("{}x{}+0+0".format(t_width, t_heigth))
tela.deiconify()

tela.update()
#funcoes_arquivos_configurar(None, "abrirArquivo", 'game.fyn')

tela.mainloop()
