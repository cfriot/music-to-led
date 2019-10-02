from __future__ import print_function
from __future__ import division
import time
import os
import sys

import numpy as np


class PixelReshaper:

    def __init__(self, total_pixel_number=60, strip_shape=[30, 30], default_mods={"is_full_strip": False, "is_reverse": False, "is_mirror": False}):

        self.total_pixel_number = total_pixel_number
        self.number_of_strips = len(strip_shape)
        self.pixels = np.tile(.0, (3, self.total_pixel_number))
        self.strip_shape = strip_shape
        self.strips = []
        for i, strip_length in enumerate(strip_shape):
            self.strips.append([])
            self.strips[i] = np.tile(.0, (3, strip_length))

        self.is_reverse = default_mods["is_reverse"]
        self.is_full_strip = default_mods["is_full_strip"]
        self.is_mirror = default_mods["is_mirror"]

    # RESET PIXELS #####
    def concatenatePixels(self, strips):
        """Concatenate the x strips into 1"""
        tmp = [[], [], []]

        for i, strip_length in enumerate(self.strip_shape):
            tmp[0] = np.concatenate((tmp[0], strips[i][0]), axis=0)
            tmp[1] = np.concatenate((tmp[1], strips[i][1]), axis=0)
            tmp[2] = np.concatenate((tmp[2], strips[i][2]), axis=0)

        return tmp

    def splitForStrips(self, strips, pixels):
        """Split pixels to respect the shape"""
        # print("pixels", pixels)
        for i, strip_length in enumerate(self.strip_shape):
            if(self.is_reverse and not self.is_mirror):
                strips[i] = pixels[:, self.total_pixel_number - strip_length:]
            elif(self.is_mirror and not self.is_reverse):
                center = self.total_pixel_number // 2
                center_of_strip = strip_length // 2
                strips[i] = pixels[
                    :,
                    center - center_of_strip:
                    center + center_of_strip
                ]
            elif(self.is_mirror and self.is_reverse):

                tmp = pixels[:, :strip_length // 2]
                tmp2 = pixels[:, self.total_pixel_number - strip_length // 2:]
                strips[i] = np.concatenate((tmp, tmp2), axis=1)
            else:
                strips[i][0] = np.resize(pixels[0], strip_length)
                strips[i][1] = np.resize(pixels[1], strip_length)
                strips[i][2] = np.resize(pixels[2], strip_length)
            # print("strips", i, strips[i])
        return self.concatenatePixels(strips)

    def reversePixels(self, pixels):
        """Reverse pixels"""
        pixels[0] = list(reversed(pixels[0]))
        pixels[1] = list(reversed(pixels[1]))
        pixels[2] = list(reversed(pixels[2]))
        return pixels

    def mirrorPixels(self, pixels, number_of_pixels):
        """Mirror pixels"""
        if(self.is_reverse):
            tmp = np.copy(pixels[:, number_of_pixels // 2:])
            return np.concatenate((tmp[:, ::-1], tmp), axis=1)
        else:
            tmp = np.copy(pixels[:, :number_of_pixels // 2])
            return np.concatenate((tmp[:, ::-1], tmp), axis=1)

    # DRAW FRAME #####
    def reshape(self, pixels):

        tmp_p = np.copy(pixels)

        if(self.is_reverse):
            tmp_p = self.reversePixels(tmp_p)

        if(self.is_mirror):
            tmp_p = self.mirrorPixels(tmp_p, self.total_pixel_number)

        if(self.is_full_strip):
            return tmp_p
        else:
            return self.splitForStrips(self.strips, tmp_p)


if __name__ == "__main__":

    from serialToArduinoLedStrip import SerialToArduinoLedStrip

    print('Starting PixelReshaper test on ports :')
    print(SerialToArduinoLedStrip.listAvailableUsbSerialPorts())
    ports = SerialToArduinoLedStrip.listAvailableUsbSerialPorts()

    number_of_pixels = 16

    pixelReshaper = PixelReshaper(
        total_pixel_number=number_of_pixels,
        strip_shape=[4, 8, 4],
        default_mods={"is_full_strip": False,
                      "is_reverse": False, "is_mirror": True}
    )

    pixels = np.tile(0., (3, number_of_pixels))
    pixels[0, 0] = 255
    pixels[1, 1] = 255

    pixels[0, number_of_pixels - 1] = 255
    pixels[1, number_of_pixels - 2] = 255

    tmp = pixelReshaper.reshape(pixels)
    serialToArduinoLedStrip = SerialToArduinoLedStrip(
        number_of_pixels, ports)
    serialToArduinoLedStrip.setup()

    while True:
        pixels = np.roll(pixels, 1, axis=1)
        tmp = pixelReshaper.reshape(pixels)
        serialToArduinoLedStrip.update(tmp)
        time.sleep(.2)
