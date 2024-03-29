import numpy as np

from copy import deepcopy

from scipy.ndimage.filters import gaussian_filter1d

from visualizations.pixelReshaper import PixelReshaper

from helpers.audio.expFilter import ExpFilter

from visualizations.functions.sound.scroll import Scroll
from visualizations.functions.sound.energy import Energy
from visualizations.functions.sound.channelIntensity import ChannelIntensity
from visualizations.functions.sound.channelFlash import ChannelFlash
from visualizations.functions.sound.spectrum import Spectrum

from visualizations.functions.midi.pianoNote import PianoNote
from visualizations.functions.midi.pianoScroll import PianoScroll
from visualizations.functions.midi.pitchwheelFlash import PitchwheelFlash

from visualizations.functions.time.alternateColors import AlternateColors
from visualizations.functions.time.transitionColors import TransitionColors
from visualizations.functions.time.drawLine import DrawLine

from visualizations.functions.generic.fullColor import FullColor
from visualizations.functions.generic.fadeOut import FadeOut
from visualizations.functions.generic.clear import Clear
from visualizations.functions.generic.fire import Fire

from scipy.ndimage.filters import gaussian_filter1d


class Visualizer(Spectrum, FullColor, FadeOut, Clear, AlternateColors, TransitionColors, DrawLine, Scroll, ChannelIntensity, ChannelFlash, Energy, PianoNote, PianoScroll, Fire, PitchwheelFlash):

    def __init__(self, config, index):
        """ The main class that contain all viz functions """

        self.config = config
        self.strip_config = config.strips[index]
        self.pixelReshaper = PixelReshaper(self.config, index)

        self.audio_datas = []
        self.audio_data = []
        self.midi_datas = []

        self.initVizualiser()

    def initVizualiser(self):

        self.active_state = self.strip_config.active_state
        self.number_of_pixels = self.active_state.shapes[self.active_state.active_shape_index].number_of_pixels

        self.timeSinceStart = self.config.timeSinceStart
        self.number_of_audio_samples = self.config.audio_ports[self.active_state.active_audio_channel_index].number_of_audio_samples

        self.gain = ExpFilter(
            np.tile(0.01, self.number_of_audio_samples),
            alpha_decay = 0.001,
            alpha_rise=0.99
        )

        self.initEnergy()
        self.initSpectrum()
        self.initChannelIntensity()
        self.initChannelFlash()

        self.initPianoNote()
        self.initPianoScroll()
        self.initPitchwheelFlash()

        self.initAlternateColors()
        self.initTransitionColorShapes()

        self.initFullColor()
        self.initFadeOut()
        self.initFire()
        self.resetFrame()

        self.pixelReshaper.initActiveShape()


    def filterAudioDatas(self, audio_data):

        # self.config.audio_datas

        min = self.active_state.audio_samples_filter_min
        max = self.active_state.audio_samples_filter_max

        new_audio_data = audio_data.copy()
        # audio_channel_min_frequency, audio_channel_max_frequency
        for i, sample in enumerate(audio_data):
            if(i < min or i > max):
                new_audio_data[i] = sample * 0
            else:
                new_audio_data[i] = sample

        return new_audio_data

    @staticmethod
    def clampToNewRange(value, old_min, old_max, new_min, new_max):
        new_value = (((value - old_min) * (new_max - new_min)) // (old_max - old_min)) + new_min
        return new_value

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
        return np.clip(pixels, 0, max_brightness)

    def drawFrame(self):
        """ Return current pixels """
        self.audio_data = self.audio_datas[self.active_state.active_audio_channel_index]
        self.audio_data = self.filterAudioDatas(self.audio_datas[self.active_state.active_audio_channel_index])


        pixels = []

        # SOUND BASED
        if(self.active_state.active_visualizer_effect == "scroll"):
            pixels = self.visualizeScroll()
        elif(self.active_state.active_visualizer_effect == "energy"):
            pixels = self.visualizeEnergy()
        elif(self.active_state.active_visualizer_effect == "channel_intensity"):
            pixels = self.visualizeChannelIntensity()
        elif(self.active_state.active_visualizer_effect == "channel_flash"):
            pixels = self.visualizeChannelFlash()
        elif(self.active_state.active_visualizer_effect == "spectrum"):
            pixels = self.visualizeSpectrum()

        # MIDI BASED
        elif(self.active_state.active_visualizer_effect == "piano_scroll"):
            pixels = self.visualizePianoScroll()
        elif(self.active_state.active_visualizer_effect == "piano_note"):
            pixels = self.visualizePianoNote()
        elif(self.active_state.active_visualizer_effect == "pitchwheel_flash"):
            pixels = self.visualizePitchwheelFlash()

        # TIME BASED
        elif(self.active_state.active_visualizer_effect == "alternate_color_chunks"):
            pixels = self.visualizeAlternateColorChunks()
        elif(self.active_state.active_visualizer_effect == "alternate_color_shapes"):
            pixels = self.visualizeAlternateColorShapes()
        # elif(self.active_state.active_visualizer_effect == "transition_color_shapes"):
        #     pixels = self.visualizeTransitionColorShapes()
        elif(self.active_state.active_visualizer_effect == "draw_line"):
            pixels = self.visualizeDrawLine()

        # GENERIC
        elif(self.active_state.active_visualizer_effect == "full_color"):
            pixels = self.visualizeFullColor()
        elif(self.active_state.active_visualizer_effect == "fade_out"):
            pixels = self.VisualizeFadeOut()
        elif(self.active_state.active_visualizer_effect == "clear_frame"):
            pixels = self.visualizeClear()
        elif(self.active_state.active_visualizer_effect == "fire"):
            pixels = self.visualizeFire()

        else:
            print("Oops... There is no visualization function that match with the active visualizer effect")
            pixels = self.visualizeClear()

        # filterAudioDatas(self.audio_datas)
        return pixels
