import yaml, json, sys, os
import numpy as np


from helpers.time.timeSinceStart import TimeSinceStart
from helpers.color.colorSchemeFormatter import ColorSchemeFormatter

from visualizations.visualizer import Visualizer

from inputs.midiInput import MidiInput
from inputs.audioInput import AudioInput

from outputs.serialOutput import SerialOutput

def isAnEvenArray(arr):
    for item in arr:
        if(item % 2 == 1):
            return False
    return True

class AudioPortConfig() :

    def __init__(
        self,
        name = "Built-in Microphone",
        min_frequency = 200,
        max_frequency = 12000,
        sampling_rate = 44000,
        number_of_audio_samples = 24,
        min_volume_threshold = 1e-7,
        n_rolling_history = 4,
        debug = False
    ):

        self.name = name
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.sampling_rate = sampling_rate
        self.number_of_audio_samples = number_of_audio_samples
        self.min_volume_threshold = float(min_volume_threshold)
        self.n_rolling_history = n_rolling_history

        if(debug):
            AudioInput.tryPort(name)

    def print(self):
        print("--")
        print("----------------")
        print("Audio Port Config : ")
        print("----------------")
        print("name -> ", self.name)
        print("min_frequency -> ", self.min_frequency)
        print("max_frequency -> ", self.max_frequency)
        print("sampling_rate -> ", self.sampling_rate)
        print("number_of_audio_samples -> ", self.number_of_audio_samples)
        print("min_volume_threshold -> ", self.min_volume_threshold)
        print("n_rolling_history -> ", self.n_rolling_history)
        print("----------------")
        print("--")


class ShapeConfig() :

    def __init__(
        self,
        shape = [74, 74, 125, 125]
    ):

        self.shape = shape
        self.number_of_substrip = len(self.shape)
        self.number_of_pixels = 0
        for pixel_number in self.shape:
            self.number_of_pixels += pixel_number

    def print(self):
        print("--")
        print("----------------")
        print("Shape Config : ")
        print("----------------")
        print("shape -> ", self.shape)
        print("number_of_substrip -> ", self.number_of_substrip)
        print("number_of_pixels -> ", self.number_of_pixels)
        print("----------------")
        print("--")


class StripConfig() :

    def __init__(
        self,
        name = "strip",
        serial_port_name = "/dev/tty.usbserial-14240",
        is_online= False,
        max_brightness = 120,
        midi_ports_for_changing_mode = [],
        associated_midi_channels = [],
        active_visualizer_effect = "scroll",
        active_visualizer_mode = 0,
        real_shape = [52],
        shapes = [[26,26],[12,12]],
        active_audio_channel_index = 0,
        active_shape_index = 0,
        is_reverse = False,
        time_interval = 120,
        chunk_size = 5,
        is_mirror = False,
        active_color_scheme_index = 0,
        color_schemes = [["#FF0000", "#00FF00"]],
        debug = False
    ):

        self.name = name
        self.serial_port_name = serial_port_name
        self.is_online = is_online
        self.max_brightness = max_brightness
        self.midi_ports_for_changing_mode = midi_ports_for_changing_mode
        self.associated_midi_channels = associated_midi_channels
        self.active_audio_channel_index = active_audio_channel_index

        real_shape_number_of_pixels = 0
        for pixel_number in real_shape:
            real_shape_number_of_pixels += pixel_number
        self.pixels = np.tile(0., (3, real_shape_number_of_pixels)).tolist()

        if(debug):
            SerialOutput.tryPort(serial_port_name)
            if(associated_midi_channels or midi_ports_for_changing_mode):
                for name in associated_midi_channels + midi_ports_for_changing_mode:
                    MidiInput.tryPort(name)

        self.active_shape_index = active_shape_index
        self.real_shape = real_shape
        self.shapes = []
        for shape in shapes:
            self.shapes.append(ShapeConfig(shape))
        self.number_of_shapes = len(self.shapes)

        self.active_visualizer_effect = active_visualizer_effect
        self.active_visualizer_mode = active_visualizer_mode

        self.time_interval = time_interval
        self.chunk_size = chunk_size

        self.is_reverse = is_reverse
        self.is_mirror = is_mirror

        self.active_color_scheme_index = active_color_scheme_index
        self.color_schemes = color_schemes
        self.number_of_color_schemes = len(color_schemes)

        self.formatted_color_schemes = []
        colorSchemeFormatter = ColorSchemeFormatter()
        for scheme in self.color_schemes:
            self.formatted_color_schemes.append(colorSchemeFormatter.render(scheme))

    def print(self):
        print("--")
        print("----------------")
        print("Strip Config : ")
        print("----------------")
        print("name -> ", self.name)
        print("serial_port_name -> ", self.serial_port_name)
        print("max_brightness -> ", self.max_brightness)
        print("midi_ports_for_changing_mode -> ", self.midi_ports_for_changing_mode)
        print("associated_midi_channels -> ", self.associated_midi_channels)
        print("active_audio_channel_index -> ", self.active_audio_channel_index)
        print("active_shape_index -> ", self.active_shape_index)
        print("real_shape -> ", self.real_shape)
        for shape in self.shapes:
            shape.print()
        print("number_of_shapes -> ", self.number_of_shapes)
        print("active_visualizer_effect -> ", self.active_visualizer_effect)
        print("active_visualizer_mode -> ", self.active_visualizer_mode)
        print("time_interval -> ", self.time_interval)
        print("chunk_size -> ", self.chunk_size)
        print("is_reverse -> ", self.is_reverse)
        print("is_mirror -> ", self.is_mirror)
        print("active_color_scheme_index -> ", self.active_color_scheme_index)
        print("color_schemes -> ", self.color_schemes)
        print("formatted_color_schemes -> ", self.formatted_color_schemes)
        print("----------------")
        print("--")


