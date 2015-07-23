from clasesber import  *
from clasesmata import  *
from clasesleanv import  *
__author__ = 'bernapanarello'
class MidiTranslator:
    def generateMIDIFile(self, root):


        strFormatHeader1 = "MFile 1 {0} 384"
        strFormatHeader2 = "000:00:000 TimeSig {0} 24 8"
        strFormatHeader3 = "000:00:000 Tempo {0}"
        strFormatHeader4 = "000:00:000 Meta TrkEnd"
        strFormatHeader5 = "TrkEnd"


        strFormatVoyHeader1 = 'MTrk'
        strFormatVoyHeader2 = '000:00:000 Meta TrkName "{0}"'
        strFormatVoyHeader3 = '000:00:000 ProgCh ch={0} prog={1}'
        strFormatVoyHeader4 = '000:00:000 On ch=1 note=c5 vol=70'
        strFormatVoyHeader5 = "TrkEnd"

        strFormatVoyNoteOn = '{0:000}:{1}:{2} On ch={3} note={4} vol=70'
        strFormatVoyNoteOff = '{0}:{1}:{2} Off ch={3} note={4} vol=0'



