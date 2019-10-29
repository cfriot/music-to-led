import numpy as np

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
                    if(mode >= 0 and mode <= 15) :

                        # SOUND BASED
                        if(mode == 0):
                            self.strip_config.active_visualizer_effect = "scroll"
                        elif(mode == 1):
                            self.strip_config.active_visualizer_effect = "energy"
                        elif(mode == 2):
                            self.strip_config.active_visualizer_effect = "intensity_channels"
                        elif(mode == 3):
                            self.strip_config.active_visualizer_effect = "spectrum"

                        # MIDI BASED
                        elif(mode == 5):
                            self.strip_config.active_visualizer_effect = "piano"
                        elif(mode == 6):
                            self.strip_config.active_visualizer_effect = "piano2"
                        elif(mode == 7):
                            self.strip_config.active_visualizer_effect = "envelope"

                        # BPM BASED
                        elif(mode == 9):
                            self.visualizer.alternate_colors_size = valueUpdater(
                                self.visualizer.alternate_colors_size,
                                velocity,
                                50,
                                2
                            )
                            self.visualizer.drawAlternateColors()
                            self.strip_config.active_visualizer_effect = "alternate_colors"
                        elif(mode == 10):
                            self.strip_config.active_visualizer_effect = "alternate_colors_full"
                        elif(mode == 11):
                            self.strip_config.active_visualizer_effect = "alternate_colors_for_shapes"

                        # GENERIC
                        elif(mode == 13):
                            self.strip_config.active_visualizer_effect = "full"
                            self.visualizer.old_full_intensity = 0
                        elif(mode == 14):
                            self.strip_config.active_visualizer_effect = "nothing"
                            self.visualizer.old_full_intensity = 1

                        if(old_vizualizer_effect != self.strip_config.active_visualizer_effect):
                            message = "is changing viz effect to -> " + self.strip_config.active_visualizer_effect
                            logger(self.strip_config.name, message)

                    if(mode == 16):
                        self.visualizer.resetFrame()
                        self.visualizer.pixelReshaper.resetStrips()
                        logger(self.strip_config.name, "is reseting his frame")

                    # MODIFIERS
                    if(mode > 16 and mode <= 25) :

                        if(mode == 18):
                            self.strip_config.is_reverse = not self.strip_config.is_reverse
                            message = "is changing reverse mode to -> " + str(self.strip_config.is_reverse)
                            logger(self.strip_config.name, message)

                        elif(mode == 19):
                            self.strip_config.is_mirror = not self.strip_config.is_mirror
                            message = "is changing mirror mode to -> " + str(self.strip_config.is_mirror)
                            logger(self.strip_config.name, message)

                        # VELOCITY BASED MODIFIERS
                        elif(mode == 21):
                            self.strip_config.active_color_scheme_index = valueUpdater(
                                self.strip_config.active_color_scheme_index,
                                velocity,
                                self.strip_config.number_of_color_schemes,
                                1
                            )
                            message = "is changing color scheme to -> " + str(self.strip_config.color_schemes[self.strip_config.active_color_scheme_index])
                            logger(self.strip_config.name, message)

                        elif(mode == 22):
                            self.strip_config.active_shape_index = valueUpdater(
                                self.strip_config.active_shape_index,
                                velocity,
                                self.strip_config.number_of_shapes,
                                1
                            )
                            number_of_pixels = self.strip_config.shapes[self.strip_config.active_shape_index].number_of_pixels
                            pixels = np.tile(.0, (3, number_of_pixels))
                            # self.serialOutput.update(pixels)
                            self.visualizer.initVizualiser()
                            self.visualizer.resetFrame()
                            self.visualizer.pixelReshaper.initActiveShape()

                            message = "is changing shape to -> " + str(self.strip_config.shapes[self.strip_config.active_shape_index].shape)
                            logger(self.strip_config.name, message)

                        elif(mode == 23):

                            self.strip_config.bpm = valueUpdater(
                                self.strip_config.bpm,
                                velocity,
                                420,
                                5
                            )
                            message = "is changing bpm to -> " + str(self.strip_config.bpm)
                            logger(self.strip_config.name, message)

                        elif(mode == 24):
                            self.strip_config.active_audio_channel_index = valueUpdater(
                                self.strip_config.active_audio_channel_index,
                                velocity,
                                self.config.number_of_audio_ports,
                                1
                            )

                            message = "is changing audio mod to -> " + str(self.config.audio_ports[self.strip_config.active_audio_channel_index].name)
                            logger(self.strip_config.name, message)
