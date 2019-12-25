import numpy as np

def clampToNewRange(value, old_min, old_max, new_min, new_max):
    new_value = (((value - old_min) * (new_max - new_min)) // (old_max - old_min)) + new_min
    return new_value

def valueUpdater(old_value, value, max, increment):
    """ Wahou """
    new_value = old_value

    if(value * increment >= max):
        new_value += increment
        if(new_value >= max):
            new_value = 0
    else:
        new_value = value * increment

    return new_value

def logger(name, information):
    print("Strip " + name + " : ", end = "")
    print(information)


class ModSwitcher:

    def __init__(self, visualizer, config, index):

        self.config = config
        self.strip_config = config.strips[index]
        self.visualizer = visualizer

    def changeMod(self):
        if(self.midi_datas):
            for midi_data in self.midi_datas:
                if(midi_data["type"] == "note_on"):
                    mode = midi_data["note"]
                    velocity = midi_data["velocity"]
                    old_vizualizer_effect = self.strip_config.active_visualizer_effect
                    # VISUALIZATIONS EFFECTS
                    if(mode >= 0 and mode < 20) :

                        # SOUND BASED
                        if(mode == 0):
                            self.strip_config.active_visualizer_effect = "scroll"
                        elif(mode == 1):
                            self.strip_config.active_visualizer_effect = "energy"
                        elif(mode == 2):
                            self.visualizer.initVizualiser()
                            self.strip_config.active_visualizer_effect = "spectrum"
                        elif(mode == 3):
                            self.strip_config.active_visualizer_effect = "intensity_channels"

                        # MIDI BASED
                        elif(mode == 4):
                            self.strip_config.active_visualizer_effect = "piano"
                        elif(mode == 5):
                            self.strip_config.active_visualizer_effect = "piano2"
                        elif(mode == 6):
                            self.strip_config.active_visualizer_effect = "envelope"
                        elif(mode == 7):
                            print("Empty slot. This note is not assigned to an effect...")

                        # TIME BASED
                        elif(mode == 8):
                            self.visualizer.drawAlternateColors()
                            self.strip_config.active_visualizer_effect = "alternate_colors"
                        elif(mode == 9):
                            self.strip_config.active_visualizer_effect = "alternate_colors_for_shapes"
                        elif(mode == 10):
                            self.strip_config.active_visualizer_effect = "draw_line"
                        elif(mode == 11):
                           print("Empty slot. This note is not assigned to an effect...")

                        # GENERIC
                        elif(mode == 12):
                            self.strip_config.active_visualizer_effect = "full"
                            self.visualizer.old_full_intensity = 0
                        elif(mode == 13):
                            self.strip_config.active_visualizer_effect = "fadeToNothing"
                            self.visualizer.old_full_intensity = 1
                        elif(mode == 14):
                            self.strip_config.active_visualizer_effect = "clear"
                        elif(mode == 15):
                            self.strip_config.active_visualizer_effect = "fire"

                        # LOGGER
                        if(old_vizualizer_effect != self.strip_config.active_visualizer_effect):
                            message = "is changing viz effect to -> " + self.strip_config.active_visualizer_effect
                            logger(self.strip_config.name, message)

                    # MODIFIERS
                    if(mode >= 16 and mode <= 26) :

                        if(mode == 16):
                            self.strip_config.is_reverse = not self.strip_config.is_reverse
                            message = "is changing reverse mode to -> " + str(self.strip_config.is_reverse)
                            logger(self.strip_config.name, message)

                        elif(mode == 17):
                            self.strip_config.is_mirror = not self.strip_config.is_mirror
                            message = "is changing mirror mode to -> " + str(self.strip_config.is_mirror)
                            logger(self.strip_config.name, message)

                        elif(mode == 18):
                            self.strip_config.active_shape_index = valueUpdater(
                                self.strip_config.active_shape_index,
                                velocity,
                                self.strip_config.number_of_shapes,
                                1
                            )
                            number_of_pixels = self.strip_config.shapes[self.strip_config.active_shape_index].number_of_pixels
                            pixels = np.tile(.0, (3, number_of_pixels))
                            self.visualizer.initVizualiser()
                            self.visualizer.resetFrame()
                            self.visualizer.pixelReshaper.initActiveShape()

                            message = "is changing shape to -> " + str(self.strip_config.shapes[self.strip_config.active_shape_index].shape)
                            logger(self.strip_config.name, message)

                        elif(mode == 19):
                            self.strip_config.active_color_scheme_index = valueUpdater(
                                self.strip_config.active_color_scheme_index,
                                velocity,
                                self.strip_config.number_of_color_schemes,
                                1
                            )
                            message = "is changing color scheme to -> " + str(self.strip_config.color_schemes[self.strip_config.active_color_scheme_index])
                            logger(self.strip_config.name, message)

                        elif(mode == 20):

                            self.strip_config.time_interval = valueUpdater(
                                self.strip_config.time_interval,
                                velocity,
                                420,
                                5
                            )
                            message = "is changing time_interval to -> " + str(self.strip_config.time_interval)
                            logger(self.strip_config.name, message)

                        elif(mode == 21):
                            self.strip_config.active_audio_channel_index = valueUpdater(
                                self.strip_config.active_audio_channel_index,
                                velocity,
                                self.config.number_of_audio_ports,
                                1
                            )

                            message = "is changing audio port to -> " + str(self.config.audio_ports[self.strip_config.active_audio_channel_index].name)
                            logger(self.strip_config.name, message)


                        elif(mode == 22):
                            self.strip_config.max_brightness = valueUpdater(
                                self.strip_config.max_brightness,
                                velocity,
                                255,
                                2
                            )

                            message = "is changing max_brightness to -> " + str(self.strip_config.max_brightness)
                            logger(self.strip_config.name, message)

                        elif(mode == 23):
                            self.strip_config.chunk_size = valueUpdater(
                                self.strip_config.chunk_size,
                                velocity,
                                50,
                                2
                            )
                            logger(self.strip_config.name, "is changing chunk size to " + str(self.strip_config.chunk_size))


                        # Old reset frame. Not used anymmore
                        #
                        # elif(mode == 24):
                        #     self.visualizer.resetFrame()
                        #     self.visualizer.pixelReshaper.resetStrips()
                        #     logger(self.strip_config.name, "is reseting his frame")
