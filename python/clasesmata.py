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
            if (len(voice.getCompasses() != len(voicelist.first.getCompasses()):
                raise Exception("Las voces tienen distinta cantidad de compases")
            ### Un compás de la nueva voz tiene que durar lo mismo que un compás de la lista
            if (voice.getCompasses().first.getTempo() != voicelist.first.getCompasses().first.getTempo()):
                raise Exception("La duracion de los compases de las voces son distintas")
        self._voicelist = voicelist ++ voice


class Compas(Expression):
    def _init(self, notelist):
        self._notelist = notelist
        ### Calculo la duracion del compas
        duracion = 0
        for note in notelist:
            acum += note.getduration()
        self._tempo = duracion

    def getTempo():
      return self._tempo

class Notelist(Expression):
    def _init(self, note, notelist = []):
        self._notelist = notelist ++ note

    def getNoteList():
      return self._notelist






