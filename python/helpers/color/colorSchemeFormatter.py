from colour import Color

class ColorSchemeFormatter:
    """ Format a color scheme """

    def render(self, colors):
        formatted_colors = []
        for i, color in enumerate(colors):
            rgb_255_color = self.interpolate_to_rgb_255(Color(color))
            formatted_colors.append([rgb_255_color[0], rgb_255_color[1], rgb_255_color[2]])
        return formatted_colors

    @staticmethod
    def interpolate_to_rgb_255(color):
        r = (int)(color.rgb[0] * 255.999)
        g = (int)(color.rgb[1] * 255.999)
        b = (int)(color.rgb[2] * 255.999)
        return [r, g, b]


if __name__ == '__main__':


    print('Starting ColorFormatter test on ports :')

    color = Color("blue")

    print(color)
    print(ColorFormatter.interpolate_to_rgb_255(color))
