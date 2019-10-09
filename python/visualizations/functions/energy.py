import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

class Energy():

    def visualizeEnergy(self):
        """Effect that expands from the center with increasing sound energy"""
        self.audio_data = np.copy(self.audio_data)
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        # Scale by the width of the LED strip
        self.audio_data *= float((self.number_of_pixels // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        r = 0
        g = 0
        b = 0
        active_color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]
        chunk_size = len(self.audio_data) // len(active_color_scheme)
        for i in range(len(active_color_scheme)) :
            x = chunk_size * i
            y = chunk_size * (i + 1)
            value = int(np.mean(self.audio_data[x:y]**scale))
            r += int(value * active_color_scheme[i][0] / 100)
            g += int(value * active_color_scheme[i][1] / 100)
            b += int(value * active_color_scheme[i][2] / 100)

        self.pixels[0, :r] = 255.0
        self.pixels[0, r:] = 0.0
        self.pixels[1, :g] = 255.0
        self.pixels[1, g:] = 0.0
        self.pixels[2, :b] = 255.0
        self.pixels[2, b:] = 0.0
        self.p_filt.update(self.pixels)
        self.pixels = np.round(self.p_filt.value)
        # Apply substantial blur to smooth the edges
        self.pixels[0, :] = gaussian_filter1d(self.pixels[0, :], sigma=1.0)
        self.pixels[1, :] = gaussian_filter1d(self.pixels[1, :], sigma=1.0)
        self.pixels[2, :] = gaussian_filter1d(self.pixels[2, :], sigma=1.0)

        return self.pixelReshaper.reshapeFromPixels(self.pixels)
