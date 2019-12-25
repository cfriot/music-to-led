import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

from visualizations.pixelReshaper import PixelReshaper

from helpers.audio.expFilter import ExpFilter

from visualizations.functions.sound.scroll import Scroll
from visualizations.functions.sound.energy import Energy
from visualizations.functions.sound.spectrum import Spectrum
from visualizations.functions.sound.intensityChannels import IntensityChannels

from visualizations.functions.midi.piano import Piano
from visualizations.functions.midi.piano2 import Piano2
from visualizations.functions.midi.envelope import Envelope

from visualizations.functions.time.alternateColors import AlternateColors
from visualizations.functions.time.drawLine import DrawLine
from visualizations.functions.time.neonFadeIn import NeonFadeIn

from visualizations.functions.generic.full import Full
from visualizations.functions.generic.fire import Fire

from scipy.ndimage.filters import gaussian_filter1d

def clampToNewRange(value, old_min, old_max, new_min, new_max):
    new_value = (((value - old_min) * (new_max - new_min)) // (old_max - old_min)) + new_min
    return new_value

class Visualizer(Full, AlternateColors, DrawLine, Scroll, IntensityChannels, Energy, Spectrum, Piano, Piano2, Fire, Envelope, NeonFadeIn):

    def __init__(self, config, index):
        """ The main class that contain all viz functions """

        self.strip_config = config.strips[index]
        self.number_of_audio_samples = config.audio_ports[config.strips[index].active_audio_channel_index].number_of_audio_samples
        self.timeSinceStart = config.timeSinceStart
        self.time_interval_ms_interval = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.time_interval)
        self.initVizualiser()
        self.resetFrame()

        self.audio_datas = []
        self.audio_data = []
        self.midi_datas = []

        self.pixelReshaper = PixelReshaper(config.strips[index])

        # print(interval)
        #
        # if(self.timeSinceStart.getMs() >= interval):
        #     self.alternate_colors_index += 1
        #     self.timeSinceStart.restart()

    def initVizualiser(self):
        self.number_of_pixels = self.strip_config.shapes[self.strip_config.active_shape_index].number_of_pixels
        self.gain = ExpFilter(
            np.tile(0.01, self.number_of_audio_samples),
            alpha_decay = 0.001,
            alpha_rise=0.99
        )

        self.initEnergy()
        self.initIntensityChannels()
        self.initSpectrum()

        self.initPiano()
        self.initPiano2()
        self.initEnvelope()

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
        """ Draw current pixels """
        self.audio_data = self.audio_datas[self.strip_config.active_audio_channel_index]

        pixels = []

        # SOUND BASED
        if(self.strip_config.active_visualizer_effect == "scroll"):
            pixels = self.visualizeScroll()
        if(self.strip_config.active_visualizer_effect == "energy"):
            pixels = self.visualizeEnergy()
        if(self.strip_config.active_visualizer_effect == "spectrum"):
            pixels = self.visualizeSpectrum()
        if(self.strip_config.active_visualizer_effect == "intensity_channels"):
            pixels = self.visualizeIntensityChannels()

        # MIDI BASED
        if(self.strip_config.active_visualizer_effect == "piano"):
            pixels = self.visualizePiano()
        if(self.strip_config.active_visualizer_effect == "piano2"):
            pixels = self.visualizePiano2()
        if(self.strip_config.active_visualizer_effect == "envelope"):
            pixels = self.visualizeEnvelope()

        # TIME BASED
        if(self.strip_config.active_visualizer_effect == "alternate_colors"):
            pixels = self.visualizeAlternateColors()
        if(self.strip_config.active_visualizer_effect == "alternate_colors_for_shapes"):
            pixels = self.visualizeAlternateColorsForShapes()
        if(self.strip_config.active_visualizer_effect == "draw_line"):
            pixels = self.visualizeDrawLine()

        # GENERIC
        if(self.strip_config.active_visualizer_effect == "full"):
            pixels = self.visualizeFull()
        if(self.strip_config.active_visualizer_effect == "fadeToNothing"):
            pixels = self.visualizeFadeToNothing()
        if(self.strip_config.active_visualizer_effect == "clear"):
            pixels = self.visualizeClear()
        if(self.strip_config.active_visualizer_effect == "fire"):
            pixels = self.visualizeFire()



        # import time
        # time.sleep(10)

        return pixels
