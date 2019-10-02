"""Settings for audio reactive LED strip"""
from __future__ import print_function
from __future__ import division
import os

ginger_strips_shape = [
    [34, 52, 50],
    [16, 16, 26, 26, 24, 24]
]

data = {
    "audio_ports": [
        {
            "name": "Built-in Microphone",
            "min_frequency": 200,
            "max_frequency": 12000,
        },
        # {
        #     "name": "Background Music",
        #     "min_frequency": 200,
        #     "max_frequency": 12000,
        # }
    ],
    "midi_ports": [
        "Ableton-virtual-midi-ouput ChangeMod",
        "Ableton-virtual-midi-ouput LeftSynth",
        "Ableton-virtual-midi-ouput RightSynth"
    ],
    "strips": [
        {
            "serial_port_name": "/dev/tty.usbserial-14210",
            "active_audio_channel": 0,
            "associated_midi_channels": ["Ableton-virtual-midi-ouput RightSynth"],
            "strip_shapes": [
                [62, 62, 62, 62],
                [126, 126],
            ],
            "active_visualizer": "scroll",
            "strip_mods": {
                "is_full_strip": False,
                "is_reverse": False,
                "is_mirror": True,
                "is_monochromatic": False
            }
        },
        {
            "serial_port_name": "/dev/tty.usbserial-14220",
            "active_audio_channel": 0,
            "associated_midi_channels": ["Ableton-virtual-midi-ouput LeftSynth"],
            "strip_shapes": [
                [62, 62, 62, 62],
                [126, 126],
            ],
            "active_visualizer": "scroll",
            "strip_mods": {
                "is_full_strip": False,
                "is_reverse": False,
                "is_mirror": True,
                "is_monochromatic": False
            }
        },
        {
            "serial_port_name": "/dev/tty.usbserial-14230",
            "active_audio_channel": 0,
            "associated_midi_channels": [],
            "strip_shapes": [
                [62, 62, 62, 62],
                [126, 126],
            ],
            "active_visualizer": "scroll",
            "strip_mods": {
                "is_full_strip": False,
                "is_reverse": False,
                "is_mirror": True,
                "is_monochromatic": False
            }
        }
    ]
}


N_PIXELS = 252
"""Number of pixels in the LED strip"""

DISPLAY_SHELL_INTERFACE = False
"""Display the Ncurse shell interface"""

DISPLAY_AUDIO_INTERFACE = False
"""Display the Qt interface to debug audio curves"""

MIC_RATE = 44100
"""Sampling frequency of the microphone in Hz"""

DISPLAY_FPS = False
"""Whether to display the FPS when running (can reduce performance)"""

FPS = 100
"""Desired refresh rate of the visualization (frames per second)

FPS indicates the desired refresh rate, or frames-per-second, of the audio
visualization. The actual refresh rate may be lower if the computer cannot keep
up with desired FPS value.

Higher framerates improve "responsiveness" and reduce the latency of the
visualization but are more computationally expensive.

Low framerates are less computationally expensive, but the visualization may
appear "sluggish" or out of sync with the audio being played if it is too low.

The FPS should not exceed the maximum refresh rate of the LED strip, which
depends on how long the LED strip is.
"""

_max_led_FPS = int(((N_PIXELS * 30e-6) + 50e-6)**-1.0)
assert FPS <= _max_led_FPS, 'FPS must be <= {}'.format(_max_led_FPS)

MIN_FREQUENCY = 200
"""Frequencies below this value will be removed during audio processing"""

MAX_FREQUENCY = 12000
"""Frequencies above this value will be removed during audio processing"""

N_FFT_BINS = 24
"""Number of frequency bins to use when transforming audio to frequency domain

Fast Fourier transforms are used to transform time-domain audio data to the
frequency domain. The frequencies present in the audio signal are assigned
to their respective frequency bins. This value indicates the number of
frequency bins to use.

A small number of bins reduces the frequency resolution of the visualization
but improves amplitude resolution. The opposite is true when using a large
number of bins. More bins is not always better!

There is no point using more bins than there are pixels on the LED strip.
"""

N_ROLLING_HISTORY = 4
"""Number of past audio frames to include in the rolling window"""

MIN_VOLUME_THRESHOLD = 1e-7
"""No music visualization displayed if recorded audio volume below threshold"""
