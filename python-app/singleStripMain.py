import sys, os, struct, serial, time, glob
import argparse
import numpy as np

from settings.settingsLoader import SettingsLoader

from helpers.time.framerateCalculator import FramerateCalculator
from helpers.time.bpmTicker import BPMTicker

from helpers.midiDispatcher import MidiDispatcher
from helpers.audioDispatcher import AudioDispatcher

from outputs.serialOutput import SerialOutput

from visualizations.visualizer import Visualizer
from visualizations.modSwitcher import ModSwitcher

if __name__ == "__main__":


    settingsLoader = SettingsLoader("../CONFIG.yml")

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="strip name",
                        type=str)
    args = parser.parse_args()

    print("Launching -> ", args.name)

    config = settingsLoader.data
    index = settingsLoader.findStripIndexByStripName(args.name)
    strip_config = config.strips[index]

    audioDispatcher = AudioDispatcher(config.audio_ports)

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

    # audioInterface = AudioInterface(
    #     visualizer,
    #     config,
    #     index
    # )

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

        # audioInterface.drawFrame()

        # print(framerateCalculator.getFps())
