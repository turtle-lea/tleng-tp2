#!/usr/bin/python
# -*- coding: latin-1 -*-
from clasesber import *
from lexer_rules import tokens


#Una constante que es un número
def p_initial(subexpressions):
    'expr : constlist'
    subexpressions[0] = subexpressions[1]

def p_val_num(subexpression):
    'value : NUM'
    subexpression[0] = NumValue(int(subexpression[1]))

def p_val_cname(subexpression):
    'value : CNAME'
    subexpression[0] = ConstValue(subexpression[1])


def p_const(subexpressions):
    'const : CONST CNAME EQUALS NUM SEMICOLON'
    subexpressions[0] = Const(subexpressions[2],subexpressions[4], False)

#Una constante que es un puntero a otra constante
def p_const_cname(subexpressions):
    'const : CONST CNAME EQUALS CNAME SEMICOLON'
    subexpressions[0] = Const(subexpressions[2],subexpressions[4], True)


def p_const_list_base(subexpressions):
    'constlist : const'
    subexpressions[0] = ConstList(subexpressions[1],None)

def p_const_list_rec(subexpressions):
    'constlist : constlist const'
    subexpressions[0] = ConstList(subexpressions[2],subexpressions[1])


# def p_voice_content_base_compas(subexpressions):
#     'voicecontent : compas'
#     subexpressions[0] = VoiceContent(subexpressions[1],None)
#
# def p_voice_content_rec_compasloop(subexpressions):
#     'voicecontent : voicecontent compasloop'
#     subexpressions[0] = VoiceContent(subexpressions[2],subexpressions[1])
#
# def p_voice_content_rec_compas(subexpressions):
#     'voicecontent : voicecontent compas'
#     subexpressions[0] = VoiceContent(subexpressions[2],subexpressions[1])


def p_error(subexpressions):
    raise Exception("Syntax error.")
