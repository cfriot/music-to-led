import numpy as np

class TransitionColors():

    def initTransitionColorShapes(self):
        self.color_index = 0

    @staticmethod
    def lerp2(a, b, t):
        return [
            a[0]*(1 - t) + b[0]*t,
            a[1]*(1 - t) + b[1]*t,
            a[2]*(1 - t) + b[2]*t
        ]

    @staticmethod
    def rgbLerp(a, b, time):
        return [a[0] + (b[0] - a[0]) * time,
        a[1] + (b[1] - a[1]) * time,
        a[2] + (b[2] - a[2]) * time]

    def visualizeTransitionColorShapes(self):
        """Effect that alternate two colors moving forward"""

        ms = self.timeSinceStart.getMs()
        interval = self.timeSinceStart.getMsIntervalFromBpm(self.active_state.time_interval)
        color_scheme = self.active_state.formatted_color_schemes[self.active_state.active_color_scheme_index]

        # print("interval")
        # print(interval)

        if(ms >= interval):
            self.color_index += 1
            self.timeSinceStart.restart()
        currentTime = round(ms / interval, 2)

        if(self.color_index >= len(color_scheme) - 1):
            self.color_index = 0

        if(currentTime > 1.0):
            currentTime = 1.0

        # print("current time " + str(currentTime))

        color = self.lerp2(color_scheme[self.color_index], color_scheme[self.color_index + 1], currentTime)
        self.pixels[0] = color[0]
        self.pixels[1] = color[1]
        self.pixels[2] = color[2]

        # print("color " + str(self.pixels[0][0]) + ", " + str(self.pixels[1][0]) + ", " + str(self.pixels[2][0]))

        return self.pixelReshaper.reshapeFromPixels(self.pixels)

        # which_color = self.alternate_colors_index % len(color_scheme)
        #
        # self.pixelReshaper.initActiveShape()
        #
        # for x, strip in enumerate(self.pixelReshaper.strips):
        #     which_color += 1
        #     if(which_color >= len(color_scheme)):
        #         which_color = 0
        #     max_length = len(strip[0])
        #     for i in range(max_length):
        #         strip[0][i] = color_scheme[which_color][0]
        #         strip[1][i] = color_scheme[which_color][1]
        #         strip[2][i] = color_scheme[which_color][2]
