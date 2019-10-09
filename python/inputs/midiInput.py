import time
import numpy as np
import pyaudio
import rtmidi
import mido
from mido.ports import MultiPort

class MidiInput:
    def __init__(self, port_name):
        """ Create a data stream from midi input """
        self.notes = []
        self.port = 0
        self.port_name = port_name
        self.port = mido.open_input(self.port_name)

    @staticmethod
    def listAvailablePortsName():
        """ List avaiable ports names """
        return mido.get_output_names()

    def getRawData(self):
        global toto
        """ Return actual midi data """
        self.notes = []
        for msg in self.port.iter_pending():
            if(hasattr(msg, 'note') and hasattr(msg, 'type') and (msg.type == "note_on" or msg.type == "note_off") and msg.velocity):
                self.notes.append(
                    {"port": self.port_name, "type": msg.type, "note": msg.note, "velocity": msg.velocity})
        return self.notes

    def __del__(self):
        self.port.close()


if __name__ == "__main__":

    print('Starting MidiInput test on ports :')
    ports = MidiInput.listAvailablePortsName()
    midiClasses = []
    print(ports)
    for port in ports :
        midiClasses.append(MidiInput(port))

    while 1:
        notes = []

        for midiClass in midiClasses :
            notes += midiClass.getRawData()

        if(notes != []):
            print(notes)
