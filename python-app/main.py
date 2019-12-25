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

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--list-devices", help="list available devices", action="store_true")

parser.add_argument("--test-audio-device", help="test a given audio port", type=str)
parser.add_argument("--test-midi-device", help="test a given midi port", type=str)
parser.add_argument("--test-serial-device", help="test a given serial port", type=str)
parser.add_argument("--test-config-file", help="test a given config file", type=str)

parser.add_argument("--single-strip", help="launch on the first strip", type=str)

parser.add_argument("--with-config-file", help="launch with spectific config file", type=str)

args = parser.parse_args()

if(args.list_devices):
    AudioInput.printDeviceList()
    MidiInput.printDeviceList()
    SerialOutput.printDeviceList()

elif(args.test_audio_device):
    AudioInput.testDevice(args.test_audio_device)

elif(args.test_midi_device):
    MidiInput.testDevice(args.test_midi_device)

elif(args.test_serial_device):
    SerialOutput.testDevice(args.test_serial_device)

elif(args.single_strip):

    config_file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/CONFIG.yml'

    settingsLoader = SettingsLoader(config_file_path)

    print("Launching -> ", args.single_strip)

    config = settingsLoader.data
    index = settingsLoader.findStripIndexByStripName(args.single_strip)
    strip_config = config.strips[index]

    audioDispatcher = AudioDispatcher(config.audio_ports)

    # shellInterface = ShellInterface()

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

        # shellInterface.printAudio(1, visualizer.audio_datas)
        # shellInterface.printStrip(10, serialOutput.is_connected, strip_config, pixels)
        # shellInterface.waitForInput()


elif not len(sys.argv) > 1:

    def audioProcess(shared_list):

        print("* Init Audio Process")

        config = shared_list[0]
        audioDispatcher = AudioDispatcher(config.audio_ports)

        while 1:

            audioDispatcher.dispatch()
            shared_list[1] = audioDispatcher.audio_datas

    def serialProcess(index, shared_list):

        config = shared_list[0]
        audio_datas = shared_list[1]
        strip_config = config.strips[index]

        serial_port_name = strip_config.serial_port_name
        number_of_pixels = strip_config.shapes[strip_config.active_shape_index].number_of_pixels

        print("* Init Serial process on port : ", serial_port_name)

        serialOutput = SerialOutput(
            number_of_pixels,
            serial_port_name
        )

        while 1:

            # shared_list[0].strips[index].is_online = serialOutput.isOnline()
            # print("is_online ", shared_list[0].strips[index].is_online)

            serialOutput.update(
                shared_list[2 + index]
            )

    def stripProcess(index, shared_list):

        print("* Init Strip process")

        config = shared_list[0]
        audio_datas = shared_list[1]
        strip_config = config.strips[index]
        strip_config.midi_logs = []

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

            # Updating midi logs
            strip_config.midi_logs += midiDispatcher.midi_datas_for_changing_mode
            strip_config.midi_logs += midiDispatcher.midi_datas_for_visualization
            if(len(strip_config.midi_logs) > 10):
                strip_config.midi_logs.pop(0)

            modSwitcher.changeMod()

            pixels = visualizer.drawFrame()
            pixels = visualizer.applyMaxBrightness(pixels, strip_config.max_brightness)
            pixels = np.clip(pixels, 0, 255).astype(int)

            shared_list[2 + index] = pixels

            # shared_list[0].strips[index] = config.strips[index]
            shared_list[0] = config

            # shared_list[2 + config.number_of_strips + index] = config.strips[index]
            # print(shared_list[2 + config.number_of_strips + index].is_mirror)

            time.sleep(config.delay_between_frames)

            # print("FPS from process ", serial_port_name, framerateCalculator.getFps())

    print("Parsing config file...")

    config_file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/CONFIG.yml'
    settingsLoader = SettingsLoader(config_file_path)

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

    max_workers = multiprocessing.cpu_count()
    number_of_workers = config.number_of_strips * 2 + 2

    print("Starting " + str(number_of_workers) + " sub-processes :")

    with concurrent.futures.ProcessPoolExecutor(
        max_workers = number_of_workers
    ) as executor:
        executor.submit(audioProcess, shared_list)
        for i in range(config.number_of_strips):
            executor.submit(stripProcess, i, shared_list)
            executor.submit(serialProcess, i, shared_list)

        time.sleep(1)

        shellInterface = ShellInterface()
        audio_datas = shared_list[1]
        pixels = [[],[],[]]

        shellInterface.printHeader()

        # shellInterface.drawBox((10, 10), (10, 10))

        for index in range(config.number_of_strips):

            strip_config = shared_list[0].strips[index]
            offset = (0, (index * 10) + 5)
            size = (83, 8)
            shellInterface.drawBox(offset, size)

        while 1:

            shellInterface.printAudio(0 * 10, audio_datas)
            shellInterface.waitForInput()

            for index in range(config.number_of_strips):

                pixels = shared_list[2 + index]
                strip_config = shared_list[0].strips[index]
                audio_datas = shared_list[1]
                shellInterface.printStrip((index * 10) + 5, True, strip_config, pixels)
