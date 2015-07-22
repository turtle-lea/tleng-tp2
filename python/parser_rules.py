#!/usr/bin/python
# -*- coding: latin-1 -*-
from clasesber import *
from clasesleanv import *
from clasesmata import *
from lexer_rules import tokens

def p_root(subexpressions):
    'h : tempo compasheader constlistinit voicelist'
    subexpressions[0] = Root(subexpressions[1], subexpressions[2], subexpressions[3], subexpressions[4])

def p_tempo(subexpression):
    'tempo : TEMPOBEGIN SHAPE NUM'
    subexpression[0] = Tempo(subexpression[2], int(subexpression[3]))
def p_voice_list_base(subexpression):
    'voicelist : voice'
    subexpression[0] = VoiceList(subexpression[1])

def p_voice_list_rec(subexpressions):
    'voicelist : voicelist voice'
    ### Invierto parametros intencionalmente. voicelist param es opcional en el new de la clase
    subexpressions[0] = VoiceList(subexpressions[2], subexpressions[1].getList())

def p_compas(subexpressions):
    'compas: COMPASBEGIN LEFTCURL notelist RIGHTCURL'
    subexpressions[0] = Compas(subexpressions[3])

def p_note_list_base(subexpression):
    'notelist : note'
    subexpression[0] = NoteList(subexpression[1])

def p_note_list_rec(subexpressions):
    'notelist : notelist note'
    ### Invierto parametros intencionalmente. notelist param es opcional en el new de la clase
    subexpressions[0] = NoteList(subexpressions[2], subexpressions[1])

def p_val_num(subexpression):
    'value : NUM'
    #subexpression[0] = NumValue(int(subexpression[1]))
    subexpression[0] = int(subexpression[1])


def p_val_cname(subexpression):
    'value : CNAME'
    #subexpression[0] = ConstValue(subexpression[1])
    subexpression[0] = ConstantManager.getInstance().getValue(subexpression[1])
def p_const(subexpressions):
    'const : CONST CNAME EQUALS NUM SEMICOLON'
    subexpressions[0] = Const(subexpressions[2],subexpressions[4], False)

#Una constante que es un puntero a otra constante
def p_const_cname(subexpressions):
    'const : CONST CNAME EQUALS CNAME SEMICOLON'
    subexpressions[0] = Const(subexpressions[2],subexpressions[4], True)

#Es un pasamanos para poder inicializar el ConstantManager y que pueda ser usado por las otras producciones
#(esto asume que las constantes se declaran primero en el header)
def p_const_list_init(subexpressions):
    'constlistinit : constlist'
    subexpressions[0] = subexpressions[1]
    #Sabemos que subexpressions[0] es un constlist, inicializamos el Constantmanager para que el resto
    #de las producciones puedan referenciar constantes.
    #TODO: Pasarle el reserved del Lexer
    ConstantManager.createInstance (subexpressions[0].getList(),[] )


def p_const_list_base(subexpressions):
    'constlist : const'
    subexpressions[0] = ConstList(subexpressions[1],[])

def p_const_list_rec(subexpressions):
    'constlist : constlist const'
    subexpressions[0] = ConstList(subexpressions[2],subexpressions[1].getList())


def p_voice_content_base_loop(subexpressions):
    'voicecontent : compasloop'
    subexpressions[0] = VoiceContent(subexpressions[1],[])

def p_voice_content_base_compas(subexpressions):
    'voicecontent : compas'
    subexpressions[0] = VoiceContent(subexpressions[1],[])

def p_voice_content_rec_compasloop(subexpressions):
    'voicecontent : voicecontent compasloop'
    subexpressions[0] = VoiceContent(subexpressions[2],subexpressions[1].getList())

def p_voice_content_rec_compas(subexpressions):
    'voicecontent : voicecontent compas'
    subexpressions[0] = VoiceContent(subexpressions[2],subexpressions[1].getList())


def p_error(subexpressions):
    raise Exception("Syntax error.")
