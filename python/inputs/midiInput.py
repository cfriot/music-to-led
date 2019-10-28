import time
import numpy as np
import pyaudio
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
    def tryPort(port_name):
        try :
            port = mido.open_input(port_name)
            port.close()
        except IOError:
            print("Midi port not found, please check your config file -> ", port_name)
            quit()

    @staticmethod
    def listAvailablePortsName():
        """ List avaiable ports names """
        return mido.get_output_names()

    def getRawData(self):
        """ Return actual midi data """
        self.notes = []
        for msg in self.port.iter_pending():
            if(hasattr(msg, 'type') and (msg.type == "pitchwheel") and msg.pitch):
                self.notes.append({"port": self.port_name, "type": msg.type, "pitch": msg.pitch})
            if(hasattr(msg, 'type') and (msg.type == "control_change") and msg.control):
                self.notes.append({"port": self.port_name, "type": msg.type, "control": msg.control})
            if(hasattr(msg, 'note') and hasattr(msg, 'type') and (msg.type == "note_on" or msg.type == "note_off") and msg.velocity):
                self.notes.append(
                    {"port": self.port_name, "type": msg.type, "note": msg.note, "velocity": msg.velocity})
        return self.notes

    def __del__(self):
        if(self.port != 0):
            self.port.close()


if __name__ == "__main__":

    print('Starting MidiInput test on ports :')
    ports = MidiInput.listAvailablePortsName()
    ports = ['Ableton-virtual-midi-ouput LeftSynth']
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
