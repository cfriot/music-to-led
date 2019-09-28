from __future__ import print_function
from __future__ import division
import time
import config
import numpy as np
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtGui, QtCore

from audioFilters.dsp import ExpFilter, create_mel_bank


class AudioInterface:

    def __init__(self, visualization):

        self.app = QtGui.QApplication([])
        self.view = pg.GraphicsView()
        self.layout = pg.GraphicsLayout(border=(100, 100, 100))
        self.view.setCentralItem(self.layout)
        self.view.show()
        self.view.setWindowTitle("Visualization")
        self.view.resize(800, 600)
        self.visualization = visualization
        self.fft_plot_filter = ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                                         alpha_decay=0.5, alpha_rise=0.99)

        self.fft_plot = self.layout.addPlot(
            title='Filterbank Output', colspan=3)
        self.fft_plot.setRange(yRange=[-0.1, 1.2])
        self.fft_plot.disableAutoRange(axis=pg.ViewBox.YAxis)
        self.x_data = np.array(range(1, config.N_FFT_BINS + 1))
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
        self.x_data = np.array(range(1, config.N_PIXELS + 1))
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
            (config.MIN_FREQUENCY / (config.MIC_RATE / 2.0))**0.5)
        self.freq_slider.addTick(
            (config.MAX_FREQUENCY / (config.MIC_RATE / 2.0))**0.5)
        self.freq_slider.tickMoveFinished = self.freq_slider_change
        self.freq_label.setText('Frequency range: {} - {} Hz'.format(
            config.MIN_FREQUENCY,
            config.MAX_FREQUENCY))
        # # Effect selection
        self.active_color = '#16dbeb'
        self.inactive_color = '#FFFFFF'
        # # Layout
        self.layout.nextRow()
        self.layout.addItem(self.freq_label, colspan=3)
        self.layout.nextRow()
        self.layout.addItem(self.freq_slider, colspan=3)

    def freq_slider_change(self, tick):
        minf = self.freq_slider.tickValue(0)**2.0 * (config.MIC_RATE / 2.0)
        maxf = self.freq_slider.tickValue(1)**2.0 * (config.MIC_RATE / 2.0)
        t = 'Frequency range: {:.0f} - {:.0f} Hz'.format(minf, maxf)
        self.freq_label.setText(t)
        config.MIN_FREQUENCY = minf
        config.MAX_FREQUENCY = maxf
        create_mel_bank()

    def drawFrame(self):
        # Plot filterbank output
        self.x = np.linspace(config.MIN_FREQUENCY, config.MAX_FREQUENCY, len(
            self.visualization.audio_data))
        self.mel_curve.setData(x=self.x, y=self.fft_plot_filter.update(
            self.visualization.audio_data))
        # Plot the color channels
        self.r_curve.setData(y=self.visualization.pixels[0])
        self.g_curve.setData(y=self.visualization.pixels[1])
        self.b_curve.setData(y=self.visualization.pixels[2])
        self.app.processEvents()
