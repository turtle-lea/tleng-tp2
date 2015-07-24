from clasesber import  *
from clasesmata import  *
from clasesleanv import  *
__author__ = 'bernapanarello'
class MidiTranslator:
    def generateMIDIFile(self, root):


        strFormatHeader1 = "MFile 1 {0} 384"
        strFormatHeader2 = "000:00:000 TimeSig {0}/{1} 24 8"
        strFormatHeader3 = "000:00:000 Tempo {0}"
        strFormatHeader4 = "000:00:000 Meta TrkEnd"
        strFormatHeader5 = "TrkEnd"


        strFormatVoyHeader1 = 'MTrk'
        strFormatVoyHeader2 = '000:00:000 Meta TrkName "Voz {0}"'
        strFormatVoyHeader3 = '000:00:000 ProgCh ch={0} prog={1}'


        strFormatVoyHeader4 = '{0:03d}:{1:02d}:{2:03d} Meta TrkEnd'
        strFormatVoyHeader5 = "TrkEnd"


        self.writeMidi(strFormatHeader1.format(len(root.getVoiceList().getList()) + 1))
        self.writeMidi(strFormatHeader2.format(root.getCompasHeader().getNumerator(), root.getCompasHeader().getDenominator()))
        self.writeMidi(strFormatHeader3.format(self.calculateTempo(root.getTempo())))
        self.writeMidi(strFormatHeader4)
        self.writeMidi(strFormatHeader5)

        vlist = root.getVoiceList().getList()

        for i in range(0, len(vlist)):
            #Encabezado de la Voz
            v = vlist[i]
            channel = i + 1
            self.writeMidi(strFormatVoyHeader1)
            self.writeMidi(strFormatVoyHeader2.format(channel))
            self.writeMidi(strFormatVoyHeader3.format(channel, v.getInstrument()))
            compasId = 0
            vc = v.getCompasses()
            for j in range(0, len(vc)):
                content = vc[j]

                if content.isLoop():
                    repeat = content.getRepeat()
                    contentList = content.getCompasses()
                else:
                    repeat = 1
                    contentList = [content]

                for k in range(0, repeat):
                    for c in contentList:
                        self.writeCompass(c, root, compasId, channel)
                        compasId = compasId + 1

            self.writeMidi(strFormatVoyHeader5)

            self.writeMidi(strFormatVoyHeader5)



    def writeMidi(self, line):
        print(line)

    def writeCompass(self, compass, root, compassId, channel):

        strFormatVoyNoteOn = '{0:03d}:{1:02d}:{2:03d} On ch={3} note={4}{5} vol=70'
        strFormatVoyNoteOff = '{0:03d}:{1:02d}:{2:03d} Off ch={3} note={4}{5} vol=0'

        clickOffset = 0
        pulseOffset = 0
        for n in compass.getNoteList():
            clicks = int(n.getDuration() * root.getCompasHeader().getDenominator() * 384)
            finalClick = (clicks + clickOffset) % 384
            finalPulse = (clicks + clickOffset) // 384

            #TODO : HAY QUE ARREGLAR EL TEMA DEL COMPAS SILENCIOSO (VER COMPAS 13 DEL EJ1)
            if not n.isSilence():
                noteName = self.fromLatinToAmerican(n.getHeight())
                octave = n.getOctave()
                self.writeMidi(strFormatVoyNoteOn.format(compassId, pulseOffset, clickOffset, channel, noteName, octave))
                self.writeMidi(strFormatVoyNoteOff.format(compassId, finalPulse, finalClick, channel, noteName, octave))

            clickOffset = finalClick
            pulseOffset = finalPulse




    def calculateTempo(self, tempo):
        return int(1000000 * 60 / (tempo.getShapeDuration() * 4 * tempo.getCount()))

    def fromLatinToAmerican(self, noteName):
        #A: la
        #B: si
        #C: do
        #D: re
        #E: mi
        #F: fa
        #G: sol.

        return noteName.replace('la', 'A').replace('si','B').replace('do', 'C').replace('re', 'D').replace('mi', 'E').replace('fa', 'F').replace('sol', "G")