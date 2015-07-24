#!/usr/bin/python
# -*- coding: latin-1 -*-
from clasesber import *
from clasesmata import *


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


class CompasHeader(Expression):
    def __init__(self, num1, num2):
        if num2 == 0:
            raise Exception("El denominador del compas debe ser mayor a cero")
        self._numerator = num1
        self._denominator = num2


    def getDuration(self):
        return float(self._numerator) / float(self._denominator)


    def getDenominator(self):
        return self._denominator


    def getNumerator(self):
        return self._numerator


class Voice(Expression):
    def __init__(self, value, voiceContent):
        self._value = value
        self._compasses = voiceContent.getList()

    def getInstrument(self):
        return self._value

    def getCompasses(self):
        return self._compasses



class CompasLoop(Expression):
    def __init__(self, value, compasList):
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