from __future__ import print_function
from __future__ import division
import time
import numpy as np
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

from helpers.audio.expFilter import ExpFilter
from helpers.audio.melbank import Melbank

N_FFT_BINS = 24
N_ROLLING_HISTORY = 4
FPS = 60
MIC_RATE = 44100
MIN_FREQUENCY = 200
MAX_FREQUENCY = 12000
MIN_VOLUME_THRESHOLD = 1e-7

def create_mel_bank():
    global samples, mel_y, mel_x
    samples = int(MIC_RATE *
                  N_ROLLING_HISTORY / (2.0 * FPS))
    mel_y, (_, mel_x) = Melbank.compute_melmat(
        num_mel_bands = N_FFT_BINS,
        freq_min = MIN_FREQUENCY,
        freq_max = MAX_FREQUENCY,
        num_fft_bands = samples,
        sample_rate = MIC_RATE
    )

samples = None
mel_y = None
mel_x = None
create_mel_bank()

class AudioInterface:

    def __init__(self, visualization, config, index):

        self.config = config
        self.strip_config = config.strips[index]
        self.audio_class = config.audio_ports[0]


        self.app = QtGui.QApplication([])
        self.view = pg.GraphicsView()
        self.layout = pg.GraphicsLayout(border=(100, 100, 100))
        self.view.setCentralItem(self.layout)
        self.view.show()
        self.view.setWindowTitle("Visualization")
        self.view.resize(800, 600)
        self.visualization = visualization
        self.fft_plot_filter = ExpFilter(np.tile(1e-1, config.number_of_audio_samples),
                                         alpha_decay=0.5, alpha_rise=0.99)

        self.fft_plot = self.layout.addPlot(
            title='Filterbank Output', colspan=3)
        self.fft_plot.setRange(yRange=[-0.1, 1.2])
        self.fft_plot.disableAutoRange(axis=pg.ViewBox.YAxis)
        self.x_data = np.array(range(1, N_FFT_BINS + 1))
        self.mel_curve = pg.PlotCurveItem()
        self.mel_curve.setData(x=self.x_data, y=self.x_data * 0)
        self.fft_plot.addItem(self.mel_curve)
        # # Visualization plot
        self.layout.nextRow()
        self.led_plot = self.layout.addPlot(
            title='Visualization Output', colspan=3)
        self.led_plot.setRange(yRange=[-5, 260])
        self.led_plot.disableAutoRange(axis=pg.ViewBox.YAxis)
        # # Pen for each of the color channel curves
        self.r_pen = pg.mkPen((255, 30, 30, 200), width=4)
        self.g_pen = pg.mkPen((30, 255, 30, 200), width=4)
        self.b_pen = pg.mkPen((30, 30, 255, 200), width=4)
        # # Color channel curves
        self.r_curve = pg.PlotCurveItem(pen=self.r_pen)
        self.g_curve = pg.PlotCurveItem(pen=self.g_pen)
        self.b_curve = pg.PlotCurveItem(pen=self.b_pen)
        # # Define x data
        self.x_data = np.array(range(1, visualization.number_of_pixels + 1))
        self.r_curve.setData(x=self.x_data, y=self.x_data * 0)
        self.g_curve.setData(x=self.x_data, y=self.x_data * 0)
        self.b_curve.setData(x=self.x_data, y=self.x_data * 0)
        # # Add curves to plot
        self.led_plot.addItem(self.r_curve)
        self.led_plot.addItem(self.g_curve)
        self.led_plot.addItem(self.b_curve)
        # # Frequency range label
        self.freq_label = pg.LabelItem('')

        self.freq_slider = pg.TickSliderItem(
            orientation='bottom', allowAdd=False)
        self.freq_slider.addTick(
            (MIN_FREQUENCY / (MIC_RATE / 2.0))**0.5)
        self.freq_slider.addTick(
            (MAX_FREQUENCY / (MIC_RATE / 2.0))**0.5)
        self.freq_slider.tickMoveFinished = self.freq_slider_change
        self.freq_label.setText('Frequency range: {} - {} Hz'.format(
            MIN_FREQUENCY,
            MAX_FREQUENCY))
        # # Effect selection
        self.active_color = '#16dbeb'
        self.inactive_color = '#FFFFFF'
        # # Layout
        self.layout.nextRow()
        self.layout.addItem(self.freq_label, colspan=3)
        self.layout.nextRow()
        self.layout.addItem(self.freq_slider, colspan=3)

    def freq_slider_change(self, tick):
        minf = self.freq_slider.tickValue(0)**2.0 * (MIC_RATE / 2.0)
        maxf = self.freq_slider.tickValue(1)**2.0 * (MIC_RATE / 2.0)
        t = 'Frequency range: {:.0f} - {:.0f} Hz'.format(minf, maxf)
        self.freq_label.setText(t)
        MIN_FREQUENCY = minf
        MAX_FREQUENCY = maxf
        create_mel_bank()

    def drawFrame(self):
        # Plot filterbank output
        self.x = np.linspace(MIN_FREQUENCY, MAX_FREQUENCY, len(
            self.visualization.audio_data))
        self.mel_curve.setData(x=self.x, y=self.fft_plot_filter.update(
            self.visualization.audio_data))
        # Plot the color channels
        self.r_curve.setData(y=self.visualization.pixels[0])
        self.g_curve.setData(y=self.visualization.pixels[1])
        self.b_curve.setData(y=self.visualization.pixels[2])
        self.app.processEvents()
