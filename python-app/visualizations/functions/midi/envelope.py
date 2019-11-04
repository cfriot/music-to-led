import numpy as np

def clampToNewRange(value, old_min, old_max, new_min, new_max):
    new_value = (((value - old_min) * (new_max - new_min)) // (old_max - old_min)) + new_min
    return new_value

def getValueFromPercentage(value, percentage):
    return value / 100 * percentage

class Envelope():

    def initEnvelope():
        notes_on = []

    def visualizeEnvelope(self):
        """Envelope midi visualizer"""

        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        which_color = 0
        number_of_notes = len(self.midi_datas)
        r = 0
        g = 0
        b = 0
        for midi_note in self.midi_datas:
            # print(midi_note)
            if(midi_note["type"] == "pitchwheel"):
                pitch = midi_note["pitch"]

                value = clampToNewRange(pitch, -8192, 8191, 0, 100)

                r = getValueFromPercentage(color_scheme[which_color][0], value)
                g = getValueFromPercentage(color_scheme[which_color][1], value)
                b = getValueFromPercentage(color_scheme[which_color][2], value)

        self.pixels[0] = r
        self.pixels[1] = g
        self.pixels[2] = b

        return self.pixelReshaper.reshapeFromPixels(self.pixels)
