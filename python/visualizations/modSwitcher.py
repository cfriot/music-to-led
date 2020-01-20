import numpy as np

from copy import deepcopy


class ModSwitcher:

    def __init__(self, visualizer, config, index, verbose):

        self.config = config
        self.strip_config = config.strips[index]
        self.active_state = self.strip_config.active_state

        self.visualizer = visualizer
        self.verbose = verbose

    def logger(self, name, information):
        if(self.verbose):
            print("Strip " + name + " : ", end = "")
            print(information)

    @staticmethod
    def valueUpdater(old_value, value, max, increment):
        new_value = old_value

        if(value * increment >= max):
            new_value += increment
            if(new_value >= max):
                new_value = 0
        else:
            new_value = value * increment

        return new_value


    def changeMod(self):
        if(self.midi_datas):
            for midi_data in self.midi_datas:
                if(midi_data["type"] == "note_on"):
                    mode = midi_data["note"]
                    velocity = midi_data["velocity"]
                    old_vizualizer_effect = self.active_state.active_visualizer_effect
                    # VISUALIZATIONS EFFECTS
                    if(mode >= 0 and mode < 20) :

                        # SOUND BASED
                        if(mode == 0):
                            self.active_state.active_visualizer_effect = "scroll"
                        elif(mode == 1):
                            self.active_state.active_visualizer_effect = "energy"
                        elif(mode == 2):
                            self.active_state.active_visualizer_effect = "channel_intensity"
                        elif(mode == 3):
                            self.active_state.active_visualizer_effect = "channel_flash"

                        # MIDI BASED
                        elif(mode == 4):
                            self.active_state.active_visualizer_effect = "piano_scroll"
                        elif(mode == 5):
                            self.active_state.active_visualizer_effect = "piano_note"
                        elif(mode == 6):
                            self.active_state.active_visualizer_effect = "pitchwheel_flash"
                        elif(mode == 7):
                            self.logger(self.strip_config.name, "Empty slot. This note is not assigned to any effect...")

                        # TIME BASED
                        elif(mode == 8):
                            self.active_state.active_visualizer_effect = "alternate_color_chunks"
                        elif(mode == 9):
                            self.active_state.active_visualizer_effect = "alternate_color_shapes"
                        elif(mode == 10):
                            self.active_state.active_visualizer_effect = "transition_color_shapes"
                        elif(mode == 11):
                            self.active_state.active_visualizer_effect = "draw_line"
                        # GENERIC
                        elif(mode == 12):
                            self.active_state.active_visualizer_effect = "full_color"
                        elif(mode == 13):
                            self.active_state.active_visualizer_effect = "fade_out"
                        elif(mode == 14):
                            self.active_state.active_visualizer_effect = "clear_frame"
                        elif(mode == 15):
                            self.active_state.active_visualizer_effect = "fire"

                        # LOGGER
                        if(old_vizualizer_effect != self.active_state.active_visualizer_effect):
                            message = "is changing viz effect to -> " + self.active_state.active_visualizer_effect
                            self.logger(self.strip_config.name, message)

                    # MODIFIERS
                    if(mode >= 16 and mode <= 26) :

                        if(mode == 16):
                            self.active_state.is_reverse = not self.active_state.is_reverse
                            message = "is changing reverse mode to -> " + str(self.active_state.is_reverse)
                            self.logger(self.strip_config.name, message)

                        elif(mode == 17):
                            self.active_state.is_mirror = not self.active_state.is_mirror
                            message = "is changing mirror mode to -> " + str(self.active_state.is_mirror)
                            self.logger(self.strip_config.name, message)

                        elif(mode == 18):
                            self.active_state.active_shape_index = self.valueUpdater(
                                self.active_state.active_shape_index,
                                velocity,
                                self.active_state.number_of_shapes,
                                1
                            )
                            message = "is changing shape to -> " + str(self.active_state.shapes[self.active_state.active_shape_index].shape)
                            self.logger(self.strip_config.name, message)

                        elif(mode == 19):
                            self.active_state.active_color_scheme_index = self.valueUpdater(
                                self.active_state.active_color_scheme_index,
                                velocity,
                                self.active_state.number_of_color_schemes,
                                1
                            )
                            message = "is changing color scheme to -> " + str(self.active_state.color_schemes[self.active_state.active_color_scheme_index])
                            self.logger(self.strip_config.name, message)

                        elif(mode == 20):

                            self.active_state.time_interval = self.valueUpdater(
                                self.active_state.time_interval,
                                velocity,
                                420,
                                5
                            )
                            message = "is changing time_interval to -> " + str(self.active_state.time_interval)
                            self.logger(self.strip_config.name, message)

                        elif(mode == 21):
                            self.active_state.active_audio_channel_index = self.valueUpdater(
                                self.active_state.active_audio_channel_index,
                                velocity,
                                self.config.number_of_audio_ports,
                                1
                            )

                            message = "is changing audio port to -> " + str(self.config.audio_ports[self.active_state.active_audio_channel_index].name)
                            self.logger(self.strip_config.name, message)

                        elif(mode == 22):
                            self.active_state.max_brightness = self.valueUpdater(
                                self.active_state.max_brightness,
                                velocity,
                                255,
                                2
                            )

                            message = "is changing max_brightness to -> " + str(self.active_state.max_brightness)
                            self.logger(self.strip_config.name, message)

                        elif(mode == 23):
                            self.active_state.chunk_size = self.valueUpdater(
                                self.active_state.chunk_size,
                                velocity,
                                50,
                                2
                            )
                            self.logger(self.strip_config.name, "is changing chunk size to " + str(self.active_state.chunk_size))

                        elif(mode == 24):
                            self.strip_config.active_state_index = self.valueUpdater(
                                self.strip_config.active_state_index,
                                velocity,
                                len(self.config.states),
                                1
                            )

                            # self.strip_config.active_state = self.config.states[self.strip_config.active_state_index].copy()
                            self.strip_config.active_state = deepcopy(self.config.states[self.strip_config.active_state_index])
                            self.active_state = self.strip_config.active_state

                            self.visualizer.initVizualiser()

                            self.logger(self.strip_config.name, "is changing state for " + self.config.states[self.strip_config.active_state_index].name)

        return self.strip_config
