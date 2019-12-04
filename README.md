
<p align="center">
  <a href="https://github.com/tfrere/music-2-led" title="haxe.org"><img src="images/logo.svg" width="400"></a>
</p>

<p align="center">
	<a href="https://github.com/tfrere/music-2-led#licence"><img src="https://img.shields.io/badge/licence-MIT-green" alt="Licence"></a>
	<a href="https://github.com/tfrere/music-2-led"><img src="https://img.shields.io/badge/platform-osx--64%20%7C%20linux--64%20%7C%20win--64-lightgrey" alt="Platform support"></a>
  <a href="https://github.com/tfrere/music-2-led"><img src="https://img.shields.io/github/last-commit/tfrere/music-2-led" alt="Last update"></a>
<a href="https://github.com/tfrere/music-2-led"><img src="https://img.shields.io/github/v/tag/tfrere/music-2-led" alt="Current version"></a>
</p>

#

**Music 2 Led** is an open source program that allows you to create **real-time audio and midi visualizations on led strips** using Arduino, Electron and Python. It was designed for **DJ**'s or **music groups** that want to add some **automated lighting effects** to their shows without big budget.

( starting at ~40$ including arduino and leds )

### Showcase

...

### How it works ?

![software-architecture](images/archi.png)

### What do i need to make one ?

