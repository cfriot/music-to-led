import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

from helpers.audio.expFilter import ExpFilter

class IntensityChannels():

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
        chunk_size = len(self.audio_data) // self.pixelReshaper.number_of_strips
        # print(chunk_size)
        for i in range(self.pixelReshaper.number_of_strips) :
            x = chunk_size * i
            y = chunk_size * (i + 1)
            stripItensities.append(int(np.mean(self.audio_data[x:y]**scale)))

        # print(stripItensities)
        self.pixelReshaper.initActiveShape()

        for x, strip in enumerate(self.pixelReshaper.strips):
            max_length = len(strip[0])
            for i in range(max_length):
                if(i < stripItensities[x]):
                    strip[0][i] = color_scheme[0][0]
                    strip[1][i] = color_scheme[0][1]
                    strip[2][i] = color_scheme[0][2]

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

            print(strip)
            if(self.strip_config.is_reverse):
                strip = self.pixelReshaper.reversePixels(strip)
            if(self.strip_config.is_mirror):
                strip = self.pixelReshaper.mirrorPixels(strip, max_length)
            print(strip)

        return self.pixelReshaper.concatenatePixels(self.pixelReshaper.strips)
