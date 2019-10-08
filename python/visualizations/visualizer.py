import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

from visualizations.pixelReshaper import PixelReshaper

from helpers.audio.expFilter import ExpFilter

from visualizations.functions.full import Full
from visualizations.functions.alternateColors import AlternateColors
from visualizations.functions.scroll import Scroll
from visualizations.functions.intensityBounce import IntensityBounce
from visualizations.functions.intensityChannels import IntensityChannels
from visualizations.functions.energy import Energy
from visualizations.functions.spectrum import Spectrum
from visualizations.functions.piano import Piano
from visualizations.functions.neonFadeIn import NeonFadeIn


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
        self.pixelReshaper = PixelReshaper(config.strips[index])


        self.initSpectrum()
        self.initFull()

        self.visualizer_effect = self.visualizeScroll

    def initVizualiser(self):
        self.number_of_pixels = self.strip_config.shapes[0].number_of_pixels
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

    def resetFrame(self):
        """ Reset current pixels """
        self.pixels = np.tile(0., (3, self.number_of_pixels))

    # DRAW FRAME #####
    def drawFrame(self):
        """ Draw current pixels """
        self.audio_data = self.audio_datas[self.strip_config.active_audio_channel_index]
        # tmp = self.visualizer_effect()
        # tmp2 = self.visualizeAlternateColors()
        # tmp[0] += tmp2[0]
        # tmp[1] += tmp2[1]
        # tmp[2] += tmp2[2]
        return self.visualizer_effect()
