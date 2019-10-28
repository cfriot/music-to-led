import numpy as np

from inputs.audioInput import AudioInput

from helpers.audio.audioProcessing import AudioProcessing

class AudioDispatcher():
    def __init__(self, audio_ports):
        self.audio_ports = audio_ports
        self.number_of_audio_ports = len(audio_ports)
        self.audio_datas = np.tile(0., (self.number_of_audio_ports, 24))
        self.audio_input_classes = []
        self.audio_processors = []
        for audio_port in self.audio_ports:
            self.audio_input_classes.append(AudioInput(audio_port.name, audio_port.min_frequency, audio_port.max_frequency))
            self.audio_processors.append(AudioProcessing())

    def dispatch(self):
        self.audio_datas = []
        for i in range(self.number_of_audio_ports):
            self.audio_datas.append(self.audio_processors[i].render(self.audio_input_classes[i].getRawData()))
