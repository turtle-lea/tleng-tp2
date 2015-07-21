#!/usr/bin/python
# -*- coding: latin-1 -*-
#1)H
#2)TEMPO
#3)CONST
#4)VOICELIST
#5)VOICE
#6)VOICECONTENT
#7)COMPAS
#8)COMPASLOOP
#9)COMPASLIST
#10)NOTELIST
#11)NOTE
#12)SILENCE

class Expression(object):
    pass


#Representa una lista como un valor y un puntero a otra lista
#Por ejemplo, A -> id, A -> A id. Notar que los elementos de la lista est�n en orden inverso
class ExpressionList(Expression):
    def __init__(self, current, nextList):
        self._current = current
        self._nextList = nextList

    #Devuelve el elemento en la cabeza del nodo
    def getCurrent(self):
        return self._current

    #Devuelve la recuesi�n (cola de la lista)
    def getNext(self):
        return self._nextList

    #Hace la recursi�n sobre un nodo de una producci�n recursiva a izquierda y devuelve una lista lineal
    def getList(self):
        ret = [self._current]
        next = self._nextList
        while (next != None):
            ret.insert(0, next.getCurrent())
            next = next.getNext()

        return ret


class Const(Expression):
    def __init__(self, cname, val, isPointer):
        self._cname = cname
        self._value = val
        self._isPointer = isPointer

    def getName(self):
        return self._cname

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value


    def isPointer(self):
        return self._isPointer

class LexerValue(Expression):
    def getValue(self):
        pass

class ConstValue(LexerValue):
    def __init__(self, cname):
        self._cname = cname
    def getValue(self):
        #Devolver el valor de la constante usando constant manager
        pass


class NumValue(LexerValue):
    def __init__(self, val):
        self._val = val
    def getValue(self):
        return self._val


class ConstList(ExpressionList):
    pass

class VoiceContent(ExpressionList):
    pass

class CompasList(ExpressionList):
    pass


class Silence(Expression):
    def __init__(self,time, shape):
        self._shape = shape
        self._time = time

    def getTime(self):
        return self._time

    def getShape(self):
        return self._shape


class ConstantManager:
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
        self.dictConst[cname] = const

    #Devuelve el valor de una constante. Si es una referencia a otra constante, calcula primero el valor recursivamente (y lo cachea)
    def getValue(self, cname):
        const = self.dictConst.get(cname)
        if const == None:
            raise Exception("Constante no definida")
        else:
            constVal = self.resolveVal(const)

        return constVal


    #Calcula el valor de una constante. Si es num�rica (caso base), devuelve su valor.
    #Si es un puntero, busca el valor de la constante a la que apunta (recursivamente), chequeando que no hayan loops.
    def resolveVal(self, const):
        if (not const._isPointer):
            return const.getValue()

        found = False;
        visited = [const.getName()]
        next = const
        while(not found):
            if (next.isPointer()):
                nextcname = next.getValue()
                if visited.count(nextcname) > 0:
                    raise Exception("Definici�n circular de constante <{0}>".format(const.getName()))

                next = self.dictConst.get(nextcname)
                if (next == None):
                    raise Exception("La constante <{0}> apunta al nombre <{1}> que no est� definido".format(const.getName(),nextcname))
                visited.append(nextcname)
            else:
                #const.setValue(next.getValue())
                found = True

        return next.getValue()

