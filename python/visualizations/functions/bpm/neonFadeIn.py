import numpy as np

class NeonFadeIn():

    def visualizeNeonFadeIn(self):
        """ Effect that imitate the neon fade in """
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        colors = [
            [0, 0, 0],
            color_scheme[0]
        ]
        fadeInArray = [
            0, 25, 50, 60, 115, 155
        ]
        which_color = 0
        time = self.timeSinceStart.getMs()

        for i in range(self.number_of_pixels):
            for x, step in enumerate(fadeInArray):
                if(time < step):
                    break;
                if(x % 2 == 0):
                    which_color = 0
                else:
                    which_color = 1
            self.pixels[0][i] = colors[which_color][0]
            self.pixels[1][i] = colors[which_color][1]
            self.pixels[2][i] = colors[which_color][2]

        return self.pixels
