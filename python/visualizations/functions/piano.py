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
    pixels[0] = shiftArray(pixels[0], 1, 100)
    pixels[1] = shiftArray(pixels[1], 1, 100)
    pixels[2] = shiftArray(pixels[2], 1, 100)


def putPixel(strip, ledIndex, r, g, b, velocity):
    strip[0][ledIndex] += r / 100 * velocity
    strip[1][ledIndex] += g / 100 * velocity
    strip[2][ledIndex] += b / 100 * velocity


def octaveColor(strip, note):
    if note >= 0 and note <= 11:
        putPixel(strip, 0, 255, 255, 255)
    elif note >= 12 and note <= 23:
        putPixel(strip, 0, 255, 255, 255)
    elif note >= 24 and note <= 35:
        putPixel(strip, 0, 255, 255, 255)
    elif note >= 36 and note <= 47:
        putPixel(strip, 0, 255, 255, 255)
    elif note >= 48 and note <= 60:
        putPixel(strip, 0, 255, 255, 255)

class Piano():

    def visualizePiano(self):
        """Piano"""

        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        for midi_note in self.midi_datas:
            real_note = midi_note["note"]
            r = color_scheme[0][0]
            g = color_scheme[0][1]
            b = color_scheme[0][2]
            putPixel(self.pixels, 0, r, g, b, midi_note["velocity"])
        shiftPixelsSmoothly(self.pixels)

        return self.pixelReshaper.reshape(self.pixels)
