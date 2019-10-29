import sys, os, struct, serial, time, glob, multiprocessing, logging, json
import concurrent.futures
from multiprocessing import Pool
import numpy as np

if __name__ == "__main__":


    class Titi():
        __init__(self):
            self.tititu = 1

    class Toto():
        __init__(self):
            self.tototu = 1
            self.subclass = Titi()

    def stripProcess(index, shared_list):

        print("Init strip process")

        config = shared_list[0]
        audio_datas = shared_list[1]
        strip_config = config.strips[index]

        framerateCalculator = FramerateCalculator(config.fps)

        associated_midi_channels = strip_config.associated_midi_channels
        midi_ports_for_changing_mode = strip_config.midi_ports_for_changing_mode

        midiDispatcher = MidiDispatcher(
            midi_ports_for_changing_mode,
            associated_midi_channels
        )

        visualizer = Visualizer(
            config,
            index
        )

        serial_port_name = strip_config.serial_port_name
        number_of_pixels = strip_config.shapes[strip_config.active_shape_index].number_of_pixels

        modSwitcher = ModSwitcher(
            visualizer,
            config,
            index
        )

        while 1:

            visualizer.audio_datas = shared_list[1]

            midiDispatcher.dispatch()

            modSwitcher.midi_datas = midiDispatcher.midi_datas_for_changing_mode
            visualizer.midi_datas =  midiDispatcher.midi_datas_for_visualization

            modSwitcher.changeMod()

            pixels = visualizer.drawFrame()
            pixels = np.clip(pixels, 0, 255).astype(int)

            shared_list[2 + index] = pixels


            # shared_list[0].strips[index] = config.strips[index]
            print("strip_config before pixels", strip_config)
            strip_config.pixels = pixels
            print("strip_config after pixels", strip_config)
            # shared_list[0] = config

            print("shared_list[0]", shared_list[0])
            print("config", config)
            time.sleep(1)

            # time.sleep(config.delay_between_frames)

            # print("FPS from process ", serial_port_name, framerateCalculator.getFps())

    print("Parsing config file")
    settingsLoader = SettingsLoader("settings/settings_file.yml")
    config = settingsLoader.data
    number_of_strips = config.number_of_strips

    manager = multiprocessing.Manager()
    shared_list = manager.list()
    # Shared list :
    # 0     : Config
    # 1     : Audio datas
    # 2...n : Pixels
    shared_list.append(config)
    shared_list.append(np.tile(0.,(config.number_of_audio_ports, 24)))

    for i in range(config.number_of_strips):
        shared_list.append([])

    print("Starting sub-processes")

    max_workers = multiprocessing.cpu_count()
    number_of_workers = config.number_of_strips * 2 + 2

    with concurrent.futures.ProcessPoolExecutor(
        max_workers = number_of_workers
    ) as executor:
        executor.submit(audioProcess, shared_list)
        executor.submit(apiProcess, shared_list)
