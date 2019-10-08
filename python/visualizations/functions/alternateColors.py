import numpy as np

class AlternateColors():

    def visualizeAlternateColors(self):
        """Effect that alternate two colors moving forward"""
        size = 20
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]
        which_color = 0
        for i in range(self.number_of_pixels):
            if(i % size == 0):
                which_color += 1
                if(which_color >= len(color_scheme)):
                    which_color = 0
            self.pixels[0][i] = color_scheme[which_color][0]
            self.pixels[1][i] = color_scheme[which_color][1]
            self.pixels[2][i] = color_scheme[which_color][2]
        self.pixels = np.roll(
            self.pixels, self.timeSinceStart.getMs(), axis=1)

        return self.pixelReshaper.reshape(self.pixels)