1. [Install the program](#python-program)
2. [Build an arduino case](#arduino-part)
3. [Update the CONFIG.yml](#configuration)
4. [Setup your show with the effects and mods documentation](#effects---modes)
5. Enjoy !


# Table of contents
- [Install](#install)
  * [Python program](#python-program)
  * [Arduino setup](#arduino-setup)
- [Configuration](#configuration)
  * [Audio channels](#audio-channels)
  * [Virtual Audio Source](#virtual-audio-source)
    + [Linux](#linux)
    + [OSX](#osx)
  * [Midi channels](#midi-channels)
    + [OSX](#osx-1)
    + [Ableton live](#ableton-live)
  * [CONFIG.yml](#configyml)
    + [Sample config file](#sample-config-file)
- [Effects & Modes](#effects---modes)
  * [Effects](#effects)
    + [Sound based](#sound-based)
    + [Midi based](#midi-based)
    + [BPM based](#bpm-based)
    + [Generic](#generic)
  * [Modes](#modes)
- [Credits](#credits)
- [Contribute](#contribute)
- [License](#license)



# Install

If you encounter any problems running program, please open a new issue. Also, please consider opening an issue if you have any questions or suggestions for improving the installation process.

## Python program
Code is compatible with Python 3.7. Install dependencies using pip and the conda package manager.

```
pip install -r requirements.txt
conda install --file requirements.txt
```

## Arduino setup

As each led project has very specific needs, i kept this part as simple as possible.

In case you need a complete packaged product, there is a more advanced version of this part in the [Arduino folder](/arduino/). You will find 3d printed arduino cases and a more complete electronic scheme.

The arduino code is [here](arduino/serial-case/serial-case.ino).

PS : For now, please consider not using more than 254 leds by arduino.

![electronic-scheme](images/simple-electronic-scheme.png)


<!-- # Links
- [Wikipedia DMX](https://fr.wikipedia.org/wiki/DMX_(%C3%A9clairage) -->
<!--

  Mon projet est Music 2 led, il s'addresse aux dj et groupes de musiques, se trouvant
  ..., qui ont besoin d'un setup light automatisé.
  Il est plutot utilisé quand le groupe n'a pas beaucoup de budget

  TO DO BEFORE RELEASE

  OK - Package python with standalone version
  - Package electron
  - Toggle interface
  OK - Réparer la carte son de ginger et faire des tests avec ( test d'intensité )
  OK - Max brightness value sur pitchbend
  - Faire un helper imprimable sur piano
  - Changer BPM par time based 

  OK - Update README avec badges
  - Bel exemple réel en gif
  OK - Credit the audio reactive led strip author
  OK - 4 step graphic
  - Finaliser et update la charte graphique
  - Faire une branch dev et master
  OK - Utiliser le semantic versionning MAJOR.MINOR.PATCH
  - Gh page ?

  # VIZ
  OK - Piano : velocité
  - Piano : pitch et l'autre
  OK - Mettre un max a intensity_channels ( ajouter du gradient ? )

  # MAVEN besoins

  # Grosse saturation de ouf
  # Utiliser le mouvement de l'onde de la batterie pour les leds
  # entre 50 et 110 Decibels

  # 27 novembre


 -->

# Configuration

This program will use Audio ports, Midi ports and Serial ports.

To help you to configure your CONFIG.yml correctly, there is a little helper that
will list all available ports for each of them.

```
npm run list-ports
```

## Audio channels

This program streams audio from the default audio input device (set by the operating system).

Examples of typical audio sources:
- Audio cable connected to the audio input jack (requires USB sound card on Raspberry Pi)
- Webcam microphone, headset, studio recording microphone, etc

<!-- You can make some tests with a tone generator and the spectrum mode
https://www.szynalski.com/tone-generator/ -->

## Virtual Audio Source
You can use a "virtual audio device" to transfer audio playback from one application to another. This means that you can play music on your computer and connect the playback directly into the program.

### Linux
Linux users can use [Jack Audio](http://jackaudio.org/) to create a virtual audio device.

### OSX
On OSX, [Loopback](https://www.rogueamoeba.com/loopback/) can be use to create a virtual audio device.

### Windows
...

## Midi channels

### OSX

![osx-midi-settings](images/osx-midi-settings.png)

### Ableton live

![ableton-midi-settings](images/ableton-midi-settings.png)

...

## CONFIG.yml

You can validate the config file with

```
npm run test-config
```

### Sample config file

```yml

---  # document start

# Desired framerate

fps: 60

# Tell to electron to display the GUI or not

display_interface: false

# Audio ports
# List of used audio ports
# Can be listed with listAvailableDevices.sh
# Can be changed with "Change audio channel"

audio_ports:
  -
    name: Built-in Microphone
    min_frequency: 200
    max_frequency: 12000
    sampling_rate: 44000
    number_of_audio_samples: 24
    min_volume_threshold: 1e-7
    n_rolling_history: 4

# Strips
# They represents independant Arduino cases

strips:
  -

    # Name of the strip
    # Only used in the GUI

    name: Led strip name

    # Name of the associated serial port
    # Can be listed with listAvailableDevices.sh

    serial_port_name: /dev/tty.usbserial-14210

    # Maximum allowed brightness
    # Can be used to limit the power consumption
    # Check the Arduino part readme for more informations about it

    max_brightness: 255

    # Midi channels
    # Can be listed with listAvailableDevices.sh
    # associated_midi_channels : used for midi based visualizers
    # midi_ports_for_changing_mode : used for live changing modes

    associated_midi_channels:
      - Audio2Led Synth
    midi_ports_for_changing_mode:
      - Audio2Led ChangeMod

    # Reverse and mirror mods

    is_reverse: false
    is_mirror: false

    # BPM value that is used in BPM based visualizers

    bpm: 120

    # Shapes
    # Real shape : represents the physical shape of the strip
    # Shapes : represents virtual shapes
    # Be sure that both of them not contains odd numbers,
    # it may cause crash

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

    # Available color schemes
    # Can be changed via "Change color scheme"

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

    # Default parameters for various stuff
    # Be sure that you are not attempting to access to an index that not
    # exists, it may cause crash

    active_audio_channel_index: 0
    active_shape_index: 0
    active_color_index: 0
    active_color_scheme_index: 0
    active_visualizer_effect: scroll

...  # document end

```


# Effects & Modes

Music To Led has 16 visualization effects and 8 mods.

They can be live changed via dedicated Midi channels. You can choose to use programs like Ableton Live to automate these changes or use a dedicated synthetiser / pad to change them manually during the show.

**Principle** You have to send a midi note signal for activating / modifying effects. The table just after will show you the documentation.

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
| 26 | D-0 | **Change Max Brightness** | Size based on velocity | ![scroll](images/nothing.gif)
| 27 | D#-0 | **Reset Frame** | - | ![scroll](images/nothing.gif)


# Credits
This project was a fork of the great [audio-reactive-led-strip](https://github.com/scottlawsonbc/audio-reactive-led-strip). A lot of code has been rewritten since the beginning but it still remains some of the visualizers and audio processing code.

# Contribute
Feel free to send me an e-mail or submit a pull request.

# License
This project was developed by Thibaud FRERE and is released
under the MIT License.
