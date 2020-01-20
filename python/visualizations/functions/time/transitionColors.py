import numpy as np

class TransitionColors():

    def initTransitionColorShapes(self):
        self.alternate_colors_index = 0

    def drawTransitionColorShapes(self):

        color_scheme = self.active_state.formatted_color_schemes[self.active_state.active_color_scheme_index]

        which_color = 0
        self.alternateColorsInterval = self.timeSinceStart.getMsIntervalFromBpm(self.active_state.time_interval)

        if(self.active_state.chunk_size == 0):
            self.active_state.chunk_size = 1

        for i in range(self.number_of_pixels):
            if(i % self.active_state.chunk_size == 0):
                which_color += 1
                if(which_color >= len(color_scheme)):
                    which_color = 0
            self.pixels[0][i] = color_scheme[which_color][0]
            self.pixels[1][i] = color_scheme[which_color][1]
            self.pixels[2][i] = color_scheme[which_color][2]

    def visualizeTransitionColorShapes(self):
        """Effect that alternate two colors moving forward"""

        # TO DO
        
        color_scheme = self.active_state.formatted_color_schemes[self.active_state.active_color_scheme_index]

        interval = self.timeSinceStart.getMsIntervalFromBpm(self.active_state.time_interval)

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
