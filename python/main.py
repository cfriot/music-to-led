import sys, os, struct, serial, time, glob, multiprocessing, logging
import concurrent.futures
from multiprocessing import Pool
import numpy as np

from settings.settingsLoader import SettingsLoader

from helpers.time.timeSinceStart import TimeSinceStart
from helpers.time.framerateCalculator import FramerateCalculator

from helpers.midiDispatcher import MidiDispatcher
from helpers.audioDispatcher import AudioDispatcher

from outputs.serialToArduinoLedStrip import SerialToArduinoLedStrip

from visualizations.visualizer import Visualizer
from visualizations.pixelReshaper import PixelReshaper
from visualizations.modSwitcher import ModSwitcher

if __name__ == "__main__":

    def audioProcess(shared_list):

        print("Init Audio Process")

        config = shared_list[0]
        audioDispatcher = AudioDispatcher(config.audio_ports)

        while 1:

            audioDispatcher.dispatch()
            shared_list[1] = audioDispatcher.audio_datas


    def stripProcess(index, shared_list):

        print("Init strip process")

        config = shared_list[0]
        audio_datas = shared_list[1]

        strip_config = config.strips[index]
        serial_port_name = config.strips[index].serial_port_name
        number_of_pixels = strip_config.shapes[strip_config.active_shape_index].number_of_pixels
        associated_midi_channels = strip_config.associated_midi_channels
        midi_port_for_changing_mode = config.midi_port_for_changing_mode
        number_of_audio_ports = config.number_of_audio_ports

        framerateCalculator = FramerateCalculator(config.fps)

        midiDispatcher = MidiDispatcher(
            midi_port_for_changing_mode,
            associated_midi_channels
        )

        visualizer = Visualizer(
            config,
            index
        )

        serialToArduinoLedStrip = SerialToArduinoLedStrip(
            number_of_pixels,
            serial_port_name
        )

        modSwitcher = ModSwitcher(
            visualizer,
            serialToArduinoLedStrip,
            config,
            index
        )

        while 1:

            visualizer.audio_datas = shared_list[1]

            midiDispatcher.dispatch()
            modSwitcher.midi_datas = midiDispatcher.midi_datas_for_changing_mode
            visualizer.midi_datas =  midiDispatcher.midi_datas_for_visualization

            modSwitcher.changeMod()

            serialToArduinoLedStrip.update(
                visualizer.drawFrame()
            )

            # print("FPS from process ", serial_port_name, framerateCalculator.getFps())

    settingsLoader = SettingsLoader("settings/settings_file.yml")
    config = settingsLoader.data

    manager = multiprocessing.Manager()
    shared_list = manager.list()
    # Shared list :
    # 0 : Config
    # 1 : Audio datas
    shared_list.append(config)
    shared_list.append(np.tile(0.,(config.number_of_audio_ports, 24)))

    number_of_strips = config.number_of_strips

    print("Start Sub Processes")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(audioProcess, shared_list)
        for i in range(number_of_strips):
            executor.submit(stripProcess, i, shared_list)
