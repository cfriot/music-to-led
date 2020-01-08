import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

from visualizations.pixelReshaper import PixelReshaper

from helpers.audio.expFilter import ExpFilter

from visualizations.functions.sound.scroll import Scroll
from visualizations.functions.sound.energy import Energy
from visualizations.functions.sound.channelIntensity import ChannelIntensity
from visualizations.functions.sound.channelFlash import ChannelFlash

from visualizations.functions.midi.pianoNote import PianoNote
from visualizations.functions.midi.pianoScroll import PianoScroll
from visualizations.functions.midi.pitchwheelFlash import PitchwheelFlash

from visualizations.functions.time.alternateColors import AlternateColors
from visualizations.functions.time.drawLine import DrawLine

from visualizations.functions.generic.full import Full
from visualizations.functions.generic.fire import Fire

from scipy.ndimage.filters import gaussian_filter1d

def clampToNewRange(value, old_min, old_max, new_min, new_max):
    new_value = (((value - old_min) * (new_max - new_min)) // (old_max - old_min)) + new_min
    return new_value

class Visualizer(Full, AlternateColors, DrawLine, Scroll, ChannelIntensity, ChannelFlash, Energy, PianoNote, PianoScroll, Fire, PitchwheelFlash):

    def __init__(self, config, index):
        """ The main class that contain all viz functions """

        self.config = config
        self.strip_config = config.strips[index]
        self.strip_index = index
        self.active_state_index = config.strips[index].active_state_index
        self.active_state = config.states[self.active_state_index]

        self.number_of_audio_samples = config.audio_ports[config.states[self.active_state_index].active_audio_channel_index].number_of_audio_samples
        self.timeSinceStart = config.timeSinceStart
        self.time_interval_ms_interval = self.timeSinceStart.getMsIntervalFromBpm(self.active_state.time_interval)

        self.initVizualiser()
        self.resetFrame()

        self.audio_datas = []
        self.audio_data = []
        self.midi_datas = []

        self.pixelReshaper = PixelReshaper(self.active_state)

    def initVizualiser(self):

        self.number_of_pixels = self.active_state.shapes[self.active_state.active_shape_index].number_of_pixels
        self.active_state_index = self.config.strips[self.strip_index].active_state_index
        self.active_state = self.config.states[self.active_state_index]

        self.gain = ExpFilter(
            np.tile(0.01, self.number_of_audio_samples),
            alpha_decay = 0.001,
            alpha_rise=0.99
        )

        self.initEnergy()
        self.initChannelIntensity()
        self.initChannelFlash()

        self.initPianoNote()
        self.initPianoScroll()
        self.initPitchwheelFlash()

        self.initAlternateColors()

        self.initFull()
        self.initFire()

    @staticmethod
    def lerp(start, end, d):
        return start * (1 - d) + end * d

    def resetFrame(self):
        """ Reset current pixels """
        self.pixels = np.tile(0., (3, self.number_of_pixels))

    def blurFrame(self, pixels, value=1.0):
        pixels[0, :] = gaussian_filter1d(pixels[0, :], sigma=value)
        pixels[1, :] = gaussian_filter1d(pixels[1, :], sigma=value)
        pixels[2, :] = gaussian_filter1d(pixels[2, :], sigma=value)
        return pixels

    def applyMaxBrightness(self, pixels, max_brightness):
        tmp = [[],[],[]]
        for i in range(3):
            for y in range(len(pixels[0])):
                tmp[i].append(clampToNewRange(pixels[i][y], 0, 255, 0, max_brightness))
            tmp[i] = np.array(tmp[i])
        return tmp

    def drawFrame(self):
        """ Return current pixels """
        self.audio_data = self.audio_datas[self.active_state.active_audio_channel_index]

        pixels = []

        # SOUND BASED
        if(self.active_state.active_visualizer_effect == "scroll"):
            pixels = self.visualizeScroll()
        if(self.active_state.active_visualizer_effect == "energy"):
            pixels = self.visualizeEnergy()
        if(self.active_state.active_visualizer_effect == "channel_intensity"):
            pixels = self.visualizeChannelIntensity()
        if(self.active_state.active_visualizer_effect == "channel_flash"):
            pixels = self.visualizeChannelFlash()

        # MIDI BASED
        if(self.active_state.active_visualizer_effect == "piano_scroll"):
            pixels = self.visualizePianoScroll()
        if(self.active_state.active_visualizer_effect == "piano_note"):
            pixels = self.visualizePianoNote()
        if(self.active_state.active_visualizer_effect == "pitchwheel_flash"):
            pixels = self.visualizePitchwheelFlash()

        # TIME BASED
        if(self.active_state.active_visualizer_effect == "alternate_color_chunks"):
            pixels = self.visualizeAlternateColorChunks()
        if(self.active_state.active_visualizer_effect == "alternate_color_shapes"):
            pixels = self.visualizeAlternateColorShapes()
        if(self.active_state.active_visualizer_effect == "draw_line"):
            pixels = self.visualizeDrawLine()

        # GENERIC
        if(self.active_state.active_visualizer_effect == "full"):
            pixels = self.visualizeFull()
        if(self.active_state.active_visualizer_effect == "fade_to_black"):
            pixels = self.VisualizeFadeToBlack()
        if(self.active_state.active_visualizer_effect == "clear_frame"):
            pixels = self.visualizeClear()
        if(self.active_state.active_visualizer_effect == "fire"):
            pixels = self.visualizeFire()

        return pixels
