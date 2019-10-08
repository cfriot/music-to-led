import yaml

from helpers.time.timeSinceStart import TimeSinceStart
from helpers.color.colorSchemeFormatter import ColorSchemeFormatter

from visualizations.visualizer import Visualizer

class AudioPortSettings() :

    def __init__(
        self,
        name = "Built-in Microphone",
        min_frequency = 200,
        max_frequency = 12000,
        sampling_rate = 44000,
        number_of_audio_samples = 24,
        min_volume_threshold = 1e-7
    ):

        self.name = name
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.sampling_rate = sampling_rate
        self.number_of_audio_samples = number_of_audio_samples
        self.min_volume_threshold = min_volume_threshold

    def print(self):
        print("--")
        print("----------------")
        print("Audio Port Settings : ")
        print("----------------")
        print("name -> ", self.name)
        print("min_frequency -> ", self.min_frequency)
        print("max_frequency -> ", self.max_frequency)
        print("sampling_rate -> ", self.sampling_rate)
        print("number_of_audio_samples -> ", self.number_of_audio_samples)
        print("min_volume_threshold -> ", self.min_volume_threshold)
        print("----------------")
        print("--")


class ShapeSettings() :

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
        print("Shape Settings : ")
        print("----------------")
        print("shape -> ", self.shape)
        print("number_of_substrip -> ", self.number_of_substrip)
        print("number_of_pixels -> ", self.number_of_pixels)
        print("----------------")
        print("--")


class StripSettings() :

    def __init__(
        self,
        serial_port_name = "/dev/tty.usbserial-14240",
        associated_midi_channels = ["Ableton-virtual-midi-ouput LeftSynth"],
        active_visualizer_effect = "scroll",
        shapes = [[26,26],[12,12]],
        active_audio_channel_index = 0,
        active_shape_index = 0,
        is_reverse = False,
        is_mirror = False,
        active_color_scheme_index = 0,
        color_schemes = [["#FF0000", "#00FF00"]]
    ):

        self.serial_port_name = serial_port_name
        self.associated_midi_channels = associated_midi_channels
        self.active_audio_channel_index = active_audio_channel_index

        self.active_shape_index = active_shape_index
        self.shapes = []
        for shape in shapes:
            self.shapes.append(ShapeSettings(shape))
        self.number_of_shapes = len(self.shapes)

        self.active_visualizer_effect = active_visualizer_effect
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
        print("Strip Settings : ")
        print("----------------")
        print("serial_port_name -> ", self.serial_port_name)
        print("associated_midi_channels -> ", self.associated_midi_channels)
        print("active_audio_channel_index -> ", self.active_audio_channel_index)
        print("active_shape_index -> ", self.active_shape_index)
        for shape in self.shapes:
            shape.print()
        print("number_of_shapes -> ", self.number_of_shapes)
        print("active_visualizer_effect -> ", self.active_visualizer_effect)
        print("is_reverse -> ", self.is_reverse)
        print("is_mirror -> ", self.is_mirror)
        print("active_color_scheme_index -> ", self.active_color_scheme_index)
        print("color_schemes -> ", self.color_schemes)
        print("formatted_color_schemes -> ", self.formatted_color_schemes)
        print("----------------")
        print("--")


class Settings():

    def __init__(
        self,
        fps = 60,
        number_of_audio_samples = 24,
        n_rolling_history = 4,
        audio_ports = [
            {
                "name": "Built-in Microphone",
                "min_frequency": 200,
                "max_frequency": 12000,
                "min_volume_threshold": 1e-7
            }
        ],
        midi_port_for_changing_mode = "Ableton-virtual-midi-ouput ChangeMod",
        strips = [
            {
                "serial_port_name": "/dev/tty.usbserial-14210",
                "associated_midi_channels": ["Ableton-virtual-midi-ouput LeftSynth"],
                "active_visualizer_effect": "scroll",
                "shapes": [[26,26],[12,12]],
                "active_audio_channel_index": 0,
                "active_shape_index": 0
            }
        ]
    ):

        self.fps = fps
        self.timeSinceStart = TimeSinceStart()
        self.n_rolling_history = n_rolling_history
        self.number_of_audio_samples = number_of_audio_samples
        self.audio_ports = []
        for audio_port in audio_ports:
            self.audio_ports.append(
                AudioPortSettings(
                    name = audio_port["name"],
                    min_frequency = audio_port["min_frequency"],
                    max_frequency = audio_port["max_frequency"],
                    sampling_rate = audio_port["sampling_rate"],
                    number_of_audio_samples = audio_port["number_of_audio_samples"],
                    min_volume_threshold = audio_port["min_volume_threshold"]
                )
            )
        self.number_of_audio_ports = len(self.audio_ports)
        self.midi_port_for_changing_mode = "Ableton-virtual-midi-ouput ChangeMod"
        self.strips = []
        for strip in strips :
            self.strips.append(
                StripSettings(
                    serial_port_name = strip["serial_port_name"],
                    associated_midi_channels = strip["associated_midi_channels"],
                    active_visualizer_effect = strip["active_visualizer_effect"],
                    shapes = strip["shapes"],
                    active_audio_channel_index = strip["active_audio_channel_index"],
                    active_shape_index = strip["active_shape_index"],
                    active_color_scheme_index = strip["active_color_scheme_index"],
                    color_schemes = strip["color_schemes"]
                )
            )
        self.number_of_strips = len(self.strips)


    def print(self):
        print("--")
        print("----------------")
        print("Settings : ")
        print("----------------")
        print("fps -> ", self.fps)
        print("n_rolling_history -> ", self.n_rolling_history)
        for audio_port in self.audio_ports:
            audio_port.print()
        print("number_of_audio_ports -> ", self.number_of_audio_ports)
        print("midi_port_for_changing_mode -> ", self.midi_port_for_changing_mode)
        for strip in self.strips:
            strip.print()
        print("number_of_strips -> ", self.number_of_strips)
        print("----------------")
        print("--")


class SettingsLoader():
    """ Load and instanciate settings class from settings file """
    def __init__(self, file):
        with open(file, 'r') as stream:
            try:
                file = yaml.load(
                    stream,
                    Loader = yaml.FullLoader
                )

                self.data = Settings(
                    fps = file["fps"],
                    n_rolling_history = file["n_rolling_history"],
                    audio_ports = file["audio_ports"],
                    midi_port_for_changing_mode = file["midi_port_for_changing_mode"],
                    strips = file["strips"]
                )

            except yaml.YAMLError as exc:
                print(exc)


if __name__ == "__main__":

    print('Starting SettingsLoader test on ports :')

    config = SettingsLoader("settings/settings_file.yml")
    config.data.print()

    # method_list = [func for func in dir(Visualizer) if callable(getattr(Visualizer, func)) and not func.startswith("__")]
    # print(method_list)


    print("YAML VALID")
