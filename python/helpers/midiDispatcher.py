from inputs.midiInput import MidiInput

class MidiDispatcher() :
    def __init__(self, midi_port_for_changing_mode, dedicated_midi_ports):
        self.midi_port_for_changing_mode = midi_port_for_changing_mode
        self.associated_midi_channels = dedicated_midi_ports
        self.midi_input_classes = []
        self.midi_datas = []
        self.midi_datas_for_visualization = []
        self.midi_datas_for_changing_mode = []

        self.midi_input_classes.append(MidiInput(midi_port_for_changing_mode))
        for midi_port in dedicated_midi_ports:
            self.midi_input_classes.append(MidiInput(midi_port))

    def dispatch(self):
        self.midi_datas = []
        self.midi_datas_for_visualization = []
        self.midi_datas_for_changing_mode = []
        for i, midi_input_class in enumerate(self.midi_input_classes):
            self.midi_datas = self.midi_input_classes[i].getRawData()
            if(self.midi_datas):
                for midi_note in self.midi_datas:
                    if(midi_note["port"] == self.midi_port_for_changing_mode):
                        self.midi_datas_for_changing_mode.append(midi_note)
                    else :
                        for channel in self.associated_midi_channels:
                            if(midi_note["port"] == channel):
                                self.midi_datas_for_visualization.append(midi_note)
