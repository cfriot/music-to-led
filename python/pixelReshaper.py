from __future__ import print_function
from __future__ import division
import time
import os
import sys

import numpy as np


class PixelReshaper:

    def __init__(self, total_pixel_number=60, strips_shape=[30, 30], default_mods={"is_full_strip": False, "is_reverse": False, "is_mirror": False}):

        self.total_pixel_number = total_pixel_number
        self.number_of_strips = len(strips_shape)
        self.pixels = np.tile(.0, (3, self.total_pixel_number))
        self.strips_shape = strips_shape
        self.strips = []
        for i, strip_length in enumerate(strips_shape):
            self.strips.append([])
            self.strips[i] = np.tile(.0, (3, strip_length))

        self.is_reverse = default_mods["is_reverse"]
        self.is_full_strip = default_mods["is_full_strip"]
        self.is_mirror = default_mods["is_mirror"]

    # RESET PIXELS #####
    def concatenatePixels(self, strips):
        """Concatenate the x strips into 1"""
        tmp = [[], [], []]

        for i, strip_length in enumerate(self.strips_shape):
            tmp[0] = np.concatenate((tmp[0], strips[i][0]), axis=0)
            tmp[1] = np.concatenate((tmp[1], strips[i][1]), axis=0)
            tmp[2] = np.concatenate((tmp[2], strips[i][2]), axis=0)

        return tmp

    def splitForStrips(self, strips, pixels, is_reverse):
        """Split pixels to respect the shape"""
        for i, strip_length in enumerate(self.strips_shape):
            if(is_reverse):
                strips[i][0] = pixels[0][config.STRIPS_INDEXES[2] + 15:]
                strips[i][1] = pixels[1][config.STRIPS_INDEXES[2] + 15:]
                strips[i][2] = pixels[2][config.STRIPS_INDEXES[2] + 15:]
            else:
                strips[i][0] = np.resize(pixels[0], strip_length)
                strips[i][1] = np.resize(pixels[1], strip_length)
                strips[i][2] = np.resize(pixels[2], strip_length)

        return self.concatenatePixels(strips)

    def reversePixels(self, pixels):
        """Reverse pixels"""
        pixels[0] = list(reversed(pixels[0]))
        pixels[1] = list(reversed(pixels[1]))
        pixels[2] = list(reversed(pixels[2]))
        return pixels

    def mirrorPixels(self, pixels):
        """Mirror pixels"""
        tmp = np.copy(pixels[:, :self.total_pixel_number // 2])
        return np.concatenate((tmp[:, ::-1], tmp), axis=1)

    # DRAW FRAME #####
    def reshape(self, pixels):

        tmp_p = np.copy(pixels)

        if(self.is_reverse):
            tmp_p = self.reversePixels(tmp_p)

        if(self.is_mirror):
            tmp_p = self.mirrorPixels(tmp_p)

        if(self.is_full_strip):
            return tmp_p
        else:
            return self.splitForStrips(self.strips, tmp_p, self.is_reverse)
