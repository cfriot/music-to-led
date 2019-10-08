import logging
import psutil
import os
import sys
import time
import curses
from functools import wraps

import config
from audioFilters.dsp import *

from helpers.framerateCalculator import FramerateCalculator

class StdOutWrapper:
    def __init__(self):
        self.text = ""

    def write(self, txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])

    def get_text(self):
        return self.text[:30]
        # return '\n'.join(self.text.split('\n')[:20])


class DebugInterface:

    def __init__(self, visualization):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.curs_set(0)                  # hide the cursor
        self.y, self.x = self.stdscr.getmaxyx()  # get size
        self.framerateCalculator = FramerateCalculator()
        self.stdOutWrapper = StdOutWrapper()
        sys.stdout = self.stdOutWrapper
        sys.stderr = self.stdOutWrapper
        self.visualization = visualization

    def __del__(self):
        self = self
        curses.curs_set(1)
        curses.echo()
        curses.endwin()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def drawFrame(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.erase()
        self.stdscr.border(0)
        self.stdscr.addstr(1, 2, "──────────────────────────────")
        self.stdscr.addstr(2, 2, "─── LED VISUALIZATION V0.1 ───")
        self.stdscr.addstr(3, 2, "──────────────────────────────")
        self.stdscr.addstr(5, 2, "Cpu in % -> " + str(getCpuInPercent()))
        self.stdscr.addstr(6, 2, "Mem in % -> " +
                           str(getVirtualMemoryConsumtion()["percent"]))
        print(str(getVirtualMemoryConsumtion()))
        self.stdscr.addstr(7, 2, "FPS -> " +
                           self.framerateCalculator.getFps())
        self.stdscr.addstr(9, 2, "Current mode -> " +
                           self.visualization.active_mod)
        self.stdscr.addstr(11, 2, "Is reverse -> " +
                           str(self.visualization.is_reverse))
        self.stdscr.addstr(12, 2, "Is full strip -> " +
                           str(self.visualization.is_full_strip))
        self.stdscr.addstr(13, 2, "Is monochrome -> " +
                           str(self.visualization.is_monochrome))
        self.stdscr.addstr(14, 2, "Is mirror -> " +
                           str(self.visualization.is_mirror))
        self.stdscr.addstr(18, 2, "StdOut -> " + self.stdOutWrapper.get_text())
        self.stdscr.refresh()

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def getCpuInPercent():
    return psutil.cpu_percent()


def getVirtualMemoryConsumtion():
    return dict(psutil.virtual_memory()._asdict())


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              (function.func_name, str(t1 - t0))
              )
        return result
    return function_timer
