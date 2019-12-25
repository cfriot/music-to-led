import numpy as np

class DrawLine():

    def visualizeDrawLine(self):
        """Effect that alternate two colors moving forward"""
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        self.pixels = np.roll(
            self.pixels, int(1 * (self.strip_config.time_interval / 100)) + 1, axis=1)

        self.pixels[0][0] = color_scheme[0][0]
        self.pixels[1][0] = color_scheme[0][1]
        self.pixels[2][0] = color_scheme[0][2]


        return self.pixelReshaper.reshapeFromPixels(self.pixels)
