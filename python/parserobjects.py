#!/usr/bin/python
# -*- coding: latin-1 -*-
__author__ = 'AAAA'

#En este archivo implementamos todas las clases que representan los objetos que se van parseando (no terminales),
#algunas clases auxiliares y el manejador de constantes.

#Clase abstracta que representa expresiones (nodos en a gramática)
class Expression(object):
    pass

#Representa una lista como un valor y un puntero a otra lista
#Por ejemplo, A -> id, A -> A id.
# Notar que los elementos de la lista están en orden inverso
class ExpressionList(Expression):
    def __init__(self, current, nextList):
        self._list = nextList + [current]

    def getList(self):
        return self._list

#Representa un nodo del elmento const en la gramática
class Const(Expression):
    def __init__(self, cname, val, isPointer):
        self._cname = cname
        self._value = val
        self._isPointer = isPointer

    def getName(self):
        return self._cname

    def getValue(self):
        return self._value

    #indica si la constante apunta a otra constante
    def isPointer(self):
        return self._isPointer


#Representa una lista de constantes
class ConstList(ExpressionList):
    pass

#Representa la lista de contenido de una voz (compaces o loops)
class VoiceContent(ExpressionList):
    def __init__(self, current, nextList):
        if nextList != [] and current.getDuration() != nextList[0].getDuration():
            raise Exception("Se detectó un compas dentro de una voz con duración distinta al resto de los compases dentro de la misma.")

        self._duration = current.getDuration()
        super(VoiceContent,self).__init__(current, nextList)

    def getDuration(self):
        return self._duration

#Representa una lista de constantes dentro de un loop
class CompasList(ExpressionList):
    def __init__(self, current, nextList):
        if nextList != [] and current.getDuration() != nextList[0].getDuration():
            raise Exception("Se detectaron compases con distinta duración dentro de un bucle.")

        self._duration = current.getDuration()
        super(CompasList,self).__init__(current, nextList)

    def getDuration(self):
        return self._duration

#Manejador de constantes. Mantiene una lista de todas las constantes declaradas y permite obtener
#los valores de las mismas dado un nombre de constante.
class ConstantManager:
    #Inicializa el manejador de constantes dada una lista de objetos tipo Const.

    @staticmethod
    def createInstance(constList, reserved):
        ConstantManager._instance = ConstantManager(constList, reserved)

    @staticmethod
    def getInstance():
        if ConstantManager._instance == None:
            ConstantManager.createInstance([],[])
        return ConstantManager._instance


    #Inicialización y validación de consistencia de la declaración de constantes
    def __init__(self, constList, reserved):
        self.dictConst = {}
        for c in constList:
            if reserved.count(c.getName()) > 0:
                raise Exception("El nombre de constante <{0}> es una palabra reservada".format(c.getName()))

            self.Add (c.getName(), c)

        #Pido los valores de todas las ctes para que se validen
        for c in constList:
            self.getValue(c.getName())

    def Add(self, cname, const):
        if self.dictConst.get(cname) != None:
            raise Exception("Constante duplicada: {0}".format(cname))

        self.dictConst[cname] = const

    #Devuelve el valor de una constante. Si es una referencia a otra constante, calcula primero el valor recursivamente
    def getValue(self, cname):
        const = self.dictConst.get(cname)
        if const == None:
            raise Exception("Constante no definida: {0}".format(cname))
        else:
            constVal = self.resolveVal(const)

        return constVal


    #Calcula el valor de una constante. Si es numérica (caso base), devuelve su valor.
    #Si es un puntero, busca el valor de la constante a la que apunta (recursivamente), chequeando que no hayan loops.
    def resolveVal(self, const):
        if (not const._isPointer):
            return const.getValue()

        found = False
        visited = [const.getName()]
        next = const
        while(not found):
            if (next.isPointer()):
                nextcname = next.getValue()
                if visited.count(nextcname) > 0:
                    raise Exception("Definición circular de constante <{0}>".format(const.getName()))

                next = self.dictConst.get(nextcname)
                if (next == None):
                    raise Exception("La constante <{0}> apunta (directa o indirectamente) al nombre <{1}> que no está definido".format(const.getName(),nextcname))
                visited.append(nextcname)
            else:
                #const.setValue(next.getValue())
                found = True

        return next.getValue()



