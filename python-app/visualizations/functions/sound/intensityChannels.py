import time
import numpy as np

from helpers.audio.expFilter import ExpFilter


class IntensityChannels():

    def initIntensityChannels(self):
        self.oldStripItensities = []
        self.oldMaxStripItensities = []
        self.intervalForDecrease = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.time_interval)
        self.intervalForMaxDecrease = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.time_interval) // 2


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

            if(self.strip_config.active_visualizer_mode == 1):
                intensity = int(np.max(self.audio_data[x:y]**scale))
                if(intensity < 0) :
                    intensity = 0
            else:
                intensity = int(np.mean(self.audio_data[x:y]**scale))

            max_intensity = len(self.pixelReshaper.strips[i][0])
            if(self.strip_config.is_mirror):
                max_intensity = len(self.pixelReshaper.strips[i][0]) / 2

            if(intensity > max_intensity):
                intensity = max_intensity - 1

            stripItensities.append(intensity)
            maxStripItensities.append(intensity)

            if(self.oldStripItensities != [] and stripItensities[i] < self.oldStripItensities[i]) :
                stripItensities[i] = self.oldStripItensities[i] - 2

            if(self.oldMaxStripItensities != [] and maxStripItensities[i] < self.oldMaxStripItensities[i]) :
                maxStripItensities[i] = self.oldMaxStripItensities[i] - 1


        self.oldStripItensities = stripItensities
        self.oldMaxStripItensities = maxStripItensities

        self.pixelReshaper.initActiveShape()

        if(self.strip_config.active_visualizer_mode == 1) :
            for x, strip in enumerate(self.pixelReshaper.strips):
                colorIndex = x % len(color_scheme)
                strip[0] = color_scheme[colorIndex][0]
                strip[1] = color_scheme[colorIndex][1]
                strip[2] = color_scheme[colorIndex][2]
                self.pixelReshaper.strips[x] = self.applyMaxBrightness(strip, stripItensities[x] * 10)
        else :
            for x, strip in enumerate(self.pixelReshaper.strips):
                max_length = len(strip[0])
                for i in range(max_length):
                    if(i < stripItensities[x]):
                        strip[0][i] = color_scheme[0][0]
                        strip[1][i] = color_scheme[0][1]
                        strip[2][i] = color_scheme[0][2]
                    if(i == maxStripItensities[x]):
                        strip[0][i] = color_scheme[1][0] if len(color_scheme) >= 2 else color_scheme[0][0]
                        strip[1][i] = color_scheme[1][1] if len(color_scheme) >= 2 else color_scheme[0][1]
                        strip[2][i] = color_scheme[1][2] if len(color_scheme) >= 2 else color_scheme[0][2]

        return self.pixelReshaper.reshapeFromStrips(self.pixelReshaper.strips)
