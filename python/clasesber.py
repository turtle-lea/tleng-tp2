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
#Por ejemplo, A -> id, A -> A id. Notar que los elementos de la lista están en orden inverso
class ExpressionList(Expression):
    def __init__(self, current, nextList):
        self._list = [current] + nextList

    def getList(self):
        return self._list

class Const(Expression):
    def __init__(self, cname, val, isPointer):
        self._cname = cname
        self._value = val
        self._isPointer = isPointer

    def getName(self):
        return self._cname

    def getValue(self):
        return self._value

 #   def setValue(self, value):
 #       self._value = value


    def isPointer(self):
        return self._isPointer

class LexerValue(Expression):
    def getValue(self):
        pass
    def __eq__(self, other):
        return self.getValue() == other.getValue()

class ConstValue(LexerValue):
    def __init__(self, cname):
        self._cname = cname
    def getValue(self):
        #Devolver el valor de la constante usando constant manager
        return ConstantManager.getInstance().getValue(self._cname)


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
    def __init__(self, current, nextList):
        if nextList != [] and current.getDuration() != nextList[0].getDuration():
            raise Exception("Los compases no tienen la misma duración.")

        self._duration = current.getDuration()
        super(CompasList,self).__init__(current, nextList)

    def getDuration(self):
        return self._duration

class ConstantManager:
    @staticmethod
    def createInstance(constList, reserved):
        ConstantManager._instance = ConstantManager(constList, reserved)

    @staticmethod
    def getInstance():
        if ConstantManager._instance == None:
            ConstantManager.createInstance([],[])
        return ConstantManager._instance


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
                    raise Exception("La constante <{0}> apunta al nombre <{1}> que no está definido".format(const.getName(),nextcname))
                visited.append(nextcname)
            else:
                #const.setValue(next.getValue())
                found = True

        return next.getValue()

