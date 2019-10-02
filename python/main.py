import sys
import struct
import serial
import time
import glob
import multiprocessing
import concurrent.futures
import numpy as np
from multiprocessing import Pool

import config
from timeSinceProcessStart import TimeSinceProcessStart
from serialToArduinoLedStrip import SerialToArduinoLedStrip
from audioInput import AudioInput
from debugInterface import DebugInterface, FramerateCalculator
from midiInput import MidiInput
from audioFilters.audioProcessing import AudioProcessing
from audioFilters.dsp import *
from visualization import Visualization
from pixelReshaper import PixelReshaper


if __name__ == "__main__":

    def audioProcess(shared_list):
        print("AUDIO PROCESS")
        config = shared_list[0]

        audio_ports = config["audio_ports"]
        audio_channel_number = len(config["audio_ports"])
        audio_datas = np.tile(0., (audio_channel_number, 24))
        audio_input_classes = []
        audio_processors = []
        for audio_port in audio_ports:
            audio_input_classes.append(AudioInput(audio_port["name"]))
            audio_processors.append(AudioProcessing())

        shared_list[1] = audio_datas

        while 1:
            audio_datas = []
            for i in range(audio_channel_number):
                audio_datas.append(audio_processors[i].render(audio_input_classes[i].getRawData()))
            shared_list[1] = audio_datas
            # print(audio_datas)
            time.sleep(0.01)

    def handleChangeMod(midi_notes, active_audio_channel, audio_channel_number, visualization, pixelReshaper):
        if(midi_notes):
            print("CHANGEMOD")
            for midi_note in midi_notes:
                if(midi_note["note"] == 0):
                    visualization.active_mod = "scroll"
                    visualization.resetFrame()
                    visualization.visualizationEffect = visualization.visualizeScroll
                elif(midi_note["note"] == 2):
                    visualization.active_mod = "energy"
                    visualization.resetFrame()
                    visualization.visualizationEffect = visualization.visualizeEnergy
                elif(midi_note["note"] == 4):
                    visualization.active_mod = "synth"
                    visualization.resetFrame()
                    visualization.visualizationEffect = visualization.visualizeSynth
                elif(midi_note["note"] == 5):
                    visualization.active_mod = "full"
                    visualization.resetFrame()
                    old_full_intensity = 0
                    visualization.visualizationEffect = visualization.visualizeFull
                elif(midi_note["note"] == 7):
                    visualization.active_mod = "nothing"
                    old_full_intensity = 1
                    visualization.visualizationEffect = visualization.visualizeNothing
                elif(midi_note["note"] == 9):
                    visualization.active_mod = "intensity_bounce"
                    visualization.resetFrame()
                    visualization.visualizationEffect = visualization.visualizeIntensityBounce
                elif(midi_note["note"] == 11):
                    visualization.active_mod = "visualize_alternate_colors"
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
                    visualization.active_audio_channel += 1
                    if(visualization.active_audio_channel > visualization.audio_channel_number):
                        visualization.active_audio_channel = 0
                    print("Change audio mod to => %s" %
                          active_audio_channel)
                elif(midi_note["note"] == 21):
                    visualization.current_color += 1
                    if(visualization.current_color > visualization.colorDictionary.number_of_colors - 1):
                        visualization.current_color = 0
                    print("Change color to => %s" %
                          visualization.colorDictionary.dictionary[visualization.current_color])

    def stripProcess(index, shared_list):
        print("STRIP PROCESS")
        config = shared_list[0]
        timeSinceProcessStart = shared_list[2]
        stripConfig = config["strips"][index]
        number_of_strips = len(stripConfig["strip_shapes"][0])
        strip_shape = stripConfig["strip_shapes"][0]
        print("shape", strip_shape)
        port = stripConfig["serial_port_name"]
        print("port", port)
        strip_mods = stripConfig["strip_mods"]
        print("mods", strip_mods)
        default_visualization_mod = stripConfig["active_visualizer"]
        print(default_visualization_mod)
        active_audio_channel = stripConfig["active_audio_channel"]
        print("active audio channel", active_audio_channel)
        audio_channel_number = len(shared_list[1])
        print("number of audio channels", audio_channel_number)

        midi_ports = config["midi_ports"]
        print("midi ports", midi_ports)
        associated_midi_channels = stripConfig["associated_midi_channels"]
        print("associated_midi_channels", associated_midi_channels)
        midi_notes = []
        midi_input_classes = []
        for midi_port in midi_ports:
            midi_input_classes.append(MidiInput(midi_port))

        total_pixel_number = 0
        for strip_length in strip_shape:
            total_pixel_number += strip_length
        print("pixels", total_pixel_number)

        visualization = Visualization(
            timeSinceProcessStart,
            default_visualization_mod=default_visualization_mod,
            total_pixel_number=total_pixel_number
        )
        pixelReshaper = PixelReshaper(
            total_pixel_number=total_pixel_number,
            strip_shape=strip_shape,
            default_mods=strip_mods
        )
        serialToArduinoLedStrip = SerialToArduinoLedStrip(
            total_pixel_number,
            port
        )
        serialToArduinoLedStrip.setup()

        print("Begin")

        while 1:
            midi_notes = []
            midi_notes_for_visualization = []
            midi_notes_for_changing_mode = []
            for i, midi_input_class in enumerate(midi_input_classes):
                midi_notes = midi_input_classes[i].getRawData()
                if(midi_notes):
                    for midi_note in midi_notes:
                        if(midi_note["port"] == "Ableton-virtual-midi-ouput ChangeMod"):
                            midi_notes_for_changing_mode.append(midi_note)
                        else :
                            for channel in associated_midi_channels:
                                if(midi_note["port"] == channel):
                                    midi_notes_for_visualization.append(midi_note)

            if(index == 0 and midi_notes_for_changing_mode != []):
                print(midi_notes_for_changing_mode)

            visualization.audio_data = shared_list[1][0]
            visualization.midi_notes = midi_notes_for_visualization
            handleChangeMod(midi_notes_for_changing_mode, active_audio_channel, audio_channel_number, visualization, pixelReshaper)

            serialToArduinoLedStrip.update(
                pixelReshaper.reshape(
                    visualization.drawFrame()
                )
            )
            # print(FPS.getFps())
            time.sleep(0.01)

    manager = multiprocessing.Manager()
    shared_list = manager.list()
    # Shared list :
    # 0 : Config
    # 1 : Audio datas
    # 2 : TimeSinceProcessStart
    shared_list.append(config.data)
    shared_list.append(np.tile(0.,(len(config.data["audio_ports"]), 24)))
    shared_list.append(TimeSinceProcessStart())

    number_of_strips = len(config.data["strips"])

    print("start")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(audioProcess, shared_list)
        for i in range(number_of_strips):
            executor.submit(stripProcess, i, shared_list)
