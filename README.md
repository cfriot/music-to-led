# Real-time Audio and Midi LED Strip animations via Serial

Real-time LED strip music and midi visualization using Python and Arduino via serial communication.

# How it works ?

It takes multiple audio and midi inputs, use them to make awesome visualizations effects and output the result in multiple led strips via a serial protocol.


# Table of contents

- [Features](#features)
- [Effects and mods](#effects-and-mods)
  * [Effects](#effects)
    + [Audio based](#audio-based)
    + [Midi based](#midi-based)
    + [Bpm based](#bpm-based)
    + [Generic](#generic)
  * [Mods](#mods)
- [Install](#install)
- [Arduino part](#arduino-part)
- [Configuration](#configuration)
  * [Ableton live](#ableton-live)
    + [Midi channel configuration](#midi-channel-configuration)
- [TO-DO](#TO-DO)
- [Links](#links)
- [License](#license)

# Features

- Multiple audio inputs
- Multiple midi inputs
- Multiple led strips
- Live config changer using dedicated MIDI channel
- Multiple "virtual" strip shapes
- Multiple color schemes
- Revese and mirror mods
- 8 Vizualizer Effects


# Effects and mods

## Effects

### Audio based

- 0 : Scroll
- 1 : Energy
- 2 : IntensityChannels
- 3 : Spectrum

### Midi based

- 5 : Piano
- 6 : Piano2
- 7 : Envelope

### Bpm based

- 9 : AlternateColors
- 10 : AlternateColorsFull
- 11 : AlternateColorsForStrips

### Generic

- 13 : Full
- 14 : Nothing


## Mods

- 16 : Reset Frame

- 18 : (Boolean) Reverse
- 19 : (Boolean) Mirror

- 21 : (Array) Shapes
- 22 : (Array) Color schemes
- 23 : (Int) Bpm
- 24 : (Int) Audio channel


# Install

Code is compatible with Python 3.7. Install dependencies using pip and the conda package manager.

```
pip install -r requirements.txt
conda install --file requirements.txt
```

# Arduino part

[Electronic part](arduino/README.md)


# Configuration

## Ableton live

### Midi channel configuration

The config file called ports MUST match the created and open ports.

![abletonmidisettings](images/ableton-midi-settings-conf.png)
![osxmidisettings](images/osx-midi-settings-conf.png)

# TO-DO

- Electron package with a web interface
- Remote control for changing modes ( via DMX ? )
- Ability to mix effects

# Links

- https://fr.wikipedia.org/wiki/DMX_(%C3%A9clairage)

# License
This project was developed by Thibaud FRERE and is released under the MIT License.
