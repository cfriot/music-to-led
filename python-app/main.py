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

parser = argparse.ArgumentParser()

parser.add_argument("--list-devices", help="List available devices.", action="store_true")

parser.add_argument("--test-audio-device", help="Test a given audio port.", type=str, metavar="PORT_NAME")
parser.add_argument("--test-midi-device", help="Test a given midi port.", type=str, metavar="PORT_NAME")
parser.add_argument("--test-serial-device", help="Test a given serial port.", type=str, metavar="PORT_NAME")
parser.add_argument(
    "--test-config-file",
    help="Test a given config file. If your type \"\", it will test the default config file.",
    metavar="FILE_PATH"
)

parser.add_argument("--single-strip", help="Launch on the first strip.", type=str)

parser.add_argument(
    "--with-config-file",
    help="Launch with spectific config file.",
    type=str,
    default=os.path.abspath(os.path.dirname(sys.argv[0])) + '/CONFIG.yml',
    metavar="FILE_PATH"
)

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

elif(args.test_config_file):
    ConfigLoader.testConfig(path=args.test_config_file, verbose=False)

elif not len(sys.argv) > 1:

    def audioProcess(shared_list):

        config = shared_list[0]
        ports = ""
        for port in config.audio_ports:
            ports += port.name
        print("- Init Audio process on ports : ", ports)

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

        print("- Init Serial process on port : ", serial_port_name)

        serialOutput = SerialOutput(
            number_of_pixels=number_of_pixels,
            port=serial_port_name
        )

        i = 0

        while 1:
            shared_list[2 + config.number_of_strips + index] = serialOutput.isOnline()
            serialOutput.update(
                shared_list[2 + index][0]
            )

    def stripProcess(index, shared_list):

        config = shared_list[0]
        strip_config = config.strips[index]
        audio_datas = shared_list[1]
        strip_config.midi_logs = []

        print("- Init strip process : ", strip_config.name)


        framerateCalculator = FramerateCalculator(config.fps)

        midi_ports_for_visualization = strip_config.midi_ports_for_visualization
        midi_ports_for_changing_mode = strip_config.midi_ports_for_changing_mode

        midiDispatcher = MidiDispatcher(
            midi_ports_for_changing_mode,
            midi_ports_for_visualization
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
            index,
            not config.display_interface
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

            shared_list[2 + index] = [pixels, strip_config, framerateCalculator.getFps(), True]

            time.sleep(config.delay_between_frames)

    print("- Parsing and testing config file...")

    configLoader = ConfigLoader(args.with_config_file, debug=False)

    config = configLoader.data
    number_of_strips = config.number_of_strips

    manager = multiprocessing.Manager()
    shared_list = manager.list()
    # Shared list :
    # 0     : Config
    # 1     : Audio datas
    # 2...n : [pixels, strip_config, framerateCalculator.getFps()]
    # 2 + config.number_of_strips + ...n : isOnline for each strip

    shared_list.append(config)

    shared_list.append(np.tile(0.,(config.number_of_audio_ports, 24)))

    for i in range(config.number_of_strips):
        shared_list.append([np.tile(0.,(config.number_of_audio_ports, 24)), config.strips[0], 0, False])

    for i in range(config.number_of_strips):
        shared_list.append(False)

    max_workers = multiprocessing.cpu_count()
    number_of_workers = config.number_of_strips * 2 + 2

    print("- Starting " + str(number_of_workers) + " sub-processes :")

    with concurrent.futures.ProcessPoolExecutor(
        max_workers = number_of_workers
    ) as executor:
        executor.submit(audioProcess, shared_list)
        for i in range(config.number_of_strips):
            executor.submit(stripProcess, i, shared_list)
            executor.submit(serialProcess, i, shared_list)

        if(config.display_interface):

            time.sleep(1)
            print("- Starting GUI ...")
            time.sleep(1)

            shellInterface = ShellInterface(config)
            audio_datas = shared_list[1]
            pixels = [[],[],[]]
            audio_offset = 7
            strip_offset = 12
            rgb_border_color = (100,100,100)
            rgb_inner_border_color = (50,50,50)

            while 1:

                for index in range(config.number_of_audio_ports):
                    shellInterface.printAudio(audio_offset, (32 * index) + 1, config.audio_ports[index].name, shared_list[1][index])

                # shellInterface.waitForInput()

                for index in range(config.number_of_strips):

                    pixels = shared_list[2 + index][0]
                    strip_config = shared_list[2 + index][1]
                    fps = shared_list[2 + index][2]
                    is_online = shared_list[2 + config.number_of_strips + index]
                    audio_datas = shared_list[1]
                    shellInterface.printStrip(strip_offset + (index * 8), is_online, fps, strip_config, pixels)
