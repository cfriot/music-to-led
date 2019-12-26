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


audio_datas = []

number_of_pixels = 80

pixels = np.tile(1, (3, number_of_pixels))
pixels *= 0
pixels[0, 0] = 125  # Set 1st pixel red
pixels[1, 1] = 125  # Set 2nd pixel green
pixels[2, 2] = 125  # Set 3rd pixel blue

config_file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/CONFIG.yml'
configLoader = ConfigLoader(config_file_path)

config = configLoader.data
number_of_strips = config.number_of_strips

audioDispatcher = AudioDispatcher(config.audio_ports)

print(config.audio_ports[0].name)

shellInterface = ShellInterface()

header_offset = 0
audio_offset = 7
strip_offset = 12
rgb_border_color = (100,100,100)
rgb_inner_border_color = (50,50,50)
shellInterface.printHeader(header_offset)

for index in range(config.number_of_audio_ports):

    strip_config = config.strips[index]
    offset = ((index * 32), audio_offset)
    size = (29, 3)
    shellInterface.drawBox(offset, size, rgb_border_color)

y = 12
for index in range(config.number_of_strips):

    strip_config = config.strips[index]
    offset = (0, y + (index * 8))
    size = (83, 6)
    shellInterface.drawBox(offset, size, rgb_border_color)

while 1:

    audioDispatcher.dispatch()
    shellInterface.waitForInput()

    pixels = np.roll(pixels, 1, axis=1)

    for index in range(config.number_of_audio_ports):
        shellInterface.printAudio(audio_offset, (32 * index) + 1, config.audio_ports[index].name, audioDispatcher.audio_datas[index])

    for index in range(config.number_of_strips):

        strip_config = config.strips[index]
        shellInterface.printStrip(strip_offset + (index * 8), True, 30, strip_config, pixels)
