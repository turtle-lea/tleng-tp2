#!/usr/bin/python
# -*- coding: latin-1 -*-

from clasesber import *
from clasesleanv import *

class Root(Expression):
    def __init__(self, tempo, compasheader,constlist,voicelist):
        ### El tiempo del primer compas de la primera voz debe coincidir con el compasheader
        if (getTempo(voicelist.first.getCompasses().first) != compasheader.getTempo()):
          raise Exception("La duracion de los compases es distinta a la del encabezado")
        self._tempo = tempo
        self._compasheader = compasheader
        self._constlist = constlist
        self._voicelist = voicelist

    def getTempo(self):
        return self._tempo

    def getCompasHeader(self):
        return self._compasheader

    def getConstList(self):
        return self._constlist

    def getVoiceList(self):
        return self._voicelist

class VoiceList(Expression):
    def __init__(self, voice, voicelist=[]):
        if len(voicelist)>0:
            ### Deberíamos reescribir esto. Encapsular mediante funciones
            #if (len(voice.getCompasses() != len(voicelist.first.getCompasses()):
            #    raise Exception("Las voces tienen distinta cantidad de compases")
            ### Un compás de la nueva voz tiene que durar lo mismo que un compás de la lista
            if (voice.getCompasses().first.getDuration() != voicelist.first.getCompasses().first.getTempo()):
                raise Exception("La duracion de los compases de las voces son distintas")
            if len(voicelist)>=16:
            	raise Exception("La cantidad de voces supera 16")
        self._voicelist = voicelist ++ voice

    def getList(self):
        return self._voicelist

class Compas(Expression):
    def __init__(self, notelist):
        self._notelist = notelist
        ### Calculo la duracion del compas
        duration = 0
        for note in notelist:
            duration += note.getDuration()
        self._duration = duration

    def getDuration(self):
      return self._duracion

    def isLoop(self):
        return False

class NoteList(Expression):
    def __init__(self, note, notelist):
        self._notelist = notelist ++ note

    def getNoteList(self):
      return self._notelist