class Config():

    def __init__(
        self,
        fps = 60,
        number_of_audio_samples = 24,
        debug = False,
        audio_ports = [
            {
                "name": "Built-in Microphone",
                "min_frequency": 200,
                "max_frequency": 12000,
                "min_volume_threshold": 1e-7,
            }
        ],
        strips = [
            {
                "name": "strip",
                "serial_port_name": "/dev/tty.usbserial-14210",
                "max_brightness": 120,
                "midi_ports_for_changing_mode": ["Ableton-virtual-midi-ouput ChangeModStripOne"],
                "associated_midi_channels": ["Ableton-virtual-midi-ouput LeftSynth"],
                "active_visualizer_effect": "scroll",
                "active_visualizer_mode": 0,
                "shapes": [[26,26],[12,12]],
                "active_audio_channel_index": 0,
                "active_shape_index": 0,
                "is_reverse" : False,
                "time_interval" : 120,
                "chunk_size" : 5,
                "is_mirror" : False
            }
        ]
    ):

        self.fps = fps
        self.delay_between_frames = 1 / fps
        self.timeSinceStart = TimeSinceStart()
        self.number_of_audio_samples = number_of_audio_samples
        self.audio_ports = []
        for audio_port in audio_ports:
            self.audio_ports.append(
                AudioPortConfig(
                    name = audio_port["name"],
                    min_frequency = audio_port["min_frequency"],
                    max_frequency = audio_port["max_frequency"],
                    sampling_rate = audio_port["sampling_rate"],
                    number_of_audio_samples = audio_port["number_of_audio_samples"],
                    min_volume_threshold = audio_port["min_volume_threshold"],
                    debug = debug
                )
            )
        self.number_of_audio_ports = len(self.audio_ports)
        self.strips = []
        for strip in strips :
            self.strips.append(
                StripConfig(
                    name = strip["name"],
                    serial_port_name = strip["serial_port_name"],
                    is_online = False,
                    max_brightness = strip["max_brightness"],
                    midi_ports_for_changing_mode = strip["midi_ports_for_changing_mode"],
                    associated_midi_channels = strip["associated_midi_channels"],
                    active_visualizer_effect = strip["active_visualizer_effect"],
                    active_visualizer_mode = strip["active_visualizer_mode"],
                    real_shape = strip["real_shape"],
                    shapes = strip["shapes"],
                    active_audio_channel_index = strip["active_audio_channel_index"],
                    active_shape_index = strip["active_shape_index"],
                    active_color_scheme_index = strip["active_color_scheme_index"],
                    color_schemes = strip["color_schemes"],
                    time_interval = strip["time_interval"],
                    chunk_size = strip["chunk_size"],
                    is_mirror = strip["is_mirror"],
                    is_reverse = strip["is_reverse"],
                    debug = debug
                )
            )
        self.number_of_strips = len(self.strips)

    def getJsonFromConfig(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)

    def print(self):
        print("--")
        print("----------------")
        print("Config : ")
        print("----------------")
        print("fps -> ", self.fps)
        print("delay_between_frames -> ", self.delay_between_frames)
        for audio_port in self.audio_ports:
            audio_port.print()
        print("number_of_audio_ports -> ", self.number_of_audio_ports)
        for strip in self.strips:
            strip.print()
        print("number_of_strips -> ", self.number_of_strips)
        print("----------------")
        print("--")


class ConfigLoader():
    """ Load and instanciate settings class from settings file """
    def __init__(self, file, debug=False):
        ConfigLoader.testFilePath(file)
        with open(file, 'r') as stream:
            try:

                file = yaml.load(
                    stream,
                    Loader = yaml.FullLoader
                )

                self.data = Config(
                    fps = file["fps"],
                    audio_ports = file["audio_ports"],
                    strips = file["strips"],
                    debug = debug
                )

            except yaml.YAMLError as exc:
                print(exc)

    def findStripIndexByStripName(self, name):
        for i, strip in enumerate(self.data.strips):
            if(name == strip.name):
                return i
        return -1

    @staticmethod
    def testFilePath(path):
        try:
            open(path)
        except IOError:
            print("Cannot load this config file. Please check your path.")
            quit()


    @staticmethod
    def testConfig(path=os.path.abspath(os.path.dirname(sys.argv[0])) + '/../CONFIG.yml', verbose=False):

        ConfigLoader.testFilePath(path)
        config = ConfigLoader(path, debug=True)
        if(verbose):
            config.data.print()

        print("Congrats, your config file is valid !")


if __name__ == "__main__":

    config = ConfigLoader.testConfig(verbose=False)
    # method_list = [func for func in dir(Visualizer) if callable(getattr(Visualizer, func)) and not func.startswith("__")]
    # print(method_list)
