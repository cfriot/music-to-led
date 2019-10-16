import numpy as np

class AlternateColors():

    def initAlternateColors(self):
        self.alternate_colors_index = 0

    def visualizeAlternateColors(self):
        """Effect that alternate two colors moving forward"""
        size = 5
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        which_color = 0

        interval = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm)

        if(self.timeSinceStart.getMs() >= interval):
            self.alternate_colors_index += 1
            self.timeSinceStart.restart()

        for i in range(self.number_of_pixels):
            if(i % size == 0):
                which_color += 1
                if(which_color >= len(color_scheme)):
                    which_color = 0
            self.pixels[0][i] = color_scheme[which_color][0]
            self.pixels[1][i] = color_scheme[which_color][1]
            self.pixels[2][i] = color_scheme[which_color][2]
        self.pixels = np.roll(
            self.pixels, self.timeSinceStart.getMs() // 100, axis=1)

        return self.pixelReshaper.reshapeFromPixels(self.pixels)


    def visualizeAlternateColorsFull(self):
        """Effect that alternate two colors moving forward"""
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        interval = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm)

        if(self.timeSinceStart.getMs() >= interval):
            self.alternate_colors_index += 1
            self.timeSinceStart.restart()

        which_color = self.alternate_colors_index % len(color_scheme)

        self.pixelReshaper.initActiveShape()

        if(which_color >= len(color_scheme)):
            which_color = 0

        for x, strip in enumerate(self.pixelReshaper.strips):
            max_length = len(strip[0])
            for i in range(max_length):
                strip[0][i] = color_scheme[which_color][0]
                strip[1][i] = color_scheme[which_color][1]
                strip[2][i] = color_scheme[which_color][2]

        return self.pixelReshaper.reshapeFromStrips(self.pixelReshaper.strips)


    def visualizeAlternateColorsForShapes(self):
        """Effect that alternate two colors moving forward"""
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        interval = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm)

        if(self.timeSinceStart.getMs() >= interval):
            self.alternate_colors_index += 1
            self.timeSinceStart.restart()


        which_color = self.alternate_colors_index % len(color_scheme)

        self.pixelReshaper.initActiveShape()

        for x, strip in enumerate(self.pixelReshaper.strips):
            which_color += 1
            if(which_color >= len(color_scheme)):
                which_color = 0
            max_length = len(strip[0])
            for i in range(max_length):
                strip[0][i] = color_scheme[which_color][0]
                strip[1][i] = color_scheme[which_color][1]
                strip[2][i] = color_scheme[which_color][2]

        return self.pixelReshaper.reshapeFromStrips(self.pixelReshaper.strips)
