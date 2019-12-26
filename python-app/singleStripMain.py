import sys, os, struct, serial, time, glob, multiprocessing, logging, argparse
import concurrent.futures
from multiprocessing import Pool
import numpy as np

from config.configLoader import ConfigLoader

from gui.shellInterface import ShellInterface

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

print("Launching -> ", args.single_strip)

config = configLoader.data
index = configLoader.findStripIndexByStripName(args.single_strip)
strip_config = config.strips[index]

audioDispatcher = AudioDispatcher(config.audio_ports)

shellInterface = ShellInterface()

framerateCalculator = FramerateCalculator(config.fps)

midi_ports_for_changing_mode = strip_config.midi_ports_for_changing_mode
associated_midi_channels = strip_config.associated_midi_channels

midiDispacther = MidiDispatcher(
    midi_ports_for_changing_mode,
    associated_midi_channels
)

visualizer = Visualizer(
    config,
    index
)

serial_port_name = config.strips[index].serial_port_name
number_of_pixels = strip_config.shapes[strip_config.active_shape_index].number_of_pixels

serialOutput = SerialOutput(
    number_of_pixels,
    serial_port_name
)

modSwitcher = ModSwitcher(
    visualizer,
    config,
    index
)

while 1:

    audioDispatcher.dispatch()
    midiDispacther.dispatch()

    visualizer.audio_datas = audioDispatcher.audio_datas
    modSwitcher.midi_datas = midiDispacther.midi_datas_for_changing_mode
    visualizer.midi_datas =  midiDispacther.midi_datas_for_visualization

    modSwitcher.changeMod()

    pixels = visualizer.drawFrame()

    pixels = np.clip(pixels, 0, strip_config.max_brightness).astype(int)

    serialOutput.update(
        pixels
    )

    shellInterface.printAudio(1, 1, config.audio_ports[index].name, audioDispatcher.audio_datas[index])
    shellInterface.printStrip(10, serialOutput.is_connected, strip_config, pixels)
    shellInterface.waitForInput()
