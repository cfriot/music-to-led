import time
import numpy as np
import pyaudio

import mido
import mido.backends.rtmidi

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
            print("Midi port not available -> ", port_name)
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
            if(hasattr(msg, 'type') and (msg.type == "control_change") and msg.value and msg.control):
                self.notes.append({"port": self.port_name, "type": msg.type, "value": msg.value, "control": msg.control})
            if(hasattr(msg, 'note') and hasattr(msg, 'type') and (msg.type == "note_on" or msg.type == "note_off") and hasattr(msg, 'velocity')):
                self.notes.append(
                    {"port": self.port_name, "type": msg.type, "note": msg.note, "velocity": msg.velocity})
        return self.notes

    def __del__(self):
        if(self.port != 0):
            self.port.close()




if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="list available midi devices", action="store_true")
    parser.add_argument("-t", "--test", help="test a given midi port", type=str)

    args = parser.parse_args()

    if(args.list):
        print('Midi ports available :')
        ports = MidiInput.listAvailablePortsName()
        for port in ports:
            print("- " + port)

    if(args.test):

        MidiInput.tryPort(args.test)
        print('Midi tests test on port :')
        print(args.test)

        midiClass = MidiInput(args.test)

        while 1:
            notes = []

            notes = midiClass.getRawData()

            if(notes != []):
                print(notes)
