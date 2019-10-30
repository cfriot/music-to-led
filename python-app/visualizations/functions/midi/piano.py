import numpy as np

def shiftArray(arr, num, decrease_amount):
    value = arr[0] - decrease_amount
    if(value < 0):
        value = 0
    arr = np.roll(arr, num)
    if num < 0:
        arr[num:] = value
    elif num > 0:
        arr[:num] = value
    return arr

def shiftPixelsSmoothly(pixels):
    pixels[0] = shiftArray(pixels[0], 1, 50)
    pixels[1] = shiftArray(pixels[1], 1, 50)
    pixels[2] = shiftArray(pixels[2], 1, 50)


def putPixel(strip, ledIndex, r, g, b, velocity):
    # print(r / 127 * (velocity + 1))
    strip[0][ledIndex] = r / 127 * (velocity + 1)
    strip[1][ledIndex] = g / 127 * (velocity + 1)
    strip[2][ledIndex] = b / 127 * (velocity + 1)

class Piano():

    def initPiano(self):
        self.notes_on = []

    def visualizePiano(self):
        """Piano midi visualizer"""

        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        for midi_note in self.midi_datas:
            if(midi_note["type"] == "note_on"):
                self.notes_on.append(midi_note["note"])
            if(midi_note["type"] == "note_off"):
                if midi_note["note"] in self.notes_on: self.notes_on.remove(midi_note["note"])

        if(len(self.notes_on) > 0):
            which_color = 0
            which_color = len(self.notes_on)

            if(which_color >= len(color_scheme)):
                which_color = 0

            r = color_scheme[which_color][0]
            g = color_scheme[which_color][1]
            b = color_scheme[which_color][2]
            putPixel(self.pixels, 0, r, g, b, 100)
        else:
            putPixel(self.pixels, 0, 0, 0, 0, 100)

        # print(self.pixels[0][1], len(self.notes_on), self.notes_on)
        shiftPixelsSmoothly(self.pixels)
        return self.pixelReshaper.reshapeFromPixels(self.pixels)

    # def visualizePiano(self):
    #     """Piano midi visualizer"""
    #
    #     color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]
    #
    #     which_color = 0
    #     number_of_notes = len(self.midi_datas)
    #     for midi_note in self.midi_datas:
    #         if(midi_note["type"] == "note_on"):
    #
    #             real_note = midi_note["note"]
    #
    #             which_color = number_of_notes
    #
    #             if(which_color >= len(color_scheme)):
    #                 which_color = 0
    #
    #             r = color_scheme[which_color][0]
    #             g = color_scheme[which_color][1]
    #             b = color_scheme[which_color][2]
    #             putPixel(self.pixels, 0, r, g, b, midi_note["velocity"])
    #     shiftPixelsSmoothly(self.pixels)
    #
    #     return self.pixelReshaper.reshapeFromPixels(self.pixels)
