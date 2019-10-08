import time
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

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

class AudioProcessing():
    def __init__(self):

        self.samples_per_frame = int(MIC_RATE / FPS)
        self.y_roll = np.random.rand(
            N_ROLLING_HISTORY, self.samples_per_frame) / 1e16

        self.fft_plot_filter = ExpFilter(
            np.tile(1e-1, N_FFT_BINS),
            alpha_decay = 0.5,
            alpha_rise = 0.99
        )

        self.mel_gain = ExpFilter(
            np.tile(1e-1, N_FFT_BINS),
            alpha_decay = 0.01,
            alpha_rise = 0.99
        )

        self.mel_smoothing = ExpFilter(
            np.tile(1e-1, N_FFT_BINS),
            alpha_decay = 0.5,
            alpha_rise = 0.99
        )

        self.fft_window = np.hamming(
            int(MIC_RATE / FPS) * N_ROLLING_HISTORY
        )


    @staticmethod
    def rfft(data, window = None):
        """Real-Valued Fast Fourier Transform"""
        window = 1.0 if window is None else window(len(data))
        ys = np.abs(np.fft.rfft(data * window))
        xs = np.fft.rfftfreq(len(data), 1.0 / MIC_RATE)
        return xs, ys


    @staticmethod
    def fft(data, window = None):
        """Fast Fourier Transform"""
        window = 1.0 if window is None else window(len(data))
        ys = np.fft.fft(data * window)
        xs = np.fft.fftfreq(len(data), 1.0 / MIC_RATE)
        return xs, ys


    def render(self, audio_samples):
        # Sound case
        # Normalize samples between 0 and 1
        y = audio_samples / 2.0**15
        # Construct a rolling window of audio samples
        self.y_roll[:-1] = self.y_roll[1:]
        self.y_roll[-1, :] = np.copy(y)
        y_data = np.concatenate(self.y_roll, axis=0).astype(np.float32)
        vol = np.max(np.abs(y_data))

        if vol < MIN_VOLUME_THRESHOLD:
            # print('No audio input. Volume below threshold. Volume:', vol)
            return np.tile(0., N_FFT_BINS)
        else:
            # Transform audio input into the frequency domain
            N = len(y_data)
            N_zeros = 2**int(np.ceil(np.log2(N))) - N
            # Pad with zeros until the next power of two
            y_data *= self.fft_window
            y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
            YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
            # Construct a Mel filterbank from the FFT data
            mel = np.atleast_2d(YS).T * mel_y.T
            # Scale data to values more suitable for visualization
            mel = np.sum(mel, axis=0)
            mel = mel**2.0
            # Gain normalization
            self.mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
            mel /= self.mel_gain.value
            mel = self.mel_smoothing.update(mel)
            return mel
