#!/usr/bin/python
# -*- coding: latin-1 -*-
from clasesber import  *
from clasesmata import  *
from clasesleanv import  *
__author__ = 'bernapanarello'
class MidiTranslator:
    def generateMIDIFile(self, root):

        strFormatHeader0 = "MFile 1 {0} 384"
        strFormatHeader1 = "MTrk"
        strFormatHeader2 = "000:00:000 Tempo {0}"
        strFormatHeader3 = "000:00:000 TimeSig {0}/{1} 24 8"
        strFormatHeader4 = "000:00:000 Meta TrkEnd"
        strFormatHeader5 = "TrkEnd"


        strFormatVoyHeader1 = 'MTrk'
        strFormatVoyHeader2 = '000:00:000 Meta TrkName "Voz {0}"'
        strFormatVoyHeader3 = '000:00:000 ProgCh ch={0} prog={1}'


        strFormatVoyHeader4 = '{0:03d}:{1:02d}:{2:03d} Meta TrkEnd'
        strFormatVoyHeader5 = "TrkEnd"

        self.writeMidi(strFormatHeader0.format(len(root.getVoiceList().getList()) + 1))
        self.writeMidi(strFormatHeader1)
        self.writeMidi(strFormatHeader2.format(self.calculateTempo(root.getTempo())))
        self.writeMidi(strFormatHeader3.format(root.getCompasHeader().getNumerator(), root.getCompasHeader().getDenominator()))
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
                    contentList = content.getCompasses().getList()
                else:
                    repeat = 1
                    contentList = [content]

                for k in range(0, repeat):
                    for c in contentList:
                        self.writeCompass(c, root, compasId, channel)
                        compasId = compasId + 1

            self.writeMidi(strFormatVoyHeader4.format(compasId, 0, 0))

            self.writeMidi(strFormatVoyHeader5)



    def writeMidi(self, line):
        print(line)

    def writeCompass(self, compass, root, compassId, channel):

        strFormatVoyNoteOn = '{0:03d}:{1:02d}:{2:03d} On ch={3} note={4}{5} vol=70'
        strFormatVoyNoteOff = '{0:03d}:{1:02d}:{2:03d} Off ch={3} note={4}{5} vol=0'

        clickOffset = 0
        pulseOffset = 0
        nList = compass.getNoteList()
        for i in range (0, len(nList)):
            n = nList[i]
            clicks = int(n.getDuration() * root.getCompasHeader().getDenominator() * 384)
            finalClick = (clicks + clickOffset) % 384

            finalPulse = pulseOffset + (clicks + clickOffset) // 384


            if not n.isSilence():
                noteName = self.fromLatinToAmerican(n.getHeight())
                octave = n.getOctave()
                self.writeMidi(strFormatVoyNoteOn.format(compassId, pulseOffset, clickOffset, channel, noteName, octave))

                #Imprimo la nota en el archivo. Si la nota es la última del compás, entonces imprimo el Off al comienzo del próximo compas
                if i < len(nList) - 1:

                    self.writeMidi(strFormatVoyNoteOff.format(compassId, finalPulse, finalClick, channel, noteName, octave))
                else:
                    self.writeMidi(strFormatVoyNoteOff.format(compassId + 1, 0, 0, channel, noteName, octave))


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

        return noteName.replace('la', 'a').replace('si','b').replace('do', 'c').replace('re', 'd').replace('mi', 'e').replace('fa', 'f').replace('sol', "g")