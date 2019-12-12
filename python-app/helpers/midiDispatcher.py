from inputs.midiInput import MidiInput

class MidiDispatcher() :
    def __init__(self, midi_ports_for_changing_mode, dedicated_midi_ports):
        self.midi_ports_for_changing_mode = midi_ports_for_changing_mode
        self.associated_midi_channels = dedicated_midi_ports
        self.midi_input_classes = []
        self.midi_datas = []
        self.midi_datas_for_visualization = []
        self.midi_datas_for_changing_mode = []

        if(self.midi_ports_for_changing_mode):
            for midi_port_for_changing_mode in self.midi_ports_for_changing_mode:
                self.midi_input_classes.append(MidiInput(midi_port_for_changing_mode))
        if(self.associated_midi_channels):
            for midi_port in self.associated_midi_channels:
                self.midi_input_classes.append(MidiInput(midi_port))

    def dispatch(self):
        self.midi_datas = []
        self.midi_datas_for_visualization = []
        self.midi_datas_for_changing_mode = []
        for i, midi_input_class in enumerate(self.midi_input_classes):
            self.midi_datas = self.midi_input_classes[i].getRawData()
            if(self.midi_datas):
                for midi_note in self.midi_datas:
                    for channel in self.midi_ports_for_changing_mode:
                        if(midi_note["port"] == channel):
                            self.midi_datas_for_changing_mode.append(midi_note)
                    for channel in self.associated_midi_channels:
                        if(midi_note["port"] == channel):
                            self.midi_datas_for_visualization.append(midi_note)
