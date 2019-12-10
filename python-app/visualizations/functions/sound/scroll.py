import numpy as np

class Scroll():

    def visualizeScroll(self):
        """Effect that originates in the center and scrolls outwards"""
        self.audio_data = self.audio_data**2.0
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        self.audio_data *= 255.0

        active_color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]
        length_of_color_scheme = len(active_color_scheme)
        chunk_size = len(self.audio_data) // length_of_color_scheme
        r = 0
        g = 0
        b = 0

        for i in range(length_of_color_scheme) :
            x = chunk_size * i
            y = chunk_size * (i + 1)
            value = int(np.mean(self.audio_data[x:y]))
            r += value * active_color_scheme[i][0]
            g += value * active_color_scheme[i][1]
            b += value * active_color_scheme[i][2]

        r = r / length_of_color_scheme
        g = g / length_of_color_scheme
        b = b / length_of_color_scheme

        self.pixels[:, 1:] = self.pixels[:, :-1]
        self.pixels *= 0.98
        self.blurFrame(0.2)
        self.pixels[0, 0] = r
        self.pixels[1, 0] = g
        self.pixels[2, 0] = b

        self.pixels = np.clip(self.pixels, 0, 255)

        return self.pixelReshaper.reshapeFromPixels(self.pixels)
