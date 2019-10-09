import numpy as np

class AlternateColors():

    def visualizeAlternateColors(self):
        """Effect that alternate two colors moving forward"""
        size = 5
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        # print(self.timeSinceStart.getMs())
        # print(self.timeSinceStart.getMs() * bpm)
        which_color = 0
        # toto = bpmTicker.isTicking()
        # print(toto)
        # if(toto == 1):
        #     print("toto")
        # if(toto == 2):
        #     print("titi")

        for i in range(self.number_of_pixels):
            if(i % size == 0):
                which_color += 1
                if(which_color >= len(color_scheme)):
                    which_color = 0
            self.pixels[0][i] = color_scheme[which_color][0]
            self.pixels[1][i] = color_scheme[which_color][1]
            self.pixels[2][i] = color_scheme[which_color][2]
        self.pixels = np.roll(
            self.pixels, self.timeSinceStart.getMs() // 3, axis=1)

        return self.pixelReshaper.reshapeFromPixels(self.pixels)
