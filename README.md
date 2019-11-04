
<img src="images/logo.svg" width="300">

![code-covergage](https://img.shields.io/badge/Code%20coverage-0%20%25-red)

Real-time music and midi visualizations on led strips using Python, Electron and Arduino.

# How it works ?

1. Handle multiple audio and midi inputs
2. Use them to make awesome visualizations effects
3. Output the result on multiple led strips via Arduino based controllers

<!-- Audio channels are used as a source for some effects.
Midi channels are used as a source for effect AND as a mod changer. -->

![software-architecture](images/archi.png)

# What do i need to make one ?

1. Install the program
2. Create an arduino box
...

# Table of contents

- [Effects & Modes](#effects---modes)
  * [Effects](#effects)
    + [Sound based](#sound-based)
    + [Midi based](#midi-based)
    + [BPM based](#bpm-based)
    + [Generic](#generic)
  * [Modes](#modes)
- [Configuration](#configuration)
  * [Audio channels](#audio-channels)
  * [Virtual Audio Source](#virtual-audio-source)
    + [Linux](#linux)
    + [OSX](#osx)
  * [Midi channels](#midi-channels)
    + [OSX](#osx-1)
    + [Ableton live](#ableton-live)
  * [CONFIG.yml](#configyml)
- [Install](#install)
  * [Python program](#python-program)
  * [Arduino part](#arduino-part)
    + [Electronic scheme](#electronic-scheme)
    + [Component list](#component-list)
    + [3d printed case](#3d-printed-case)
    + [Led number limitation](#led-number-limitation)
- [Contribute](#contribute)
- [License](#license)

# Effects & Modes

## Effects

There is four kind of effects. All the examples are based on a ["red", "green", "blue"] color scheme

### Sound based

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 0 | C-2 | **Scroll** | - | ![scroll](images/scroll.gif)
| 1 | C#-2 | **Energy** | - | ![energy](images/energy.gif)
| 2 | D-2 | **Intensity** | - | ![intensity](images/intensity.gif)
| 3 | D#-2 | **Spectrum** | - | ![spectrum](images/spectrum.gif)

### Midi based

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 5 | F-2   | **Piano** | - | ![scroll](images/piano.gif)
| 6 | F#-2  | **Envelope** | Color intensity based on pitch bend | ![scroll](images/envelope.gif)
| 7 | G-2   | - | - | ![scroll](images/nothing.gif)
| 8 | G#-2  | - | - | ![scroll](images/nothing.gif)

### BPM based

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 10 | A#-2   | **AlternateColors** | Chunk size based on velocity | ![scroll](images/alternate-chunks.gif)
| 11 | B-2    | **AlternateColorsFull** | - | ![scroll](images/alternate-colors.gif)
| 12 | C-1    | **AlternateColorsForStrips** | - | ![scroll](images/alternate-strips.gif)
| 13 | C#-1   | - | - | ![scroll](images/nothing.gif)

### Generic

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 15 | D#-1  | **Full** | - | ![scroll](images/full.gif)
| 16 | E-1   | **Nothing** | - | ![scroll](images/nothing.gif)
| 17 | F-1  | **Fire** | - | ![scroll](images/fire.gif)
| 18 | F#-1  | - | - | ![scroll](images/nothing.gif)

## Modes

| *Number* | *Midi Note* | *Mode name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 20 | G#-1  | **Toggle reverse mode** | - | ![scroll](images/reverse.gif)
| 21 | A-1  | **Toggle mirror mode** | - | ![scroll](images/mirror.gif)
| 22 | A#-1 | **Change shape** | Size based on velocity | ![scroll](images/shape.gif)
| 23 | B-1 | **Change color scheme** | Size based on velocity | ![scroll](images/color.gif)
| 24 | C-0  | **Change bpm** | Size based on velocity | ![scroll](images/nothing.gif)
| 25 | C#-0  | **Change Audio channel** | Size based on velocity | ![scroll](images/nothing.gif)
| 26 | D-0 | **Reset Frame** | - | ![scroll](images/nothing.gif)
| 27 | D#-0 | - | - | ![scroll](images/nothing.gif)


# Configuration

## Audio channels

The program streams audio from the default audio input device (set by the operating system).

Examples of typical audio sources:
- Audio cable connected to the audio input jack (requires USB sound card on Raspberry Pi)
- Webcam microphone, headset, studio recording microphone, etc

## Virtual Audio Source
You can use a "virtual audio device" to transfer audio playback from one application to another. This means that you can play music on your computer and connect the playback directly into the program.

### Linux
Linux users can use [Jack Audio](http://jackaudio.org/) to create a virtual audio device.

### OSX
On OSX, [Loopback](https://www.rogueamoeba.com/loopback/) can be use to create a virtual audio device.

## Midi channels

### OSX

![osx-midi-settings](images/osx-midi-settings.png)

### Ableton live

![ableton-midi-settings](images/ableton-midi-settings.png)

...

## CONFIG.yml

```yml
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
        name: Led strip name
        serial_port_name: /dev/tty.usbserial-14210
        max_brightness: 255
        associated_midi_channels:
          - Audio2Led Synth
        midi_ports_for_changing_mode:
          - Audio2Led ChangeMod
        is_reverse: false
        is_mirror: false
        bpm: 120

        # Be sure that real_shape and shapes only contains even numbers
        # It may cause crash if it's not the case

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

```


# Install

If you encounter any problems running program, please open a new issue. Also, please consider opening an issue if you have any questions or suggestions for improving the installation process.

## Python program
Code is compatible with Python 3.7. Install dependencies using pip and the conda package manager.

```
pip install -r requirements.txt
conda install --file requirements.txt
```

## Arduino part

You can find 3d models of the cases, the arduino code and all the instructions you need to setup the project. [Arduino part](/arduino/).

### Electronic scheme

![electronic-scheme](images/electronic-scheme.png)

### Component list

- 1x [**Alim 5V 10A**](https://www.amazon.fr/gp/product/B06XCMQ212/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)  *~25$*
- 1x **Arduino nano or other**  *~5$*
- 1x **1000mu Capacitor**  *~1$*
- 1x [**Led strip female connector**](https://www.amazon.fr/BTF-LIGHTING-Connectors-WS2812B-WS2811-20pairs/dp/B01DC0KIT2)  *~5$*
- 1x **Led strip WS2812B**  *~35$*

**Estimated cost** *~100$*

### 3d printed case

![arduino-case](images/arduino-case.png)

### Led number limitation

It depends on two factors :
 - Your board maximum baud rate
 - Your led alimentation

For now, consider not using more than 254 leds.

<!-- # Links
- [Wikipedia DMX](https://fr.wikipedia.org/wiki/DMX_(%C3%A9clairage) -->

<!--

  TO DO BEFORE RELEASE

  - Package app electron and python
  - Make a good readme
  - Toggle interface
  -




  # MAVEN besoins

  # Grosse saturation de ouf
  # Utiliser le mouvement de l'onde de la batterie pour les leds
  # entre 50 et 110 Decibels
  # Variations sur les gros applats de notes
  # Gestion des modulateurs pour piano ?
  # Gestion de la vélocité pour Piano

  # Mode piano post rock


  # Windows compatibility

  # General needs

  # Make a more resilient midi code

  # 27 novembre


 -->

# Contribute
Feel free to send me an e-mail or submit a pull request.

# License
This project was developed by Thibaud FRERE and is released
under the MIT License.
