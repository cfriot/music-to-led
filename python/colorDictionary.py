from colour import Color

# color_list = [
# Color("red"),
# Color("green"),
# Color("blue"),
# Color("yellow"),
# Color("white"),
# Color("black"),
# ]


class ColorDictionary:
    def __init__(self):
        self.color_list = []
        for i in range(30):
            self.color_list.append(
                Color(hue=i / 30, saturation=1, luminance=0.5))

        # self.color_list = [
        #     Color("red"),
        #     Color("green"),
        #     Color("blue"),
        #     Color("yellow"),
        #     Color("white"),
        #     Color("black"),
        # ]
        self.dictionary = []
        self.render()

    def render(self):
        self.dictionary = []
        for i, color in enumerate(self.color_list):
            rgb_255_color = self.interpolate_to_rgb_255(color)
            self.dictionary.append(
                [rgb_255_color[0], rgb_255_color[1], rgb_255_color[2]])

    @staticmethod
    def interpolate_to_rgb_255(color):
        r = (int)(color.rgb[0] * 255.999)
        g = (int)(color.rgb[1] * 255.999)
        b = (int)(color.rgb[2] * 255.999)
        return [r, g, b]


if __name__ == '__main__':

    import numpy as np
    import time
    from serialToArduinoLedStrip import SerialToArduinoLedStrip

    print('Starting color dictionary test on ports :')
    print(SerialToArduinoLedStrip.listAvailableUsbSerialPorts())

    colorDictionary = ColorDictionary()
    number_of_pixels_by_strip = 30

    pixels = np.tile(1, (3, number_of_pixels_by_strip))
    pixels *= 0
    for i, color in enumerate(colorDictionary.dictionary):
        pixels[0, i] = color[0]
        pixels[1, i] = color[1]
        pixels[2, i] = color[2]

    serialToArduinoLedStrip = SerialToArduinoLedStrip(
        number_of_pixels_by_strip)
    serialToArduinoLedStrip.setup()

    while True:
        pixels = np.roll(pixels, 1, axis=1)
        serialToArduinoLedStrip.update(pixels)
        time.sleep(.02)
