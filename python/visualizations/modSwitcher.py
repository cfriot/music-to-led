import numpy as np

class ModSwitcher:
    def __init__(self, visualizer, serialToArduinoLedStrip, config, index):

        self.config = config
        self.strip_config = config.strips[index]
        self.visualizer = visualizer
        self.serialToArduinoLedStrip = serialToArduinoLedStrip

    def changeMod(self):
        if(self.midi_datas):
            for midi_data in self.midi_datas:
                if(midi_data["type"] == "note_on"):
                    mode = midi_data["note"]
                    if(mode == 0):
                        self.strip_config.active_visualizer_effect = "scroll"
                        self.visualizer.resetFrame()
                        self.visualizer.visualizer_effect = self.visualizer.visualizeScroll
                        print("Change viz to => scroll")
                    elif(mode == 2):
                        self.strip_config.active_visualizer_effect = "energy"
                        self.visualizer.resetFrame()
                        self.visualizer.visualizer_effect = self.visualizer.visualizeEnergy
                        print("Change viz to => energy")
                    elif(mode == 4):
                        self.strip_config.active_visualizer_effect = "piano"
                        self.visualizer.resetFrame()
                        self.visualizer.visualizer_effect = self.visualizer.visualizePiano
                        print("Change viz to => piano")
                    elif(mode == 5):
                        self.strip_config.active_visualizer_effect = "full"
                        self.visualizer.resetFrame()
                        self.visualizer.old_full_intensity = 0
                        self.visualizer.visualizer_effect = self.visualizer.visualizeFull
                        print("Change viz to => full")
                    elif(mode == 7):
                        self.strip_config.active_visualizer_effect = "nothing"
                        self.visualizer.old_full_intensity = 1
                        self.visualizer.visualizer_effect = self.visualizer.visualizeNothing
                        print("Change viz to => nothing")
                    elif(mode == 9):
                        self.strip_config.active_visualizer_effect = "intensity_channels"
                        self.visualizer.resetFrame()
                        self.visualizer.visualizer_effect = self.visualizer.visualizeIntensityChannels
                        print("Change viz to => intensityChannels")
                    elif(mode == 11):
                        self.strip_config.active_visualizer_effect = "visualize_alternate_colors"
                        self.visualizer.resetFrame()
                        self.visualizer.visualizer_effect = self.visualizer.visualizeAlternateColors
                        print("Change viz to => alternateColors")
                    elif(mode == 12):
                        self.strip_config.active_visualizer_effect = "visualize_neon_fade_in"
                        self.visualizer.resetFrame()
                        self.visualizer.timeSinceStart.restart()
                        self.visualizer.visualizer_effect = self.visualizer.visualizeNeonFadeIn
                        print("Change viz to => neonFadeIn")
                    elif(mode == 14):
                        self.strip_config.is_reverse = not self.strip_config.is_reverse
                        print("Change mod to reverse mode => %s" %
                              self.strip_config.is_reverse)
                    elif(mode == 16):
                        self.strip_config.is_mirror = not self.strip_config.is_mirror
                        print("Change mod to mirror mode => %s" %
                              self.strip_config.is_mirror)
                    elif(mode == 17):
                        self.strip_config.active_color_scheme_index += 1
                        if(self.strip_config.active_color_scheme_index >= self.strip_config.number_of_color_schemes):
                            self.strip_config.active_color_scheme_index = 0
                        print("Change color to => %s" %
                              self.strip_config.color_schemes[self.strip_config.active_color_scheme_index])
                    elif(mode == 19):
                        self.strip_config.active_audio_channel_index += 1
                        if(self.strip_config.active_audio_channel_index >= self.config.number_of_audio_ports):
                            self.strip_config.active_audio_channel_index = 0
                            self.visualizer.active_audio_channel_index = self.strip_config.active_audio_channel_index
                        print("Change audio mod to => %s" %
                              self.strip_config.active_audio_channel_index)
                    elif(mode == 21):
                        self.strip_config.active_shape_index += 1
                        if(self.strip_config.active_shape_index >= self.strip_config.number_of_shapes):
                            self.strip_config.active_shape_index = 0
                        number_of_pixels = self.strip_config.shapes[self.strip_config.active_shape_index].number_of_pixels
                        pixels = np.tile(.0, (3, number_of_pixels))
                        print(number_of_pixels)
                        self.serialToArduinoLedStrip.update(pixels)
                        self.visualizer.number_of_pixels = number_of_pixels
                        self.visualizer.initVizualiser()
                        self.visualizer.resetFrame()
                        self.visualizer.pixelReshaper.initActiveShape()
                        print("Change shape to =>", self.strip_config.shapes[self.strip_config.active_shape_index].shape)
                    elif(mode == 23):
                        self.strip_config.bpm += 10
                        if(self.strip_config.bpm >= 320):
                            self.strip_config.bpm = 0
                        print("Change bpm to =>", self.strip_config.bpm)
