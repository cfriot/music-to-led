import time
import os
import sys
import logging
import psutil

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

import config

from debugInterface import DebugInterface
from audioInterface import AudioInterface
from timeSinceProcessStart import TimeSinceProcessStart

from audioFilters.audioProcessing import AudioProcessing
from audioFilters.dsp import *

from audioInput import AudioInput
from midiInput import MidiInput
from serialToArduinoLedStrip import SerialToArduinoLedStrip

from visualization import Visualization
from pixelReshaper import PixelReshaper


def setProcessDebugLevel():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def setProcessPriority():
    """Setup high process priority to prevent lag"""
    process = psutil.Process(os.getpid())
    process.nice(10)
    process.nice()


class LedStripVisualizer():
    def __init__(self, default_visualization_mod, audio_ports, midi_ports, serial_ports, strips_shape):
        self.active_mod = default_visualization_mod
        self.timeSinceProcessStart = TimeSinceProcessStart()

        self.audio_ports = audio_ports
        self.audio_channel_number = len(audio_ports)
        self.audio_datas = np.tile(0., (self.audio_channel_number, 24))
        self.active_audio_channel = 1
        self.audio_input_classes = []
        self.audio_processors = []
        for audio_port_name in audio_ports:
            self.audio_input_classes.append(AudioInput(audio_port_name))
            self.audio_processors.append(AudioProcessing())

        self.midi_ports = midi_ports
        self.midi_notes = []
        self.midi_input_classes = []
        for midi_port_name in midi_ports:
            self.midi_input_classes.append(MidiInput(midi_port_name))

        self.serial_ports = serial_ports
        self.visualizations = []
        self.pixel_reshapers = []
        self.serial_to_arduino_led_strip_classes = []

        self.total_pixel_number = 0
        self.number_of_strips = len(strips_shape)
        self.strips_shape = strips_shape
        for strip_length in strips_shape:
            self.total_pixel_number += strip_length

        for i, serial_port_name in enumerate(serial_ports):
            self.visualizations.append(
                Visualization(
                    self.timeSinceProcessStart,
                    default_visualization_mod="scroll",
                    total_pixel_number=self.total_pixel_number
                )
            )
            self.pixel_reshapers.append(
                PixelReshaper(
                    total_pixel_number=self.total_pixel_number,
                    strips_shape=self.strips_shape,
                    default_mods={"is_full_strip": True,
                                  "is_reverse": False, "is_mirror": False}
                )
            )
            print(serial_port_name)
            self.serial_to_arduino_led_strip_classes.append(
                SerialToArduinoLedStrip(
                    self.total_pixel_number,
                    [serial_port_name]
                )
            )
            self.serial_to_arduino_led_strip_classes[i].setup()

    # HANDLE TIC #####
    def handleTic(self):

        self.audio_datas = np.tile(0., (len(self.audio_ports), 24))
        for i, audio_input_class in enumerate(self.audio_input_classes):
            self.audio_datas[i] = self.audio_processors[i].render(
                audio_input_class.getRawData())

        self.midi_notes = []
        for midi_input_class in self.midi_input_classes:
            self.midi_notes += midi_input_class.getRawData()

        for i, serial_to_arduino_led_strip_class in enumerate(self.serial_to_arduino_led_strip_classes):
            self.visualizations[i].audio_data = self.audio_datas[self.active_audio_channel]
            filtered_midi_notes = []
            for midi_note in self.midi_notes:
                if(midi_note["port"] == "Ableton-virtual-midi-ouput LeftSynth" and i == 0):
                    filtered_midi_notes.append(midi_note)
                if(midi_note["port"] == "Ableton-virtual-midi-ouput RightSynth" and i == 1):
                    filtered_midi_notes.append(midi_note)
            self.visualizations[i].midi_notes = filtered_midi_notes
            self.serial_to_arduino_led_strip_classes[i].update(
                self.pixel_reshapers[i].reshape(
                    self.visualizations[i].drawFrame()
                )
            )
            self.handleChangeMod(
                self.visualizations[i], self.pixel_reshapers[i])

    # CHANGE MOD #####
    def handleChangeMod(self, visualization, pixelReshaper):
        if(self.midi_notes):
            for midi_note in self.midi_notes:
                if(midi_note["port"] == "Ableton-virtual-midi-ouput ChangeMod"):
                    if(midi_note["note"] == 0):
                        self.active_mod = "scroll"
                        visualization.resetFrame()
                        visualization.visualizationEffect = visualization.visualizeScroll
                    elif(midi_note["note"] == 2):
                        self.active_mod = "energy"
                        visualization.resetFrame()
                        visualization.visualizationEffect = visualization.visualizeEnergy
                    elif(midi_note["note"] == 4):
                        self.active_mod = "synth"
                        visualization.resetFrame()
                        visualization.visualizationEffect = visualization.visualizeSynth
                    elif(midi_note["note"] == 5):
                        self.active_mod = "full"
                        visualization.resetFrame()
                        self.old_full_intensity = 0
                        visualization.visualizationEffect = visualization.visualizeFull
                    elif(midi_note["note"] == 7):
                        self.active_mod = "nothing"
                        self.old_full_intensity = 1
                        visualization.visualizationEffect = visualization.visualizeNothing
                    elif(midi_note["note"] == 9):
                        self.active_mod = "intensity_bounce"
                        visualization.resetFrame()
                        visualization.visualizationEffect = visualization.visualizeIntensityBounce
                    elif(midi_note["note"] == 11):
                        self.active_mod = "visualize_alternate_colors"
                        visualization.resetFrame()
                        visualization.visualizationEffect = visualization.visualizeAlternateColors
                    elif(midi_note["note"] == 12):
                        pixelReshaper.is_reverse = not pixelReshaper.is_reverse
                        print("Change mod to reverse mod => %s" %
                              pixelReshaper.is_reverse)
                    elif(midi_note["note"] == 14):
                        pixelReshaper.is_full_strip = not pixelReshaper.is_full_strip
                        print("Change mod to full strip mod => %s" %
                              pixelReshaper.is_full_strip)
                    elif(midi_note["note"] == 16):
                        pixelReshaper.is_mirror = not pixelReshaper.is_mirror
                        print("Change mod to mirror mod => %s" %
                              pixelReshaper.is_mirror)
                    elif(midi_note["note"] == 17):
                        visualization.is_monochrome = not visualization.is_monochrome
                        print("Change mod to monochrome => %s" %
                              visualization.is_monochrome)
                    elif(midi_note["note"] == 19):
                        self.active_audio_channel += 1
                        if(self.active_audio_channel > self.audio_channel_number - 1):
                            self.active_audio_channel = 0
                        print("Change audio mod to => %s" %
                              self.active_audio_channel)


