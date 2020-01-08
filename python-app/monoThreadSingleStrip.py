# This file is for debugging purpose

import sys, os, struct, serial, time, glob, multiprocessing, logging, argparse
import concurrent.futures
from multiprocessing import Pool
import numpy as np

from config.configLoader import ConfigLoader

from helpers.time.timeSinceStart import TimeSinceStart
from helpers.time.framerateCalculator import FramerateCalculator

from helpers.midiDispatcher import MidiDispatcher
from helpers.audioDispatcher import AudioDispatcher

from inputs.audioInput import AudioInput
from inputs.midiInput import MidiInput
from outputs.serialOutput import SerialOutput

from visualizations.visualizer import Visualizer
from visualizations.pixelReshaper import PixelReshaper
from visualizations.modSwitcher import ModSwitcher


configLoader = ConfigLoader("./CONFIG.yml")

strip_name = "Front Desk"

print("Launching -> ", strip_name)

config = configLoader.data
index = configLoader.findStripIndexByStripName(strip_name)
strip_config = config.strips[index]
active_state = config.states[strip_config.active_state_index]

audioDispatcher = AudioDispatcher(
                    audio_ports = config.audio_ports,
                    framerate = config.desirated_framerate
                )

framerateCalculator = FramerateCalculator(config.desirated_framerate)

midi_ports_for_changing_mode = strip_config.midi_ports_for_changing_mode
midi_ports_for_visualization = strip_config.midi_ports_for_visualization

midiDispacther = MidiDispatcher(
    midi_ports_for_changing_mode,
    midi_ports_for_visualization
)

serial_port_name = config.strips[index].serial_port_name
number_of_pixels = active_state.shapes[active_state.active_shape_index].number_of_pixels

serialOutput = SerialOutput(
    number_of_pixels = number_of_pixels,
    port = serial_port_name
)

visualizer = Visualizer(
    config,
    index
)

modSwitcher = ModSwitcher(
    visualizer,
    config,
    index,
    True
)

while 1:

    audioDispatcher.dispatch()
    midiDispacther.dispatch()

    visualizer.audio_datas = audioDispatcher.audio_datas
    modSwitcher.midi_datas = midiDispacther.midi_datas_for_changing_mode
    visualizer.midi_datas =  midiDispacther.midi_datas_for_visualization

    modSwitcher.changeMod()

    pixels = visualizer.drawFrame()
    pixels = visualizer.applyMaxBrightness(pixels, active_state.max_brightness)
    pixels = np.clip(pixels, 0, 255).astype(int)

    serialOutput.update(
        pixels
    )
