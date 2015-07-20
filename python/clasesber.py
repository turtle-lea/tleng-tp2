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


class ExpressionList(Expression):
    def _init(self, current, nextList):
        self._current = current
        self._nextList = nextList

    def getCurrent(self):
        return self._current

    def getNext(self):
        return self._nextList


class Const(Expression):
    def _init(self, cname, val):
        self._cname = cname
        self._value = val

    def getName(self):
        return self._cname

    def getValue(self):
        return self._value


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





