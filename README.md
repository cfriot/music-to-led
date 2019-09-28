# Audio Reactive LED Strip
Real-time LED strip music visualization using Python and Arduino via serial communication.

# Midi connection
This program is linked with Ableton live midi outputs to change visualizations mods

# TO DO
- App OSX package
- Refactor to finish
- Mix viz Effect
- Debug Synth mod

# Midi signals

Notes are clamped between -36 to 91 and gives us 127 possibilities
Velocities are campled between 1 and 127 and gives us also 127 possibilities

- Effects are in a range of 0 to 50

- Mods are in a range of 50 to 100

- Bpms are in a range of 100 to 110 and are using velocity

Example :
For a bpm of 150 you have to send the node 101 with 32 velocity ( 127 + 32 )
For a bpm of 280 you have to send the node 102 with 50 velocity ( 127 + 127 + 24 )

# Led number limitation

For the moment, the protocol is limited to 254 leds

# Powering leds strips
Each individual NeoPixel draws up to 60 milliamps at maximum brightness white (red + green + blue).

60 NeoPixels × 60 mA ÷ 1,000 = 3.6 Amps minimum
135 NeoPixels × 60 mA ÷ 1,000 = 8.1 Amps minimum
135 NeoPixels × 60 mA / 2 (for each led to 125,125,125) ÷ 1,000 = 4.05 Amps minimum

300 NeoPixels × 60 mA / 2 (for each led to 125,125,125) ÷ 1,000 = 4.05 Amps minimum

# Estimations on battery
Amp-hours are current over time. A 2,600 mAh (milliamp-hour) battery can be thought of as delivering 2.6 Amps continuously for one hour, or 1.3 Amps for 2 hours, and so forth. In reality, it’s not quite linear like that; most batteries have disproportionally shorter run times with a heavy load. Also, most batteries won’t take kindly to being discharged in an hour — this can even be dangerous! Select a battery sufficiently large that it will take at least a couple hours to run down. It’s both safer for you and better for the longevity of the battery.


# Installation for Computer
## Python Dependencies
Visualization code is compatible with Python 3.7. A few Python dependencies must also be installed:

### Installing dependencies with Anaconda
Install dependencies using pip and the conda package manager
```
conda install numpy scipy pyqtgraph colour psutil python-rtmidi
pip install pyaudio
```

# Ableton live and Midi channels

![abletonmidisettings](images/ableton-midi-settings-conf.png)
![osxmidisettings](images/osx-midi-settings-conf.png)


# License
This project was developed by Thibaud FRERE and is released under the MIT License.
