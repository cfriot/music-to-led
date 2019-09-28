import time
import numpy as np
import pyaudio
import rtmidi


class AudioInput:
    def __init__(self, port_name):
        self.audio = pyaudio.PyAudio()
        self.rate = 44100
        self.fps = 60
        self.overflows = 0
        self.data = []
        self.prev_overflow_time = time.time()
        self.frames_per_buffer = int(self.rate / self.fps)
        self.port_index = AudioInput.getPortIndexFromName(port_name)
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            input_device_index=self.port_index,
            frames_per_buffer=self.frames_per_buffer
        )

    @staticmethod
    def listAvailablePortsInfos():
        audio = pyaudio.PyAudio()
        ports = []
        for i in range(audio.get_device_count()):
            print(audio.get_device_info_by_index(i)["name"])
            ports.append(audio.get_device_info_by_index(i))
        return ports

    @staticmethod
    def getPortIndexFromName(name):
        audio = pyaudio.PyAudio()
        for i in range(audio.get_device_count()):
            if(name == audio.get_device_info_by_index(i)["name"]):
                return audio.get_device_info_by_index(i)["index"]

    @staticmethod
    def listAvailablePortsName():
        audio = pyaudio.PyAudio()
        ports = []
        for i in range(audio.get_device_count()):
            print(audio.get_device_info_by_index(i)["name"])
            ports.append({"name": audio.get_device_info_by_index(
                i)["name"], "index": audio.get_device_info_by_index(i)["index"]})
        return ports

    def getRawData(self):
        """Return actual audio data"""
        try:
            self.data = np.fromstring(self.stream.read(
                self.frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            self.data = self.data.astype(np.float32)
            self.stream.read(self.stream.get_read_available(),
                             exception_on_overflow=False)
            return self.data
        except IOError:
            overflows += 1
            if time.time() > prev_overflow_time + 1:
                prev_overflow_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


if __name__ == "__main__":

    port_name = "Background Music"
    audioInput = AudioInput(port_name)

    print('Starting Audio tests test on ports :')
    print(audioInput.listAvailablePortsInfos())

    while True:
        print(audioInput.getRawData())