class Tempo(Expression):
    def __init__(self, shape, num):
        self._shape = shape
        self._num = num

    def getFigure(self):
        return self._shape

    def getCount(self):
        return self._num

    def getShapeDuration(self):
        return duration_from_shape(self.getFigure())

#Representa el nodo que define la duración de los compaces para toda la partitura
class CompasHeader(Expression):
    def __init__(self, num1, num2):
        if num2 == 0:
            raise Exception("El denominador del compas debe ser mayor a cero")
        self._numerator = num1
        self._denominator = num2


    #Devuelve la duración del compas, en redondas
    def getDuration(self):
        return float(self._numerator) / float(self._denominator)


    def getDenominator(self):
        return self._denominator


    def getNumerator(self):
        return self._numerator

#Representa un nodo voz(N)
class Voice(Expression):
    def __init__(self, value, voiceContent):
        if value > 127:
          raise Exception("El instrumento {0} es inválido".format(value))

        self._value = value
        self._compasses = voiceContent.getList()

    def getInstrument(self):
        return self._value

    def getCompasses(self):
        return self._compasses


#Representa un nodo repetir(N) con una lista de compaces adentro
class CompasLoop(Expression):
    def __init__(self, value, compasList):
        if value < 1:
            raise Exception("Existe un bucle con cantidad de repeticiones 0. Los bucles deben tener al menos una repeticion.")

        self._compasList = compasList
        self._value = value
        self._duration = compasList.getDuration()


    def getRepeat(self):
        return self._value

    def getCompasses(self):
        return self._compasList

    def getDuration(self):
        return self._duration

    def isLoop(self):
        return True


def duration_from_shape(shape):
    if shape == 'redonda':
        duration = 1.0
    elif shape == 'blanca':
        duration = 1.0 / 2.0
    elif shape == 'negra':
        duration = 1.0 / 4.0
    elif shape == 'corchea':
        duration = 1.0 / 8.0
    elif shape == 'semicorchea':
        duration = 1.0 / 16.0
    elif shape == 'fusa':
        duration = 1.0 / 32.0
    elif shape == 'semifusa':
        duration = 1.0 / 64.0
    else:
        raise Exception("Figura no definida")
    return duration


class Silence(Expression):
    def __init__(self, duration, puntillo):
        self._duration = duration_from_shape(duration)
        if puntillo:
            self._duration = self._duration * (3.0 / 2.0)

    def getDuration(self):
        return self._duration

    def getShape(self):
        return self._shape

    def isSilence(self):
        return True


class Note(Expression):
    def __init__(self, notename, alter, value, shape, puntillo):
        if value < 1 or value > 9:
            raise Exception("La octava {0} es inválida".format(value))

        # concatenacion de string
        if alter != None:
            self._height = notename + alter
        else:
            self._height = notename

        self._value = value
        self._duration = duration_from_shape(shape)

        if puntillo:
            self._duration = self._duration * (3.0 / 2.0)


    def getOctave(self):
        return self._value

    def getHeight(self):
        return self._height

    def getDuration(self):
        return self._duration

    def isSilence(self):
        return False

#Objeto nodo principal
class Root(Expression):
    def __init__(self, tempo, compasheader,constlist,voicelist):
        ### El tiempo del primer compas de la primera voz debe coincidir con el compasheader
        if voicelist.getList()[0].getCompasses()[0].getDuration() != compasheader.getDuration():
          raise Exception("La duracion de los compases es distinta a la del encabezado")
        self._tempo = tempo
        self._compasheader = compasheader
        self._constlist = constlist
        self._voicelist = voicelist

    def getDuration(self):
        return self._tempo

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
            if (voice.getCompasses()[0].getDuration() != voicelist[0].getCompasses()[0].getDuration()):
                raise Exception("La duracion de los compases de las voces son distintas")
            if len(voicelist)>=16:
            	raise Exception("La cantidad de voces supera las 16")
        self._voicelist = voicelist + [voice]

    def getList(self):
        return self._voicelist

class Compas(Expression):
    def __init__(self, notelist):
        self._notelist = notelist
        ### Calculo la duracion del compas
        duration = 0.0
        for note in notelist:
            duration += note.getDuration()
        self._duration = duration

    def getDuration(self):
      return self._duration

    def isLoop(self):
        return False

    def getNoteList(self):
        return self._notelist

class NoteList(Expression):
    def __init__(self, note, notelist):
        self._notelist = notelist + [note]

    def getNoteList(self):
      return self._notelist

