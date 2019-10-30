import numpy as np

class Full():

    def initFull(self):
        self.old_full_intensity = 0
        self.old_intensity_bounce = 0

    @staticmethod
    def lerp(start, end, d):
        return start * (1 - d) + end * d

    def visualizeFull(self):
        color_scheme = self.strip_config.formatted_color_schemes[self.strip_config.active_color_scheme_index]
        self.pixels[0] = self.lerp(self.pixels[0], color_scheme[0][0], self.old_full_intensity)
        self.pixels[1] = self.lerp(self.pixels[1], color_scheme[0][1], self.old_full_intensity)
        self.pixels[2] = self.lerp(self.pixels[2], color_scheme[0][2], self.old_full_intensity)
        self.pixels = np.clip(self.pixels, 0, 255)
        if(self.old_full_intensity < 1):
            self.old_full_intensity += 0.01

        return self.pixels

    def visualizeNothing(self):
        self.pixels[0] = self.pixels[0] * self.old_full_intensity
        self.pixels[1] = self.pixels[1] * self.old_full_intensity
        self.pixels[2] = self.pixels[2] * self.old_full_intensity
        self.pixels = np.clip(self.pixels, 0, 255)
        if(self.old_full_intensity > 0):
            self.old_full_intensity -= 0.01

        return self.pixels
