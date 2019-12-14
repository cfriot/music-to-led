import time, pyaudio
import numpy as np

class AudioInput:
    def __init__(self, port_name, min_frequency=200, max_frequency=12000):
        """ Create a data stream from audio input """
        self.audio = pyaudio.PyAudio()
        self.rate = 44100
        self.fps = 60
        self.overflows = 0
        self.data = []
        self.stream = 0
        self.prev_overflow_time = time.time()
        self.frames_per_buffer = int(self.rate / self.fps)
        self.port_index = AudioInput.getPortIndexFromName(port_name)
        self.tryPort(port_name)
        self.stream = self.audio.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.rate,
            input = True,
            input_device_index = self.port_index,
            frames_per_buffer = self.frames_per_buffer
        )

    @staticmethod
    def tryPort(port_name):
        if(AudioInput.getPortIndexFromName(port_name) == -1):
            print("Audio port not found or not acceptable, please check your config file -> ", port_name)
            list = []
            for item in AudioInput.listAvailablePortsInfos():
                if(item["maxInputChannels"] >= 2):
                    list.append(item["name"])
            print("Here's the audio ports available ->", list)
            quit()

    @staticmethod
    def listAvailablePortsInfos():
        """ List available ports informations """
        audio = pyaudio.PyAudio()
        ports = []
        for i in range(audio.get_device_count()):
            ports.append(audio.get_device_info_by_index(i))
        return ports

    @staticmethod
    def getPortIndexFromName(name):
        """ Get port index from name

            input: Port's name
            returns: Index
        """
        audio = pyaudio.PyAudio()
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            if(name == info["name"]):
                return info["index"]
        return -1

    @staticmethod
    def listAvailablePortsName():
        """List available ports names"""
        audio = pyaudio.PyAudio()
        ports = []
        for i in range(audio.get_device_count()):
            if(audio.get_device_info_by_index(i)["maxInputChannels"] >= 1):
                ports.append({"name": audio.get_device_info_by_index(
                    i)["name"], "index": audio.get_device_info_by_index(i)["index"]})
        return ports

    def getRawData(self):
        """Return actual audio data"""
        try:
            self.data = np.fromstring(
                self.stream.read(
                    self.frames_per_buffer,
                    exception_on_overflow = False
                ),
                dtype = np.int16
            )
            self.data = self.data.astype(np.float32)
            self.stream.read(
                self.stream.get_read_available(),
                exception_on_overflow = False
            )
            return self.data
        except IOError:
            overflows += 1
            if time.time() > prev_overflow_time + 1:
                prev_overflow_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))

    def __del__(self):
        if(self.stream != 0):
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="list available audio devices", action="store_true")
    parser.add_argument("-t", "--test", help="test a given audio port", type=str)

    args = parser.parse_args()

    if(args.list):
        print('Audio ports available :')
        for port in AudioInput.listAvailablePortsName():
            print("- " + port["name"])

    if(args.test):
        if(AudioInput.getPortIndexFromName(args.test) != -1):
            print('Audio tests test on port :')
            print(args.test)
            audioInput = AudioInput(args.test)
            import time
            while 1:
                data = audioInput.getRawData()
                print(data)
                print(len(data))
                time.sleep(1)
        else:
            print('This port is not available ->' + args.test)
