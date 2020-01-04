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


class StateConfig() :

    def __init__(
        self,
        max_brightness = 120,
        active_visualizer_effect = "scroll",
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

        self.active_audio_channel_index = active_audio_channel_index

        self.active_shape_index = active_shape_index
        self.shapes = []
        for shape in shapes:
            self.shapes.append(ShapeConfig(shape))
        self.number_of_shapes = len(self.shapes)

        self.active_visualizer_effect = active_visualizer_effect
        self.max_brightness = max_brightness

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
        print("State Config : ")
        print("----------------")
        print("active_audio_channel_index -> ", self.active_audio_channel_index)
        print("max_brightness -> ", self.max_brightness)
        for shape in self.shapes:
            shape.print()
        print("active_shape_index -> ", self.active_shape_index)
        print("number_of_shapes -> ", self.number_of_shapes)
        print("active_visualizer_effect -> ", self.active_visualizer_effect)
        print("time_interval -> ", self.time_interval)
        print("chunk_size -> ", self.chunk_size)
        print("is_reverse -> ", self.is_reverse)
        print("is_mirror -> ", self.is_mirror)
        print("color_schemes -> ", self.color_schemes)
        print("active_color_scheme_index -> ", self.active_color_scheme_index)
        print("formatted_color_schemes -> ", self.formatted_color_schemes)
        print("----------------")
        print("--")

class StripConfig() :

    def __init__(
        self,
        name = "strip",
        serial_port_name = "/dev/tty.usbserial-14240",
        is_online= False,
        midi_ports_for_changing_mode = [],
        midi_ports_for_visualization = [],
        active_state_index = 0,
        physical_shape = [20,20],
        debug = False
    ):

        self.name = name
        self.serial_port_name = serial_port_name
        self.is_online = is_online
        self.midi_ports_for_changing_mode = midi_ports_for_changing_mode
        self.midi_ports_for_visualization = midi_ports_for_visualization
        self.physical_shape = ShapeConfig(physical_shape)
        self.active_state_index = active_state_index

        if(debug):
            SerialOutput.tryPort(serial_port_name)
            if(midi_ports_for_visualization):
                for name in midi_ports_for_visualization:
                    MidiInput.tryPort(name)
            if(midi_ports_for_changing_mode):
                for name in midi_ports_for_changing_mode:
                    MidiInput.tryPort(name)


    def print(self):
        print("--")
        print("----------------")
        print("Strip Config : ")
        print("----------------")
        print("name -> ", self.name)
        print("serial_port_name -> ", self.serial_port_name)
        print("midi_ports_for_changing_mode -> ", self.midi_ports_for_changing_mode)
        print("midi_ports_for_visualization -> ", self.midi_ports_for_visualization)
        print("physical_shape -> ", self.physical_shape)
        print("active_state_index -> ", self.active_state_index)
        print("----------------")
        print("--")

class Config():

    def __init__(
        self,
        desirated_framerate = 60,
        display_interface = True,
        debug = False,
        audio_ports = [
            {
                "name": "Built-in Microphone",
                "min_frequency": 200,
                "max_frequency": 12000,
            }
        ],
        strips = [
            {
                "name": "strip",
                "serial_port_name": "/dev/tty.usbserial-14210",
                "midi_ports_for_changing_mode": ["Ableton-virtual-midi-ouput ChangeModStripOne"],
                "midi_ports_for_visualization": ["Ableton-virtual-midi-ouput LeftSynth"],
                "active_state_index": 0,
                "physical_shape": [50,50]
            }
        ],
        states = [
            {
                "max_brightness": 120,
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

        self.desirated_framerate = desirated_framerate
        self.display_interface = display_interface
        self.delay_between_frames = 1 / desirated_framerate
        self.timeSinceStart = TimeSinceStart()
        self.audio_ports = []
        for audio_port in audio_ports:
            self.audio_ports.append(
                AudioPortConfig(
                    name = audio_port["name"],
                    min_frequency = audio_port["min_frequency"],
                    max_frequency = audio_port["max_frequency"],
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
                    midi_ports_for_changing_mode = strip["midi_ports_for_changing_mode"],
                    midi_ports_for_visualization = strip["midi_ports_for_visualization"],
                    physical_shape = strip["physical_shape"],
                    debug = debug
                )
            )
        self.number_of_strips = len(self.strips)
        self.states = []
        for state in states :
            self.states.append(
                StateConfig(
                    active_audio_channel_index = state["active_audio_channel_index"],
                    max_brightness = state["max_brightness"],
                    active_visualizer_effect = state["active_visualizer_effect"],
                    shapes = state["shapes"],
                    active_shape_index = state["active_shape_index"],
                    color_schemes = state["color_schemes"],
                    active_color_scheme_index = state["active_color_scheme_index"],
                    time_interval = state["time_interval"],
                    chunk_size = state["chunk_size"],
                    is_mirror = state["is_mirror"],
                    is_reverse = state["is_reverse"],
                    debug = debug
                )
            )
        self.number_of_states = len(self.states)


    def getJsonFromConfig(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)

    def print(self):
        print("--")
        print("----------------")
        print("Config : ")
        print("----------------")
        print("desirated_framerate -> ", self.desirated_framerate)
        print("display_interface -> ", self.display_interface)
        print("delay_between_frames -> ", self.delay_between_frames)
        for audio_port in self.audio_ports:
            audio_port.print()
        print("number_of_audio_ports -> ", self.number_of_audio_ports)
        for strip in self.strips:
            strip.print()
        print("number_of_strips -> ", self.number_of_strips)
        for state in self.states:
            state.print()
        print("number_of_states -> ", self.number_of_states)
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
                    desirated_framerate = file["desirated_framerate"],
                    display_interface = file["display_interface"],
                    audio_ports = file["audio_ports"],
                    strips = file["strips"],
                    states = file["states"],
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
    def testConfig(path=os.path.abspath(os.path.dirname(sys.argv[0])) + '/../NEW_CONFIG.yml', verbose=False):

        ConfigLoader.testFilePath(path)
        config = ConfigLoader(path, debug=False)
        if(verbose):
            config.data.print()

        print("Congrats, your config file is valid !")


if __name__ == "__main__":

    config = ConfigLoader.testConfig(verbose=True)
    # method_list = [func for func in dir(Visualizer) if callable(getattr(Visualizer, func)) and not func.startswith("__")]
    # print(method_list)
