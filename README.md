# Real-time Audio and Midi LED Strip animations via Serial

Real-time LED strip music and midi visualization using Python and Arduino via serial communication.

# How it works ?

It takes multiple audio and midi inputs, use them to make awesome visualizations effects and output the result in multiple led strips via a serial protocol.

# Features

- Multiple audio inputs
- Multiple midi inputs
- Multiple led strips
- Live config changer using dedicated MIDI channel
- Multiple "virtual" strip shapes
- Multiple color schemes
- Revese and mirror mods
- 8 Vizualizer Effects


# Table of contents

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

## Python program
Code is compatible with Python 3.7. Install dependencies using pip and the conda package manager.

```
pip install -r requirements.txt
conda install --file requirements.txt
```

## Arduino part

### Electronic scheme

![electronic-scheme](../images/electronic-scheme.png)

### Component list

- 1x [Alim 5V 10A](https://www.amazon.fr/gp/product/B06XCMQ212/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- 1x Arduino nano or other
- 1x 1000mu Capacitor
- 1x [Led strip connector](https://www.amazon.fr/BTF-LIGHTING-Connectors-WS2812B-WS2811-20pairs/dp/B01DC0KIT2/ref=sr_1_19?__mk_fr_FR=ÅMÅŽÕÑ&keywords=led+strip+connector&qid=1569857203&s=lighting&sr=1-19)
- 1x Led strip WS2812B

### 3d printed case

![arduino-case](../images/arduino-case.png)

### Led number limitation

It depends on two factors :
  - Your board maximum baud rate
  - Your led alimentation

In this case i prefer to not use more than 255 leds for each arduino


## Configuration file

### Audio channels
...
### Strips
...
#### Midi channels
...

# TO-DO

- Electron package with a web interface
- Remote control for changing modes ( via DMX ? )
- Ability to mix effects

# Links

- https://fr.wikipedia.org/wiki/DMX_(%C3%A9clairage)

# License
This project was developed by Thibaud FRERE and is released under the MIT License.
