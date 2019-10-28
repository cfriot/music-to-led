import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

from helpers.audio.expFilter import ExpFilter

import time

class IntensityChannels():

    def initIntensityChannels(self):
        self.oldStripItensities = []
        self.oldMaxStripItensities = []
        self.intervalForDecrease = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm)
        self.intervalForMaxDecrease = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm) // 2


    def visualizeIntensityChannels(self):
        """ Effect that expands with increasing sound energy """

        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        self.audio_data = np.copy(self.audio_data)
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        # Scale by the width of the LED strip
        self.audio_data *= float((self.number_of_pixels // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9

        stripItensities = []
        maxStripItensities = []

        chunk_size = len(self.audio_data) // self.pixelReshaper.number_of_strips

        for i in range(self.pixelReshaper.number_of_strips) :
            x = chunk_size * i
            y = chunk_size * (i + 1)
            stripItensities.append(int(np.mean(self.audio_data[x:y]**scale)))
            maxStripItensities.append(int(np.mean(self.audio_data[x:y]**scale)))

            if(self.oldStripItensities != [] and stripItensities[i] < self.oldStripItensities[i]) :
                stripItensities[i] = self.oldStripItensities[i] - 2

            if(self.oldMaxStripItensities != [] and maxStripItensities[i] < self.oldMaxStripItensities[i]) :
                maxStripItensities[i] = self.oldMaxStripItensities[i] - 1
            # else:
            #     maxStripItensities[i] = -1

        # if(self.timeSinceStart.getMs() >= 300):
        #     self.timeSinceStart.restart()

        # print(stripItensities)
        # print(maxStripItensities)

        self.oldStripItensities = stripItensities
        self.oldMaxStripItensities = maxStripItensities

        self.pixelReshaper.initActiveShape()

        for x, strip in enumerate(self.pixelReshaper.strips):
            max_length = len(strip[0])
            for i in range(max_length):
                if(i < stripItensities[x]):
                    strip[0][i] = color_scheme[0][0]
                    strip[1][i] = color_scheme[0][1]
                    strip[2][i] = color_scheme[0][2]
                if(i == maxStripItensities[x]):
                    strip[0][i] = color_scheme[1][0]
                    strip[1][i] = color_scheme[1][1]
                    strip[2][i] = color_scheme[1][2]

            p_filt = ExpFilter(
                np.tile(1, (3, max_length)),
                alpha_decay = 0.1,
                alpha_rise = 0.99
            )
            p_filt.update(strip)
            strip = np.round(p_filt.value)
            # Apply substantial blur to smooth the edges
            strip[0, :] = gaussian_filter1d(strip[0, :], sigma=1.0)
            strip[1, :] = gaussian_filter1d(strip[1, :], sigma=1.0)
            strip[2, :] = gaussian_filter1d(strip[2, :], sigma=1.0)
        return self.pixelReshaper.reshapeFromStrips(self.pixelReshaper.strips)
