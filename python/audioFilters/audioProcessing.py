import config
import time
from scipy.ndimage.filters import gaussian_filter1d
from audioFilters.dsp import *

fft_plot_filter = ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                            alpha_decay=0.5, alpha_rise=0.99)
mel_gain = ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                     alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                          alpha_decay=0.5, alpha_rise=0.99)
fft_window = np.hamming(int(config.MIC_RATE / config.FPS)
                        * config.N_ROLLING_HISTORY)
samples_per_frame = int(config.MIC_RATE / config.FPS)


class AudioProcessing():
    def __init__(self):
        self.y_roll = np.random.rand(
            config.N_ROLLING_HISTORY, samples_per_frame) / 1e16

    def render(self, audio_samples):
        # Sound case
        # Normalize samples between 0 and 1
        y = audio_samples / 2.0**15
        # Construct a rolling window of audio samples
        self.y_roll[:-1] = self.y_roll[1:]
        self.y_roll[-1, :] = np.copy(y)
        y_data = np.concatenate(self.y_roll, axis=0).astype(np.float32)
        vol = np.max(np.abs(y_data))

        if vol < config.MIN_VOLUME_THRESHOLD:
            # print('No audio input. Volume below threshold. Volume:', vol)
            return np.tile(0., config.N_FFT_BINS)
        else:
            # Transform audio input into the frequency domain
            N = len(y_data)
            N_zeros = 2**int(np.ceil(np.log2(N))) - N
            # Pad with zeros until the next power of two
            y_data *= fft_window
            y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
            YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
            # Construct a Mel filterbank from the FFT data
            mel = np.atleast_2d(YS).T * mel_y.T
            # Scale data to values more suitable for visualization
            # mel = np.sum(mel, axis=0)
            mel = np.sum(mel, axis=0)
            mel = mel**2.0
            # Gain normalization
            mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
            mel /= mel_gain.value
            mel = mel_smoothing.update(mel)
            return mel
