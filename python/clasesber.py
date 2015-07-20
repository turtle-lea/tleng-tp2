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
    def _init(self, current, nextList):
        self._current = current
        self._nextList = nextList

    #Devuelve el elemento en la cabeza del nodo
    def getCurrent(self):
        return self._current

    #Devuelve la recuesión (cola de la lista)
    def getNext(self):
        return self._nextList

    #Hace la recursión sobre un nodo de una producción recursiva a izquierda y devuelve una lista lineal
    def getList(self):
        ret = [self._current]
        next = self._nextList
        while (next != None):
            ret.insert(0, next.getCurrent())
            next = next.getNext()

        return ret


class Const(Expression):
    def _init(self, cname, val, isPointer):
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
        return self.isPointer()


class ConstList(ExpressionList):
    pass

class VoiceContent(ExpressionList):
    pass

class CompasList(ExpressionList):
    pass


class Silence(Expression):
    def _init(self,time, shape):
        self._shape = shape
        self._time = time

    def getTime(self):
        return self._time

    def getShape(self):
        return self._shape


class ConstantManager:
    _instance = None
    @staticmethod
    def GetInstance():
        if ConstantManager._instance == None:
            ConstantManager._instance = ConstantManager()

        return ConstantManager._instance

    def __init__(self):
        self.dictConst = {}

    def Add(self, cname, const):
        self.dictConst[cname] = const

    #Devuelve el valor de una constante. Si es una referencia a otra constante, calcula primero el valor recursivamente (y lo cachea)
    def GetValue(self, cname):
        const = self.dictConst.get(cname)
        if const == None:
            raise Exception("Constante no definida")
        else:
            constVal = self.resolveVal(const)

        return constVal

    #Calcula el valor de una constante. Si es numérica (caso base), devuelve su valor.
    #Si es un puntero, busca el valor de la constante a la que apunta (recursivamente), chequeando que no hayan loops.
    def resolveVal(self, const):
        if  const.isPointer():
            visited = [const.getName()]
            next = const.getValue()
            found = False
            while(not found):
                if visited.count(next) > 0:
                    raise Exception("Definición circular de constante {0}")

                visited.append(next)

                constnext = self.dictConst.get(next)

                if (constnext == None):
                    raise Exception("La constante {0} apunta al nombre {1} que no está definido")

                if (constnext.isPointer):
                    next = constnext.getValue()
                else:
                    const.setValue(next.getValue())
                    found = True

        return const.getValue()