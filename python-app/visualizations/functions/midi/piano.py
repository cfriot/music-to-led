import numpy as np
import time

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

def applyGradientDecrease(pixels):
    for colorChannel in pixels:
        for i, pixel in enumerate(colorChannel):
            pixel = pixel - i * 10

def shiftPixels(pixels):
    pixels[0] = np.roll(pixels[0], 1)
    pixels[1] = np.roll(pixels[1], 1)
    pixels[2] = np.roll(pixels[2], 1)

def shiftPixelsSmoothly(pixels):
    pixels[0] = shiftArray(pixels[0], 1, 5)
    pixels[1] = shiftArray(pixels[1], 1, 5)
    pixels[2] = shiftArray(pixels[2], 1, 5)


def putPixel(strip, ledIndex, r, g, b, velocity):
    # print(r / 127 * (velocity + 1))
    strip[0][ledIndex] = r / 127 * (velocity + 1)
    strip[1][ledIndex] = g / 127 * (velocity + 1)
    strip[2][ledIndex] = b / 127 * (velocity + 1)

class Piano():

    def initPiano(self):
        self.notes_on = []
        self.pitch_bend = 0
        self.value = 0

    def visualizePiano(self):
        """Piano midi visualizer"""

        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        for midi_note in self.midi_datas:
            if(midi_note["type"] == "note_on" and midi_note["velocity"] > 0):
                self.notes_on.append(midi_note)
            if(midi_note["type"] == "note_off" or (midi_note["type"] == "note_on" and midi_note["velocity"] == 0)):
                for i, note_on in enumerate(self.notes_on):
                    if(note_on["note"] == midi_note["note"]):
                        del self.notes_on[i]

        if(len(self.notes_on) > 0):
            which_color = 0
            which_color = len(self.notes_on)

            if(which_color >= len(color_scheme)):
                which_color = 0

            r = color_scheme[which_color][0]
            g = color_scheme[which_color][1]
            b = color_scheme[which_color][2]
            putPixel(self.pixels, 0, r, g, b, self.notes_on[len(self.notes_on) - 1]["velocity"] * 2)
        else:
            putPixel(self.pixels, 0, 0, 0, 0, 100)

        shiftPixelsSmoothly(self.pixels)
        # applyGradientDecrease(self.pixels)
        # print(self.pixels)
        # time.sleep(.028)
        return self.pixelReshaper.reshapeFromPixels(self.pixels)