if __name__ == '__main__':

    setProcessDebugLevel()
    setProcessPriority()

    audio_channels = [{
        "port": "Background Music",
        "min_frequency": 200,
        "max_frequency": 12000,
    }, {
        "port": "Built-in Microphone",
        "min_frequency": 200,
        "max_frequency": 12000,
    }]

    # strips_shape = [34, 52, 50]
    strips_shape = [126, 126]
    strips_shape = [63, 63, 63, 63]
    strips_shape = [34, 52, 50]
    # strips_shape = [5, 15]

    audio_ports = ["Background Music", "Built-in Microphone"]
    midi_ports = ["Ableton-virtual-midi-ouput ChangeMod",
                  "Ableton-virtual-midi-ouput LeftSynth",
                  "Ableton-virtual-midi-ouput RightSynth"]
    serial_ports = ["/dev/tty.usbserial-14210"]
    # serial_ports = SerialToArduinoLedStrip.listAvailableUsbSerialPorts()

    ledStripVisualizer = LedStripVisualizer(
        "scroll", audio_ports, midi_ports, serial_ports, strips_shape)

    if(config.DISPLAY_AUDIO_INTERFACE):
        audioInterface = AudioInterface(ledStripVisualizer.visualizations[0])
    if(config.DISPLAY_SHELL_INTERFACE):
        debugInterface = DebugInterface(ledStripVisualizer.visualizations[0])

    while True:

        ledStripVisualizer.handleTic()

        if(config.DISPLAY_AUDIO_INTERFACE):
            audioInterface.drawFrame()
        if(config.DISPLAY_SHELL_INTERFACE):
            debugInterfac
