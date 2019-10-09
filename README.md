# Audio Reactive LED Strip
Real-time LED strip music visualization using Python and Arduino via serial communication.
This program is linked with Ableton live midi outputs to change visualizations mods

## TO DO
- App OSX package
- Visualization effect mixer
- More control for Ableton Live
- Finish debug shell and audio interfaces

# Features
- Multiple led strips
- Multiple audio inputs
- Multiple midi inputs
- Multi shapes gesture
- Multi color schemes gesture
- Revese and mirror mods
- 8 Vizualizer Effects

# Effects and mods

## Effects

- Scroll
- Energy
- Piano ( that reflect notes played in the associated midi channels )
- IntensityChannels
- AlternateColors
- Full
- NeonFadeIn
- Nothing

## Mods

- Reverse
- Mirror
- Shapes
- Color schemes

# Computer

## Python program
Visualization code is compatible with Python 3.7. A few Python dependencies must also be installed:

### Installing dependencies with Anaconda
Install dependencies using pip and the conda package manager

```
pip install -r requirements.txt
conda install --file requirements.txt
```

## Ableton live

### Midi channel configuration

The config file called ports MUST match the created and open ports.

![abletonmidisettings](images/ableton-midi-settings-conf.png)
![osxmidisettings](images/osx-midi-settings-conf.png)

### Midi signals -- Not implemented yet

Notes are clamped between -36 to 91 and gives us 127 possibilities
Velocities are campled between 1 and 127 and gives us also 127 possibilities

- Effects are in a range of 0 to 50
- Mods are in a range of 50 to 100
- Bpms are in a range of 100 to 110 and are using velocity

Example :
For a bpm of 150 you have to send the node 101 with 32 velocity ( 127 + 32 )
For a bpm of 280 you have to send the node 102 with 50 velocity ( 127 + 127 + 24 )

# Viz functions

Scroll and energy are forked from
audio-reactive-led-strip project

# Links

- https://fr.wikipedia.org/wiki/DMX_(%C3%A9clairage)

# License
This project was developed by Thibaud FRERE and is released under the MIT License.
