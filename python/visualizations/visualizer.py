import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

from visualizations.pixelReshaper import PixelReshaper

from helpers.audio.expFilter import ExpFilter


from visualizations.functions.sound.scroll import Scroll
from visualizations.functions.sound.energy import Energy
from visualizations.functions.sound.spectrum import Spectrum
from visualizations.functions.sound.intensityBounce import IntensityBounce
from visualizations.functions.sound.intensityChannels import IntensityChannels

from visualizations.functions.midi.piano import Piano

from visualizations.functions.bpm.alternateColors import AlternateColors
from visualizations.functions.bpm.neonFadeIn import NeonFadeIn

from visualizations.functions.generic.full import Full


class Visualizer(Full, AlternateColors, Scroll, IntensityBounce, IntensityChannels, Energy, Spectrum, Piano, NeonFadeIn):

    def __init__(self, config, index):
        """ The main class that contain all viz functions """

        self.strip_config = config.strips[index]
        self.N_FFT_BINS = config.number_of_audio_samples
        self.initVizualiser()
        self.resetFrame()

        self.audio_datas = []
        self.audio_data = []
        self.midi_datas = []

        self.timeSinceStart = config.timeSinceStart
        self.bpm_ms_interval = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm)
        self.pixelReshaper = PixelReshaper(config.strips[index])

        # print(interval)
        #
        # if(self.timeSinceStart.getMs() >= interval):
        #     self.alternate_colors_index += 1
        #     self.timeSinceStart.restart()

    def initVizualiser(self):
        self.number_of_pixels = self.strip_config.shapes[self.strip_config.active_shape_index].number_of_pixels
        self.gain = ExpFilter(
            np.tile(0.01, self.N_FFT_BINS),
            alpha_decay = 0.001,
            alpha_rise=0.99
        )
        self.p_filt = ExpFilter(
            np.tile(1, (3, self.number_of_pixels)),
            alpha_decay = 0.1,
            alpha_rise=0.99
        )
        self.common_mode = ExpFilter(
            np.tile(0.01, self.number_of_pixels // 2),
            alpha_decay = 0.99,
            alpha_rise=0.01
        )
        self.initSpectrum()
        self.initFull()
        self.initAlternateColors()


    def resetFrame(self):
        """ Reset current pixels """
        self.pixels = np.tile(0., (3, self.number_of_pixels))


    def drawFrame(self):
        """ Draw current pixels """
        self.audio_data = self.audio_datas[self.strip_config.active_audio_channel_index]

        # SOUND BASED
        if(self.strip_config.active_visualizer_effect == "scroll"):
            return self.visualizeScroll()
        if(self.strip_config.active_visualizer_effect == "energy"):
            return self.visualizeEnergy()
        if(self.strip_config.active_visualizer_effect == "intensity_channels"):
            return self.visualizeIntensityChannels()
        if(self.strip_config.active_visualizer_effect == "spectrum"):
            return self.visualizeSpectrum()

        # MIDI BASED
        if(self.strip_config.active_visualizer_effect == "piano"):
            return self.visualizePiano()

        # BPM BASED
        if(self.strip_config.active_visualizer_effect == "alternate_colors"):
            return self.visualizeAlternateColors()
        if(self.strip_config.active_visualizer_effect == "alternate_colors_full"):
            return self.visualizeAlternateColorsFull()
        if(self.strip_config.active_visualizer_effect == "alternate_colors_for_shapes"):
            return self.visualizeAlternateColorsForShapes()
        if(self.strip_config.active_visualizer_effect == "full"):
            return self.visualizeFull()
        if(self.strip_config.active_visualizer_effect == "nothing"):
            return self.visualizeNothing()

        return self.pixels