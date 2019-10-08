import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

class Scroll():

    def visualizeScroll(self):
        """Effect that originates in the center and scrolls outwards"""
        self.audio_data = self.audio_data**2.0
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        self.audio_data *= 255.0

        values = []
        active_color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]
        chunk_size = len(self.audio_data) // len(active_color_scheme)
        r = 0
        g = 0
        b = 0

        for i in range(len(active_color_scheme)) :
            x = chunk_size * i
            y = chunk_size * (i + 1)
            values.append(int(np.mean(self.audio_data[x:y])))
            value = int(np.mean(self.audio_data[x:y]))
            r += value * active_color_scheme[i][0]
            g += value * active_color_scheme[i][1]
            b += value * active_color_scheme[i][2]

        r = r / len(active_color_scheme)
        g = g / len(active_color_scheme)
        b = b / len(active_color_scheme)

        self.pixels[:, 1:] = self.pixels[:, :-1]
        self.pixels *= 0.98
        self.pixels = gaussian_filter1d(self.pixels, sigma=0.7)
        self.pixels[0, 0] = r
        self.pixels[1, 0] = g
        self.pixels[2, 0] = b

        return self.pixelReshaper.reshape(self.pixels)
