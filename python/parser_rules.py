from clasesber import *
from lexer_rules import tokens


def p_const_num(subexpressions):
    'const : CONST CNAME EQUALS NUM'
    subexpressions[0] = Const(subexpressions[2],subexpressions[4])

def p_const_cname(subexpressions):
    'const : CONST CNAME EQUALS CNAME'
    subexpressions[0] = Const(subexpressions[2],subexpressions[4])


def p_const_list_base(subexpressions):
    'constlist : const'
    subexpressions[0] = ConstList(subexpressions[1],None)

def p_const_list_rec(subexpressions):
    'constlist : constlist const'
    subexpressions[0] = ConstList(subexpressions[2],subexpressions[1])


def p_voice_content_base_compas(subexpressions):
    'voicecontent : compas'
    subexpressions[0] = VoiceContent(subexpressions[1],None)

def p_voice_content_rec_compasloop(subexpressions):
    'voicecontent : voicecontent compasloop'
    subexpressions[0] = VoiceContent(subexpressions[2],subexpressions[1])

def p_voice_content_rec_compas(subexpressions):
    'voicecontent : voicecontent compas'
    subexpressions[0] = VoiceContent(subexpressions[2],subexpressions[1])


def p_error(subexpressions):
    raise Exception("Syntax error.")
