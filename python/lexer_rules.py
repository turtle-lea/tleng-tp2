H-> {TEMPO}{COMPASHEADER}{CONST}{VOICELIST}
TEMPO-> {#tempo}{space}{shape}{space}{num}{newline}

COMPASHEADER-> {compasheaderbegin}{space}{num}{slash}{num}{newline}

CONST-> {const}{space}{cname}{equals}{cname}{semicolon}{newline}CONST
CONST-> {const}{space}{cname}{equals}{num}{semicolon}{newline}CONST
CONST-> {const}{space}{cname}{equals}{cname}{semicolon}{newline}
CONST-> {const}{space}{cname}{equals}{num}{semicolon}{newline}


VOICELIST->{VOICE}{VOICELIST}
VOICELIST->{VOICE}

VOICE->{vozbegin}{leftpar}{num}{rightpar}{leftcurl}{VOICECONTENT}{rightcurl}
VOICE->{vozbegin}{leftpar}{const}{rightpar}{leftcurl}{VOICECONTENT}{rightcurl}

VOICECONTENT -> {COMPAS}
VOICECONTENT -> {COMPASLOOP}
VOICECONTENT -> {COMPAS}{VOICECONTENT}
VOICECONTENT -> {COMPASLOOP}{VOICECONTENT}

COMPAS->{compasbegin}{leftcurl}{NOTELIST}{rightcurl}

COMPASLOOP->{loopbegin}{leftpar}{cname}{rightpar}{leftcurl}{COMPASLIST}{rightcurl}
COMPASLOOP->{loopbegin}{leftpar}{num}{rightpar}{leftcurl}{COMPASLIST}{rightcurl}

COMPASLIST->{COMPAS}
COMPASLIST->{COMPAS}{COMPASLIST}

NOTELIST->{NOTE}
NOTELIST->{NOTE}{NOTELIST}

NOTE->{notebegin}{leftpar}{notename}{comma}{num}{comma}{shape}{rightpar}{semicolon}
NOTE->{notebegin}{leftpar}{notename}{comma}{const}{comma}{shape}{rightpar}{semicolon}

COMMENT -> {commenttoken}{anything}{newline}
COMMENT -> {commenttoken}{anything}{eof}

// Donde se pueden usar las constantes?
// Los nombres de las constantes pueden empezar CON numeros?
