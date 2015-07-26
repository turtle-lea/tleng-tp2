tokens = [
   'COMMENT',
   'NUM',
   'CONST',
   'EQUALS',
   'CNAME',
   'SILENCEBEGIN',
   'SEMICOLON',
   'VOICEBEGIN',
   'LEFTPAR',
   'RIGHTPAR',
   'LEFTCURL',
   'RIGHTCURL',
   'COMPASBEGIN',
   'COMPASHEADERBEGIN',
   'LOOPBEGIN',
   'SLASH',
   'NOTEBEGIN',
   'SHAPE',
   'PUNTO',
   'ALTER',
   'NOTENAME',
   'COMMA',
   'NEWLINE',
   'TEMPOBEGIN'
]

#Ignoro espacios y tabs
t_ignore  = ' \t'

#Ignorar comoentarios
def t_COMMENT(token):
  r'//.*'

def t_NEWLINE(token):
  r"\n+"
  token.lexer.lineno += len(token.value)

#Chequear regexs con: https://regex101.com/#python
# Tener en cuenta poner las expresiones que matchean strings mas largos primero cuando hay ambiguedad.
# Usamos '\s' para matchear espacios en blanco
def t_TEMPOBEGIN(token):
  r"\#tempo"
  return token

def t_CONST(token):
  r"const"
  return token

def t_EQUALS(token):
  r"\="
  return token

def t_SEMICOLON(token):
  r"\;"
  #print ("semicolon")
  return token

def t_VOICEBEGIN(token):
  r"voz"
  return token

def t_LEFTPAR(token):
  r"\("
  return token

def t_RIGHTPAR(token):
  r"\)"
  return token

def t_LEFTCURL(token):
  r"\{"
  return token

def t_RIGHTCURL(token):
  r"\}"
  return token

def t_COMPASHEADERBEGIN(token):
  r"\#compas"
  return token

def t_COMPASBEGIN(token):
  r"compas"
  return token

def t_LOOPBEGIN(token):
  r"repetir"
  return token

def t_SLASH(token):
  r"/"
  return token

def t_NOTEBEGIN(token):
  r"nota"
  return token

def t_SILENCEBEGIN(token):
  r"silencio"
  return token

def t_PUNTO(token):
  r"\."
  return token

def t_ALTER(token):
  r"\+|\-"
  return token

def t_SHAPE(token):
  r"blanca|negra|redonda|semicorchea|corchea|semifusa|fusa"
  return token

def t_NOTENAME(token):
  r"do|re|mi|fa|sol|la|si"
  return token

def t_COMMA(token):
  r"\,"
  return token

def t_CNAME(token):
  r"(([a-z]|[A-Z])([0-9]|[a-z]|[A-Z])*)"
  return token

def t_NUM(token):
    r"([0]|[1-9][0-9]*)"
    token.value = int(token.value)
    return token

def t_error(token):
    message = "[Lexer] Token desconocido"
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)



