
# Real-time Audio and Midi based LED Strip animations

Real-time LED strip music and midi visualization using Python and Arduino via serial communication.

# How it works ?

It takes multiple audio and midi inputs, use them to make awesome visualizations effects and output the result in multiple led strips via a serial protocol.

**Features**

- Multiple audio inputs
- Multiple midi inputs
- Multiple led strips
- Live config changer using dedicated MIDI channels
- Multiple "virtual" strip shapes
- Multiple color schemes
- Revese and mirror mods
- 8 Vizualizer Effects


![software-architecture](images/archi.png)

- [Features](#features)
  * [Effects](#effects)
    + [Sound based](#sound-based)
    + [Midi based](#midi-based)
    + [BPM based](#bpm-based)
    + [Generic](#generic)
  * [Mods](#mods)
- [Configuration](#configuration)
  * [Audio channels](#audio-channels)
  * [Midi channels](#midi-channels)
  * [CONFIG.yml](#configyml)
- [Install](#install)
  * [Python program](#python-program)
  * [Arduino part](#arduino-part)
    + [Electronic scheme](#electronic-scheme)
    + [Component list](#component-list)
    + [3d printed case](#3d-printed-case)
    + [Led number limitation](#led-number-limitation)
- [Links](#links)
- [License](#license)

# Features

## Effects

### Sound based

| *Number* | *Midi Note* | *Effect name* | *Params*
|:--|:--|:--|:--
| 0 | C-0 | **Scroll** | -
| 1 | C#-2 | **Energy** | -
| 2 | D-2 | **Intensity** | -
| 3 | D#-2 | **Spectrum** | -

Add gif to explain

### Midi based

| *Number* | *Midi Note* | *Effect name* | *Params*
|:--|:--|:--|:--
| 5 | F-2   | **Piano** | -
| 6 | F#-2  | **Envelope** | Based on pitch bend
| 7 | G-2   | - | -
| 8 | G#-2  | - | -

### BPM based

| *Number* | *Midi Note* | *Effect name* | *Params*
|:--|:--|:--|:--
| 10 | A#-2   | **AlternateColors** | Size based on velocity
| 11 | B-2    | **AlternateColorsFull** | -
| 12 | C-1    | **AlternateColorsForStrips** | -
| 13 | C#-1   | - | -

### Generic

|Number | Midi Note | Effect name | Params
|:--|:--|:--|:--
| 15 | D#-1  | **Full** | -
| 16 | E-1   | **Nothing** | -
| 17 | F-1  | **Fire** | -
| 18 | F#-1  | - | -

## Mods

| *Number* | *Midi Note* | *Mod name* | *Params*
|:--|:--|:--|:--
| 20 | G#-1  | **Reverse mode** | -
| 21 | A-1  | **Mirror mode** | -
| 22 | A#-1 | **Shapes** | based on velocity
| 23 | B-1 | **Color schemes** | based on velocity
| 24 | C-0  | **Bpm** | based on velocity
| 25 | C#-0  | **Audio channel** | based on velocity
| 26 | D-0 | **Reset Frame** | -
| 27 | D#-0 | - | -


# Configuration

## Audio channels

...

## Midi channels

![osx-midi-settings](images/osx-midi-settings.png)

### Ableton live

![ableton-midi-settings](images/ableton-midi-settings.png)

...

## CONFIG.yml

    ---  # document start

    fps: 60

    display_shell_interface: false
    display_audio_interface: false

    n_rolling_history: 4
    number_of_audio_samples: 24

    audio_ports:
      -
        name: Built-in Microphone
        min_frequency: 200
        max_frequency: 12000
        sampling_rate: 44000
        number_of_audio_samples: 24
        min_volume_threshold: 1e-7

    strips:
      -
        name: Led Strip
        serial_port_name: /dev/tty.usbserial-14210
        max_brightness: 120
        associated_midi_channels:
          - Audio2Led Synth
        midi_ports_for_changing_mode:
          - Audio2Led ChangeMod
        is_reverse: false
        is_mirror: true
        bpm: 120
        real_shape:
          - 252
        shapes:
          -
            - 126
            - 126
          -
            - 62
            - 62
            - 62
            - 62

        color_schemes:
          # pink blue
          -
            - "#FF00C8"
            - "#00EDFF"
          # orange blue
          -
            - "#FFA200"
            - "#00C6FF"
          # red green
          -
            - "#FF002E"
            - "#00FFA4"
          # purple green
          -
            - "#F900FF"
            - "#22FF00"
          # blue yellow
          -
            - "#0024FF"
            - "#FFE500"
          -
            - red
            - green
            - blue
          -
            - red
          -
            - green
          -
            - blue
          -
            - white

        active_audio_channel_index: 0
        active_shape_index: 0
        active_color_index: 0
        active_color_scheme_index: 0
        active_visualizer_effect: scroll

    ...  # document end



# Install

## Python program
Code is compatible with Python 3.7. Install dependencies using pip and the conda package manager.

```
pip install -r requirements.txt
conda install --file requirements.txt
```

## Arduino part

You can find 3d models of the cases [there](/arduino/) and the arduino code for each protocol is [there](/arduino/)

### Electronic scheme

![electronic-scheme](images/electronic-scheme.png)

### Component list

- 1x [Alim 5V 10A](https://www.amazon.fr/gp/product/B06XCMQ212/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- 1x Arduino nano or other
- 1x 1000mu Capacitor
- 1x [Led strip female connector](https://www.amazon.fr/BTF-LIGHTING-Connectors-WS2812B-WS2811-20pairs/dp/B01DC0KIT2/ref=sr_1_19?__mk_fr_FR=ÅMÅŽÕÑ&keywords=led+strip+connector&qid=1569857203&s=lighting&sr=1-19)
- 1x Led strip WS2812B

### 3d printed case

![arduino-case](images/arduino-case.png)

### Led number limitation

It depends on two factors :
 - Your board maximum baud rate
 - Your led alimentation

For now, consider not using more than 254 leds.

# Links

- [Wikipedia DMX](https://fr.wikipedia.org/wiki/DMX_(%C3%A9clairage)

# License
This project was developed by Thibaud FRERE and is released
under the MIT License.
