import time
import numpy as np
import pyaudio
import rtmidi
import mido
from mido.ports import MultiPort


class MidiInput:
    def __init__(self, port_name):
        self.notes = []
        self.port = 0
        self.port_name = port_name
        self.port = mido.open_input(self.port_name)

    @staticmethod
    def listAvailablePortsName():
        return mido.get_output_names()

    def getRawData(self):
        """Return actual midi data"""
        self.notes = []
        for msg in self.port.iter_pending():
            if(hasattr(msg, 'note') and hasattr(msg, 'type') and msg.type == "note_on" and msg.velocity):
                self.notes.append(
                    {"port": self.port_name, "note": msg.note - 36, "velocity": msg.velocity})
        return self.notes

    def __del__(self):
        self.port.close()


if __name__ == "__main__":

    print(MidiInput.listAvailablePortsName())

    port_name = "Ableton-virtual-midi-ouput ChangeMod"
    midiInput = MidiInput(port_name)

    while True:
        notes = midiInput.getRawData()
        if(notes != []):
            print(notes)
