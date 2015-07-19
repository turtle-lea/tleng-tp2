tokens = [
   'NUM',
   'CONST',
   'EQUALS',
   'CNAME',
   'SEMICOLON',
   'VOZBEGIN',
   'LEFTPAR',
   'RIGHTPAR',
   'LEFTCURL',
   'RIGHTCURL',
   'COMPASBEGIN',
   'COMPASHEADERBEGIN',
   'LOOPBEGIN',
   'SLASH',
   'NOTEBEGIN',
   'SILENCEBEGIN',
   'SHAPE',
   'COMMA',
   'NEWLINE',
   'TEMPOBEGIN',
   'NOTENAME',
   'COMMENT'
]

#Ojo, probar que esto ande bien
#Ignorar comoentarios
t_ignore_COMMENT = r'//.*'
#Ignoro espacios y tabs
t_ignore  = ' \t'

def t_NEWLINE(token):
  r"\n+"
  token.lexer.lineno += len(token.value)

#Chequear regexs con: https://regex101.com/#python
# Tener en cuenta poner las expresiones que matchean strings mas largos primero cuando hay ambiguedad.
# Usamos '\s' para matchear espacios en blanco
t_TEMPOBEGIN = r"\#tempo"
t_CONST = r"const"
t_EQUALS = r"\="
t_SEMICOLON = r"\;"
t_VOZBEGIN = r"voz"
t_LEFTPAR = r"\("
t_RIGHTPAR =r"\)"
t_LEFTCURL =r"\{"
t_RIGHTCURL =r"\}"
t_COMPASHEADERBEGIN =r"\#compas"
t_COMPASBEGIN =r"compas"
t_LOOPBEGIN =r"repetir"
t_SLASH =r"/"
t_NOTEBEGIN =r"nota"
t_SILENCEBEGIN =r"silencio"
t_SHAPE = r"(blanca|negra|redonda|semicorchea|corchea|semifusa|fusa)?(\.)"
t_NOTENAME=r"(do|re|mi|fa|sol|la|si)?(\+|\-)"
t_COMMA =r"\,"
t_CNAME =r"([a-z]|[A-Z])([0-9]|[a-z]|[A-Z])*"

def t_NUM(token):
	r"([0]|[1-9][0-9]*)"
	token.value = int(token.value)
	return token

def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
