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

        strFormatVoyNoteOn = '{0:03d}:{1:02d}:{2:02d} On ch={3} note={4} vol=70'
        strFormatVoyNoteOff = '{0:03d}:{1:02d}:{2:02d} Off ch={3} note={4} vol=0'

        strFormatVoyHeader4 = "TrkEnd"


        self.writeMidi(strFormatHeader1.format(len(root.getVoiceList().getList()) + 1))
        self.writeMidi(strFormatHeader2.format(root.getCompasHeader().getNumerator(), root.getCompasHeader().getDenominator()))
        self.writeMidi(strFormatHeader3.format(self.calculateTempo(root.getTempo())))
        self.writeMidi(strFormatHeader4)
        self.writeMidi(strFormatHeader5)

        vlist = root.getVoiceList().getList()

        for i in range(0, len(vlist) - 1):
            #Encabezado de la Voz
            v = vlist[i]
            self.writeMidi(strFormatVoyHeader1)
            self.writeMidi(strFormatVoyHeader2.format(i + 1))
            self.writeMidi(strFormatVoyHeader3.format(i + 1, v.getInstrument()))
            compasId = 0
            vc = v.getCompasses()
            for j in range(0, len(vc) - 1):
                content = vc[i]

                if content.isLoop():
                    repeat = content.getRepeat()
                    contentList = content.getCompasses()
                else:
                    repeat = 1
                    contentList = [content]

                for k in range(1, repeat):
                    for c in contentList:
                        writeCompass(c)

            self.writeMidi(strFormatVoyHeader4)



    def writeMidi(self, line):
        pass

    def writeCompass(self, compass):
        


