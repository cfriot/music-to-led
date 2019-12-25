import signal, time, sys, psutil, os
from blessed import Terminal
from functools import partial
import numpy as np

class ShellInterface():
    def __init__(self):
        # self.echo("Init Shell Interface")

        self.term = Terminal()

        with self.term.fullscreen():

            self.input = ""
            self.echo = partial(print, end='', flush=True)

            self.height, self.width = self.term.height, self.term.width

            color_bg = self.term.on_black
            signal.signal(signal.SIGWINCH, self.on_resize)

            # self.echo(self.term.clear)
            for i in range(self.height):
                self.echo(self.term.move(i, 0) + (" " * self.width))
            # self.clearTerminal()

    def on_resize(self, signum, frame):
        self.height, self.width = self.term.height, self.term.width

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

    def printHeader(self):
        self.echo(self.term.move(0, 1) + "    __  _____  _______________    __________      __   _______")
        self.echo(self.term.move(1, 1) + "   /  |/  / / / / __/  _/ ___/   /_  __/ __ \\    / /  / __/ _ \\")
        self.echo(self.term.move(2, 1) + "  / /|_/ / /_/ /\\ \\_/ // /__      / / / /_/ /   / /__/ _// // /")
        self.echo(self.term.move(3, 1) + " /_/  /_/\\____/___/___/\___/     /_/  \\____/   /____/___/____/")
        self.echo(self.term.move(4, 1) + "                                                    v0.1.1")

    def drawBox(self, offset, size):
        style = "─│┌┐└┘"
        x, y = offset
        w, h = size

        first_line = style[2] + (style[0] * (w - 2)) + style[3]
        middle_line = style[1] + (" " * (w - 2)) + style[1]
        last_line = style[4] + (style[0] * (w - 2)) + style[5]

        self.echo(self.term.move(y, x) + first_line)
        for i in range(h):
            self.echo(self.term.move(y + i + 1, x) + middle_line)
        self.echo(self.term.move(y + h, x) + last_line)

    def waitForInput(self):
        self.input = self.term.inkey(timeout=0)
        self.echo(self.term.move(0, 85) + "input :" + self.input)

    def textWithColor(self, r,g,b,text):
        return self.term.color(int(self.rgbToAnsi256(r, g, b)))(text)

    def printAudio(self, y, audio_datas):
        self.echo(self.term.move(y, 1) + "audio" + audio_datas[0])

    # ------------------------------------------------------------------------------
    #  Name of the strip                                                      online
    #
    #  mode ---------- mirror - reverse - color - shape - time interval - brightness
    #
    #  █████████████████████████████████████████████████████████████████████████████
    # ------------------------------------------------------------------------------

    def printStrip(self, y, is_connected, strip_config, pixels):

       with self.term.hidden_cursor(), self.term.cbreak(), self.term.location():
            self.echo(self.term.move(y + 1, 2) + strip_config.name)
            self.echo(self.term.move(y + 1, 73) + "30 / 60")
            strip_config.active_visualizer_mode
            isConnected = self.textWithColor(0, 255, 0, 'online') if is_connected else self.textWithColor(255, 0, 0, 'offline')
            self.echo(self.term.move(y + 2, 73) + isConnected)
            mirrorMode = self.textWithColor(255, 255, 255, 'mirror') if strip_config.is_mirror else self.textWithColor(50, 50, 50, 'mirror')
            self.echo(self.term.move(y + 2, 2) + mirrorMode)
            reverseMode = self.textWithColor(255, 255, 255, 'reverse') if strip_config.is_reverse else self.textWithColor(50, 50, 50, 'reverse')
            self.echo(self.term.move(y + 2, 10) + reverseMode)

            array = self.getTermArrayFromPixels(pixels)
            self.echo(self.term.move(y + 5, 2) + array)

            self.echo(self.term.move(0, 0))

    def getTermArrayFromPixels(self, pixels):
        array = ""
        for i in range(len(pixels[0])):
            array += self.term.color(int(self.rgbToAnsi256(pixels[0][i], pixels[1][i], pixels[2][i])))('█')
        return array
