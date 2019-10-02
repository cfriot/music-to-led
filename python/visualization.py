from __future__ import print_function
from __future__ import division
import time
import os
import sys

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

import config
from colorDictionary import ColorDictionary
from audioFilters.dsp import *


def lerp(start, end, d):
    return start * (1 - d) + end * d


def memoize(function):
    """Provides a decorator for memoizing functions"""
    from functools import wraps
    memo = {}

    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper


@memoize
def normalizedLinspace(size):
    return np.linspace(0, 1, size)


def interpolate(y, new_length):
    """Intelligently resizes the array by linearly interpolating the values

    Parameters
    ----------
    y : np.array
        Array that should be resized

    new_length : int
        The length of the new interpolated array

    Returns
    -------
    z : np.array
        New array with length of new_length that contains the interpolated
        values of y.
    """
    if len(y) == new_length:
        return y
    x_old = normalizedLinspace(len(y))
    x_new = normalizedLinspace(new_length)
    z = np.interp(x_new, x_old, y)
    return z

# PIANO PART


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


def putPixel(strip, ledIndex, r, g, b):
    strip[0][ledIndex] += r
    strip[1][ledIndex] += g
    strip[2][ledIndex] += b


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


class Visualization:

    def __init__(self, timeSinceProcessStart, total_pixel_number=60, default_visualization_mod="scroll"):

        self.total_pixel_number = total_pixel_number
        self.pixels = np.tile(.0, (3,
                                   self.total_pixel_number))
        self.prev_spectrum = np.tile(0.01, self.total_pixel_number // 2)

        self.audio_data = []
        self.midi_notes = []

        self.colorDictionary = ColorDictionary()
        self.current_color = 0

        self.gain = ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                              alpha_decay=0.001, alpha_rise=0.99)
        self.p_filt = ExpFilter(np.tile(1, (3, self.total_pixel_number)),
                                alpha_decay=0.1, alpha_rise=0.99)

        self.r_filt = ExpFilter(np.tile(0.01, self.total_pixel_number // 2),
                                alpha_decay=0.2, alpha_rise=0.99)
        self.g_filt = ExpFilter(np.tile(0.01, self.total_pixel_number // 2),
                                alpha_decay=0.05, alpha_rise=0.3)
        self.b_filt = ExpFilter(np.tile(0.01, self.total_pixel_number // 2),
                                alpha_decay=0.1, alpha_rise=0.5)
        self.common_mode = ExpFilter(np.tile(0.01, self.total_pixel_number // 2),
                                     alpha_decay=0.99, alpha_rise=0.01)

        self.old_full_intensity = 0
        self.old_intensity_bounce = 0

        self.timeSinceProcessStart = timeSinceProcessStart

        self.is_monochrome = False
        self.active_mod = default_visualization_mod
        self.visualizationEffect = self.visualizeScroll

    # RESET FRAME #####
    def resetFrame(self):
        self.pixels = np.tile(0., (3, self.total_pixel_number))

    # DRAW FRAME #####
    def drawFrame(self):
        self.visualizationEffect()
        return self.pixels

    # VISUALIZE FULL #####
    def visualizeFull(self):
        self.pixels[0] = lerp(self.pixels[0], 255.0, self.old_full_intensity)
        self.pixels[1] = lerp(self.pixels[1], 255.0, self.old_full_intensity)
        self.pixels[2] = lerp(self.pixels[2], 255.0, self.old_full_intensity)
        self.pixels = np.clip(self.pixels, 0, 75)
        if(self.old_full_intensity < 1):
            self.old_full_intensity += 0.01

    # VISUALIZE NOTHING #####
    def visualizeNothing(self):
        self.pixels[0] = self.pixels[0] * self.old_full_intensity
        self.pixels[1] = self.pixels[1] * self.old_full_intensity
        self.pixels[2] = self.pixels[2] * self.old_full_intensity
        self.pixels = np.clip(self.pixels, 0, 75)
        if(self.old_full_intensity > 0):
            self.old_full_intensity -= 0.01

    # VISUALIZE AlternateColors #####
    def visualizeAlternateColors(self):
        """Effect that alternate two colors moving forward"""
        size = 10
        colors = [
            [0, 0, 0],
            self.colorDictionary.dictionary[self.current_color]
        ]
        which_color = 0
        for i in range(self.total_pixel_number):
            if(i % size == 0):
                if(which_color == 1):
                    which_color = 0
                else:
                    which_color = 1
            self.pixels[0][i] = colors[which_color][0]
            self.pixels[1][i] = colors[which_color][1]
            self.pixels[2][i] = colors[which_color][2]
        self.pixels = np.roll(
            self.pixels, self.timeSinceProcessStart.getMs(), axis=1)

    # VISUALIZE SCROLL #####
    def visualizeScroll(self):
        """Effect that originates in the center and scrolls outwards"""
        self.audio_data = self.audio_data**2.0
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        self.audio_data *= 255.0

        if(self.is_monochrome):
            value = (int(np.max(self.audio_data[:len(self.audio_data) // 3])) + int(np.max(self.audio_data[len(
                self.audio_data) // 3: 2 * len(self.audio_data) // 3])) + int(np.max(self.audio_data[2 * len(self.audio_data) // 3:]))) // 5
            self.pixels[:, 1:] = self.pixels[:, :-1]
            self.pixels *= 0.98
            self.pixels = gaussian_filter1d(self.pixels, sigma=0.7)
            self.pixels[0, 0] = value * \
                self.colorDictionary.dictionary[self.current_color][0]
            self.pixels[1, 0] = value * \
                self.colorDictionary.dictionary[self.current_color][1]
            self.pixels[2, 0] = value * \
                self.colorDictionary.dictionary[self.current_color][2]
        else:
            r = int(np.max(self.audio_data[:len(self.audio_data) // 3]))
            g = int(np.max(
                self.audio_data[len(self.audio_data) // 3: 2 * len(self.audio_data) // 3]))
            b = int(np.max(self.audio_data[2 * len(self.audio_data) // 3:]))
            self.pixels[:, 1:] = self.pixels[:, :-1]
            self.pixels *= 0.98
            self.pixels = gaussian_filter1d(self.pixels, sigma=0.7)
            self.pixels[0, 0] = r
            self.pixels[1, 0] = g
            self.pixels[2, 0] = b

    # INTENSITY BOUNCE VIZ #####
    def visualizeIntensityBounce(self):
        """Effect that expands from the center with increasing sound energy"""
        self.audio_data = np.copy(self.audio_data)
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        # Scale by the width of the LED strip
        self.audio_data *= float((self.total_pixel_number // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        intensity = (int(np.max(self.audio_data[:len(self.audio_data) // 3])) + int(np.max(self.audio_data[len(
            self.audio_data) // 3: 2 * len(self.audio_data) // 3])) + int(np.max(self.audio_data[2 * len(self.audio_data) // 3:]))) // 3
        new_intensity = self.old_intensity_bounce - 1
        if(new_intensity > intensity):
            intensity = new_intensity
        print(intensity)
        # Assign color to different frequency regions
        self.pixels[0] = 0.5 * intensity
        self.pixels[1] = 0.5 * intensity
        self.pixels[2] = 0.5 * intensity
        print(self.pixels[0][0])
        self.p_filt.update(self.pixels)
        self.pixels = np.round(self.p_filt.value)
        self.old_intensity_bounce = intensity

    # ENERGY VIZ #####
    def visualizeEnergy(self):
        """Effect that expands from the center with increasing sound energy"""
        self.audio_data = np.copy(self.audio_data)
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        # Scale by the width of the LED strip
        self.audio_data *= float((self.total_pixel_number // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        if(self.is_monochrome):
            value = (int(np.mean(self.audio_data[:len(self.audio_data) // 3]**scale)) + int(np.mean(self.audio_data[len(self.audio_data) // 3: 2 * len(
                self.audio_data) // 3]**scale)) + int(np.mean(self.audio_data[2 * len(self.audio_data) // 3:]**scale))) // 3
            # Assign color to different frequency regions
            self.pixels[0, :value] = self.colorDictionary.dictionary[self.current_color][0]
            self.pixels[0, value:] = 0.0
            self.pixels[1, :value] = self.colorDictionary.dictionary[self.current_color][1]
            self.pixels[1, value:] = 0.0
            self.pixels[2, :value] = self.colorDictionary.dictionary[self.current_color][2]
            self.pixels[2, value:] = 0.0
            self.p_filt.update(self.pixels)
            self.pixels = np.round(self.p_filt.value)
            # Apply substantial blur to smooth the edges
            self.pixels[0, :] = gaussian_filter1d(self.pixels[0, :], sigma=4.0)
            self.pixels[1, :] = gaussian_filter1d(self.pixels[1, :], sigma=4.0)
            self.pixels[2, :] = gaussian_filter1d(self.pixels[2, :], sigma=4.0)
        else:
            r = int(
                np.mean(self.audio_data[:len(self.audio_data) // 3]**scale))
            g = int(np.mean(self.audio_data[len(
                self.audio_data) // 3: 2 * len(self.audio_data) // 3]**scale))
            b = int(
                np.mean(self.audio_data[2 * len(self.audio_data) // 3:]**scale))
            # Assign color to different frequency regions
            self.pixels[0, :r] = 255.0
            self.pixels[0, r:] = 0.0
            self.pixels[1, :g] = 255.0
            self.pixels[1, g:] = 0.0
            self.pixels[2, :b] = 255.0
            self.pixels[2, b:] = 0.0
            self.p_filt.update(self.pixels)
            self.pixels = np.round(self.p_filt.value)
            # Apply substantial blur to smooth the edges
            self.pixels[0, :] = gaussian_filter1d(self.pixels[0, :], sigma=4.0)
            self.pixels[1, :] = gaussian_filter1d(self.pixels[1, :], sigma=4.0)
            self.pixels[2, :] = gaussian_filter1d(self.pixels[2, :], sigma=4.0)

    # SPECTRUM VIZ #####
    def visualizeSpectrum(self):
        """Effect that maps the Mel filterbank frequencies onto the LED strip"""
        self.audio_data = np.copy(interpolate(
            self.audio_data, self.total_pixel_number // 2))
        self.common_mode.update(self.audio_data)
        diff = self.audio_data - self.prev_spectrum
        self.prev_spectrum = np.copy(self.audio_data)
        # Color channel mappings
        r = self.r_filt.update(self.audio_data - self.common_mode.value)
        g = self.g_filt.update(
            np.copy(self.audio_data - self.common_mode.value))
        b = self.b_filt.update(
            np.copy(self.audio_data - self.common_mode.value))
        # Mirror the color channels for symmetric output
        r = np.concatenate((r[::-1], r))
        g = np.concatenate((g[::-1], g))
        b = np.concatenate((b[::-1], b))
        self.pixels = np.array([r, g, b]) * 255

    # SYNTH VIZ #####
    def visualizeSynth(self):
        """Piano"""
        for midi_note in self.midi_notes:
            real_note = midi_note["note"]
            r = self.colorDictionary.dictionary[self.current_color][0]
            g = self.colorDictionary.dictionary[self.current_color][1]
            b = self.colorDictionary.dictionary[self.current_color][2]
            putPixel(self.pixels, 0, r, g, b)
        shiftPixelsSmoothly(self.pixels)
