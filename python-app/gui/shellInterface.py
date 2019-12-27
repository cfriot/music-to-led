import signal, time, sys, psutil, os
from blessed import Terminal
from functools import partial
import numpy as np

class ShellInterface():
    def __init__(self, config):

        self.input = ""

        self.min_width = 123
        self.header_offset = 0
        self.audio_offset = 7
        self.strip_offset = 12
        self.rgb_border_color = (100,100,100)
        self.rgb_inner_border_color = (50,50,50)


        self.config = config

        time.sleep(1)

        self.term = Terminal()
        self.color_background = self.term.on_black
        self.echo = partial(print, end='', flush=True)

        self.height, self.width = self.term.height, self.term.width

        if (self.width < self.min_width):
            print("min size")
            quit()

        self.term.fullscreen()

        self.echo(self.term.clear)
        # for i in range(self.height):
        #     self.echo(self.term.move(i, 0) + (" " * self.width))
        # self.clearTerminal()

        # signal.signal(signal.SIGWINCH, self.on_resize)

        self.initBoxes()

    def on_resize(self, signum, frame):
        self.height, self.width = self.term.height, self.term.width

    def initBoxes(self):

        self.printHeader(self.header_offset)

        for index in range(self.config.number_of_audio_ports):

            offset = ((index * 32), self.audio_offset)
            size = (29, 3)
            self.drawBox(offset, size, self.rgb_border_color)

        for index in range(self.config.number_of_strips):

            offset = (0, self.strip_offset + (index * 8))
            size = (self.min_width, 7)
            self.drawBox(offset, size, self.rgb_border_color)
            self.echo(self.term.move(offset[1] + 2, 0) + self.textWithColor(50,50,50,"├" + ("─" * (self.min_width - 2)) + "┤"))
            self.echo(self.term.move(offset[1] + 5, 0) + self.textWithColor(50,50,50,"├" + ("─" * (self.min_width - 2)) + "┤"))


    @staticmethod
    def clearTerminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def rgbToAnsi256(r, g, b):
        if (r == g and g == b):
            if (r < 8):
                return 16
            if (r > 248):
                return 231
            return round(((r - 8) / 247) * 24) + 232
        ansi = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
        return ansi

    def drawFrame(pixel):
        with term.hidden_cursor(), term.cbreak(), term.location():
            self.echo("drawframe")

    def printHeader(self, y):
        size_of_title = len(" __  __ _   _ ___ ___ ___   _____ ___    _    ___ ___")
        space = (self.min_width - size_of_title) // 2
        self.echo(self.term.move(y + 0, space) + " __  __ _   _ ___ ___ ___   _____ ___    _    ___ ___")
        self.echo(self.term.move(y + 1, space) + "|  \\/  | | | / __|_ _/ __| |_   _/ _ \\  | |  | __|   \\")
        self.echo(self.term.move(y + 2, space) + "| |\\/| | |_| \__ \\| | (__    | || (_) | | |__| _|| |) |")
        self.echo(self.term.move(y + 3, space) + "|_|  |_|\___/|___/___\\___|   |_| \___/  |____|___|___/")
        self.echo(self.term.move(y + 4, space) + "                                                v0.1.1")

    def drawBox(self, offset, size, color=(255,255,255)):
        style = "─|┌┐└┘" # ││
        x, y = offset
        w, h = size
        r,g,b = color

        first_line = style[2] + (style[0] * (w - 2)) + style[3]
        middle_line = style[1] + (" " * (w - 2)) + style[1]
        last_line = style[4] + (style[0] * (w - 2)) + style[5]

        self.echo(self.term.move(y, x) + self.textWithColor(r,g,b,first_line))
        for i in range(h):
            self.echo(self.term.move(y + i + 1, x) + self.textWithColor(r,g,b,middle_line))
        self.echo(self.term.move(y + h, x) + self.textWithColor(r,g,b,last_line))

    def waitForInput(self):
        self.input = self.term.inkey(timeout=0)
        self.echo(self.term.move(0, 85) + "input :" + self.input)
        if(self.input == "f"):
            print("ditwoula")

    def textWithColor(self, r, g, b, text):
        return self.term.color(int(self.rgbToAnsi256(r, g, b)))(text)

    def printAudio(self, y, x, name, audio_datas):
        self.echo(self.term.move(y, x) + name)

        style = "▁▂▃▅▆▇"

        graph = ""

        for channel in audio_datas:
            charIndex = int(channel * 10) if int(channel * 10) < len(style) - 1 else len(style) - 1
            graph += style[charIndex]

        self.echo(self.term.move(y + 2, x + 1) + graph)
        self.echo(self.term.move(0, 0))

    def printStrip(self, y, is_connected, framerate, strip_config, pixels):

       with self.term.hidden_cursor(), self.term.cbreak(), self.term.location():

            is_connected = self.textWithColor(0, 255, 0, ' ⬤ online') if is_connected else self.textWithColor(255, 0, 0, ' ⬤ offline')
            is_connected_str = is_connected + self.textWithColor(100, 100, 100, ' at ') + framerate + self.textWithColor(100, 100, 100, ' FPS ')
            mirror_mode = self.textWithColor(255, 255, 255, 'mirror') if strip_config.is_mirror else self.textWithColor(50, 50, 50, 'mirror')
            reverse_mode = self.textWithColor(255, 255, 255, 'reverse') if strip_config.is_reverse else self.textWithColor(50, 50, 50, 'reverse')
            color_scheme = ""
            for current_color in strip_config.formatted_color_schemes[strip_config.active_color_scheme_index]:
                color_scheme += self.term.color(int(self.rgbToAnsi256(current_color[0], current_color[1], current_color[2])))('█ ')
            shape = ""
            for current_shape in strip_config.shapes[strip_config.active_shape_index].shape:
                shape += "[" + str(current_shape) + "]"


            self.echo(self.term.move(y + 1, 2) + strip_config.name + self.textWithColor(100, 100, 100, ' on ') + "                           ")
            self.echo(self.term.move(y + 1, 2) + strip_config.name + self.textWithColor(100, 100, 100, ' on ') + strip_config.active_visualizer_effect + " ")
            self.echo(self.term.move(y + 1, self.min_width - 22) + is_connected_str)


            self.echo(self.term.move(y + 3, 2) + self.textWithColor(100, 100, 100, 'audio channel'))
            self.echo(self.term.move(y + 4, 2) + "                    ")
            self.echo(self.term.move(y + 4, 2) + self.config.audio_ports[strip_config.active_audio_channel_index].name)

            self.echo(self.term.move(y + 3, 22) + self.textWithColor(100, 100, 100, 'color scheme'))
            self.echo(self.term.move(y + 4, 22) + "                    ")
            self.echo(self.term.move(y + 4, 22) + color_scheme)

            self.echo(self.term.move(y + 3, 42) + self.textWithColor(100, 100, 100, 'shape'))
            self.echo(self.term.move(y + 4, 42) + "                    ")
            self.echo(self.term.move(y + 4, 42) + shape)

            self.echo(self.term.move(y + 3, 62) + self.textWithColor(100, 100, 100, 'time_interval'))
            self.echo(self.term.move(y + 4, 62) + "                    ")
            self.echo(self.term.move(y + 4, 62) + str(strip_config.time_interval))

            self.echo(self.term.move(y + 3, 78) + self.textWithColor(100, 100, 100, 'brightness'))
            self.echo(self.term.move(y + 4, 78) + "                    ")
            self.echo(self.term.move(y + 4, 78) + str(strip_config.max_brightness))

            self.echo(self.term.move(y + 3, 90) + self.textWithColor(100, 100, 100, 'chunk_size'))
            self.echo(self.term.move(y + 4, 90) + "                    ")
            self.echo(self.term.move(y + 4, 90) + str(strip_config.chunk_size))

            self.echo(self.term.move(y + 3, 103) + mirror_mode)
            self.echo(self.term.move(y + 3, 113) + reverse_mode)

            array = self.getTermArrayFromPixels(pixels)
            self.echo(self.term.move(y + 6, 2) + array)

            self.echo(self.term.move(0, 0))

    def getTermArrayFromPixels(self, pixels):
        array = ""
        for i in range(len(pixels[0])):
            array += self.term.color(int(self.rgbToAnsi256(pixels[0][i], pixels[1][i], pixels[2][i])))('█')
        return array
