import numpy as np

class IntensityBounce():

    # INTENSITY BOUNCE VIZ #####
    def visualizeIntensityBounce(self):
        """Effect that expands from the center with increasing sound energy"""
        self.audio_data = np.copy(self.audio_data)
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        # Scale by the width of the LED strip
        self.audio_data *= float((self.number_of_pixels // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        intensity = (int(np.max(self.audio_data[:len(self.audio_data) // 3])) + int(np.max(self.audio_data[len(
            self.audio_data) // 3: 2 * len(self.audio_data) // 3])) + int(np.max(self.audio_data[2 * len(self.audio_data) // 3:]))) // 3
        new_intensity = self.old_intensity_bounce - 1
        if(new_intensity > intensity):
            intensity = new_intensity
        # print(intensity)
        # Assign color to different frequency regions
        self.pixels[0] = 0.5 * intensity
        self.pixels[1] = 0.5 * intensity
        self.pixels[2] = 0.5 * intensity
        # print(self.pixels[0][0])
        self.p_filt.update(self.pixels)
        self.pixels = np.round(self.p_filt.value)
        self.old_intensity_bounce = intensity

        return self.pixels
