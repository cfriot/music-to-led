import numpy as np

class AlternateColors():

    def initAlternateColors(self):
        self.alternate_colors_index = 0
        self.alternate_colors_size = 1

    def drawAlternateColors(self):

        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]

        which_color = 0
        self.alternateColorsInterval = self.timeSinceStart.getMsIntervalFromBpm(self.strip_config.bpm)

        if(self.alternate_colors_size == 0):
            self.alternate_colors_size = 1

        for i in range(self.number_of_pixels):
            if(i % self.alternate_colors_size == 0):
                which_color += 1
                if(which_color >= len(color_scheme)):
                    which_color = 0
            self.pixels[0][i] = color_scheme[which_color][0]
            self.pixels[1][i] = color_scheme[which_color][1]
            self.pixels[2][i] = color_scheme[which_color][2]

    def visualizeAlternateColors(self):
        """Effect that alternate two colors moving forward"""

        if(self.timeSinceStart.getMs() >= self.alternateColorsInterval):
            self.alternate_colors_index += 1
            self.timeSinceStart.restart()

        self.pixels = np.roll(
            self.pixels, int(1 * (self.strip_config.bpm / 100)) + 1, axis=1)
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
