#2)TEMPO
#5)VOICE
#8)COMPASLOOP
#11)NOTE

#tempo -> {#tempo}{shape}{num}

#voice -> voice ( value ) { voicecontent }

#compasloop -> compasloop ( value ) { compaslist }

#note -> note ( notename , value , shape ) ;

#value -> num|cname

class Tempo(Expression):

	def __init__(self, shape, num):
		self._shape = shape
		self._num = num

	def getFigure(self):
		return self._shape

	def getCount(self):
		return self._num


class Voice(Expression):

	def __init__(self, value, VoiceContent):
		self._value = value
		self._compasses = VoiceContent.getList()

	def getInstrument(self):
		return self._value

	def getCompasses(self):
		return self._compasses


class CompasLoop(Expression):
	def __init__(self, value, CompasList):
		self._value = value
		self._duration = CompasList.getDuration()

		for 

	def getRepeat(self):
		return self._value

	def getCompasses(self):
		return CompasList

	def getDuration(self):
		return self._duration

	def isLoop(self):
		return True



class Note(Expression):
	def __init__(self, notename, alter, value, shape, puntillo):
		#concatenacion de string
		self._height = notename+alter
		self._value = value
		self._duration = 0

		if shape == 'redonda':
			self._duration = 1
		if shape == 'blanca':
			self._duration = 1/2
		if shape == 'negra':
			self._duration = 1/4
		if shape == 'corchea':
			self._duration = 1/8
		if shape == 'semicorchea':
			self._duration = 1/16
		if shape == 'fusa':
			self._duration = 1/32
		if shape == 'semifusa':
			self._duration = 1/64
		if self._duration == 0:
			raise Exception("Figura no definida")

		if puntillo == ".":
			self._duration = self._duration*(3/2)
		if puntillo != None or puntillo != ".":
			raise Exception("Puntillo no definido")


	def getOctave(self):
		return self._value

	def getHeight(self):
		return self._height

	def getDuration(self):
		return self._duration
