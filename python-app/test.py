import sys, os, struct, serial, time, glob, multiprocessing, logging, argparse
import concurrent.futures
from multiprocessing import Pool
import numpy as np

from settings.settingsLoader import SettingsLoader

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


audio_datas = []

number_of_pixels = 80

pixels = np.tile(1, (3, number_of_pixels))
pixels *= 0
pixels[0, 0] = 125  # Set 1st pixel red
pixels[1, 1] = 125  # Set 2nd pixel green
pixels[2, 2] = 125  # Set 3rd pixel blue
pixels[0, 3] = 255  # Set 1st pixel red
pixels[1, 4] = 255  # Set 2nd pixel green
pixels[2, 5] = 255  # Set 3rd pixel blue

config_file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/CONFIG.yml'
settingsLoader = SettingsLoader(config_file_path)

config = settingsLoader.data
number_of_strips = config.number_of_strips

audioDispatcher = AudioDispatcher(config.audio_ports)

print(config.audio_ports[0].name)

# shellInterface = ShellInterface()
# shellInterface.printHeader()

for index in range(config.number_of_strips):

    strip_config = config.strips[index]
    offset = (0, (index * 10) + 15)
    size = (83, 8)
    # shellInterface.drawBox(offset, size)

while 1:

    # shellInterface.waitForInput()

    pixels = np.roll(pixels, 1, axis=1)

    for index in range(config.number_of_strips):

        strip_config = config.strips[index]
        # shellInterface.printAudio(10, audioDispatcher.audio_datas)
        # shellInterface.printStrip((index * 10) + 15, True, strip_config, pixels)
