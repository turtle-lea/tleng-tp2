from parserobjects import *

import lexer_rules
import parser_rules

from sys import argv, exit
from midi import *
from ply.lex import lex
from ply.yacc import yacc


if __name__ == "__main__":
    if len(argv) != 3:
        print ("Invalid arguments.")
        print ("Use:")
        print ("  parser.py <archivo_entrada> <archivo_salida>")
        exit(1)

    try:
        inputfile = argv[1]
        outputfile = argv[2]

        with open (inputfile, "r") as myfile:
            text=myfile.read()


        lexer = lex(module=lexer_rules)
        parser = yacc(module=parser_rules)

        expression = parser.parse(text, lexer)
        midi = MidiTranslator()

        with open (outputfile, "w") as file_output:
            midi.generateMIDIFile(expression,file_output)


    except Exception as ex:
        print('ERROR:')
        for v in ex.args:
            print(str(v))

        exit(1)

